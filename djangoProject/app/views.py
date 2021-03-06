import json

from rest_framework.authtoken.admin import User
from rest_framework.views import APIView

from .forms import PaymentForm, ProductForm
from app.models import Group, Product, Sale, ProductInstance, ProductImage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import ProductSerializer, ProductInstanceSerializer, UserSerializer, GroupSerializer


@api_view(['POST'])
def signup(request):
    """Create a new user using a JSON like {"username": "sussus", "password": "amogus"}."""
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        init_data = serialized.initial_data
        User.objects.create_user(username=init_data['username'], password=init_data['password'])
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperUser(APIView):
    """Test: Return OK status if logged in (using token in auth header)."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            return Response(request.user.is_superuser, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class ProductView(APIView):
    """GET: Get a product through its ID.
    Sucess status: 200 OK.
    Failure status: 404 NOT FOUND."""
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, i):
        try:
            return Response(ProductSerializer(Product.objects.get(id=i)).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class MyProducts(APIView):
    """GET: Get the list of the user's products.
    Allows filtering by: group, category, upper price, lower price.
    POST: Add a new product.
    Sucess status: 201 CREATED.
    Failure status: 400 BAD REQUEST."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(f'{request = }')
        req_get = request.GET
        group = req_get.get('group')
        category = req_get.get('category')
        upper = req_get.get('upper')
        lower = req_get.get('lower')
        order = req_get.get('order')
        q = Q(seller=request.user)

        if group:
            q &= Q(group__name=group)
        if category:
            q &= Q(category=category)
        if upper:
            q &= Q(price__lte=upper)
        if lower:
            q &= Q(price__gte=lower)
        product_list = Product.objects.filter(q)
        if order:
            product_list = product_list.order_by(order)
        return Response(ProductSerializer(product_list, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        print("POST PRODUCT")
        raw_data = request.read()
        print(raw_data)
        data = json.loads(raw_data)
        form = ProductForm(data)
        print(form)

        if form.is_valid():
            print("GOOD")
            category = form.cleaned_data['category']
            name = form.cleaned_data['name']
            stock = form.cleaned_data['stock']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            group = form.cleaned_data['group']
            img = form.cleaned_data['image']
            if group in [grp.name for grp in Group.objects.all()]:
                real_group = Group.objects.get(name=group)
            else:
                real_group = Group(name=group)
                real_group.save()
            new_product = Product(category=category, name=name, stock=stock, description=description, price=price,
                                  seller=request.user)
            new_product.save()
            new_product.group.add(real_group)
            image = ProductImage(url=img, product=new_product)
            image.save()
            return Response(ProductSerializer(new_product).data, status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class Dashboard(APIView):
    """GET: Gets the products, excluding the user's own, if logged in.
    Allows filtering and sorting: group, category, upper (price), lower (price), order."""
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        print(request)
        req_get = request.GET
        group = req_get.get('group')
        category = req_get.get('category')
        upper = req_get.get('upper')
        lower = req_get.get('lower')
        order = req_get.get('order')
        search_prompt = req_get.get('search_prompt')
        q = Q()
        print(search_prompt)
        if group:
            q &= Q(group__name=group)
        if category:
            q &= Q(category=category)
        if upper:
            q &= Q(price__lte=upper)
        if lower:
            q &= Q(price__gte=lower)
        if search_prompt:
            q &= Q(name__icontains=search_prompt)

        if request.user.is_authenticated:
            q &= ~Q(seller=request.user)
            if not request.user.is_superuser:
                q &= Q(hidden=False)
        else:
            q &= Q(hidden=False)

        product_list = Product.objects.filter(q)
        if order:
            product_list = product_list.order_by(order)

        return Response(ProductSerializer(product_list, many=True).data, status=status.HTTP_200_OK)


# NOT_ENOUGH_STOCK_MSG = 'The seller doesn\'t have enough of this product in stock at the moment.'
# INVALID_QTY_MSG = 'Invalid quantity. It must be a positive number.'
# ADDED_MSG = 'Product added to cart!'

class Cart(APIView):
    """DELETE: Delete a product's instances from a cart.
    GET: Get the product instances that the user's cart is composed of.
    POST: Add instances of a product to the cart."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        #print("DELETE")
        raw_data = request.read()
        #print(raw_data)
        data = json.loads(raw_data)
        if not data.get("productInstance"):
            return Response(status.HTTP_400_BAD_REQUEST)
        product_id = data.get("productInstance")
        prod_insts = ProductInstance.objects.filter(id=product_id)
        if prod_insts:
            prod_insts.delete()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Total price calculation removed, Angular's job now
        product_instance_list = ProductInstance.objects.filter(client=request.user, sold=False)
        print(ProductInstanceSerializer(product_instance_list, many=True).data)
        return Response(ProductInstanceSerializer(product_instance_list, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        print("POST")
        raw_data = request.read()
        print(raw_data)
        data = json.loads(raw_data)
        if not data.get("product_id"):
            return Response(status.HTTP_400_BAD_REQUEST)

        product_id = data.get('product_id')
        quantity = data.get('quantity')
        try:
            quantity = int(quantity)
        except ValueError:
            return Response(status.HTTP_400_BAD_REQUEST)
        if quantity <= 0:
            return Response(status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        if product.seller == request.user:
            return Response(status.HTTP_400_BAD_REQUEST)

        try:  # Check if the user already has the product in their cart and thus is just increasing the quantity
            user_instance = ProductInstance.objects.get(client=user, product=product, sold=False)
            if user_instance.quantity + quantity > product.stock:
                print(
                    f'Not enough stock of {product.name} for {user.username} ({user_instance.quantity + quantity}/{product.stock})')
                return Response(status.HTTP_400_BAD_REQUEST)
            user_instance.quantity += quantity
            user_instance.save()
            print(f'Increased quantity of {product} in {user}\'s cart by {quantity}')
            return Response(ProductInstanceSerializer(user_instance).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            if quantity > product.stock:
                return Response(status.HTTP_400_BAD_REQUEST)

            product_instance = ProductInstance(
                product=product,
                quantity=quantity,
                client=user,
                sold=False
            )
            product_instance.save()
            print(f'Instance of product {product} added to {user}\'s cart')

        return Response(ProductInstanceSerializer(product_instance).data, status=status.HTTP_200_OK)


#


class CartCheckout(APIView):
    """POST: Checkout: purchase the items in the cart.
    Success status: 200 OK.
    Failures status: 400 BAD REQUEST."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        raw_data = request.read()
        # print(raw_data)
        data = json.loads(raw_data)
        form = PaymentForm(data)
        if form.is_valid():
            prod_insts = ProductInstance.objects.filter(client=request.user, sold=False)
            if any(prod_inst.quantity > prod_inst.product.stock for prod_inst in prod_insts):
                return Response(status.HTTP_400_BAD_REQUEST)
            payment_method = form.cleaned_data['card']
            sale = Sale(client=request.user, paymentMethod=payment_method)
            print(sale)
            sale.save()
            for prod_inst in prod_insts:
                product = prod_inst.product
                product.stock -= prod_inst.quantity
                prod_inst.sold = True
                prod_inst.sale = sale
                prod_inst.save()
                product.save()
            sale.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST, )


class PurchaseHistory(APIView):
    """GET: Get the purchase history of the user."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        purchases = ProductInstance.objects.filter(client=request.user, sold=True).select_related()
        print("purchases", purchases)
        return Response(ProductInstanceSerializer(purchases, many=True).data, status=status.HTTP_200_OK)


class SaleHistory(APIView):
    """GET: Get the sale history of the user."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sales = ProductInstance.objects.filter(product__seller=request.user, sold=True).select_related()
        print("sales", sales)
        return Response(ProductInstanceSerializer(sales, many=True).data, status=status.HTTP_200_OK)


class AddStock(APIView):
    """POST: Increases the stock of a user's product."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("POST")
        raw_data = request.read()
        print(raw_data)
        data = json.loads(raw_data)
        if not data.get("product_id") and not data.get("stock"):
            return Response(status.HTTP_400_BAD_REQUEST)

        product_id = data.get('product_id')
        quantity = data.get('quantity')
        try:
            quantity = int(quantity)
        except ValueError:
            print(f'ValueError with {product_id = }, {quantity = }')
            return Response(status.HTTP_400_BAD_REQUEST)
        if quantity <= 0:
            print(f'Invalid Quantity with {quantity = }')
            return Response(status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        if product.seller != request.user:
            return Response(status.HTTP_403_FORBIDDEN)
        product.stock += quantity
        product.save()
        print(f'Stock of {product.name} increased by {quantity}')
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class AddProductImage(APIView):
    """POST: Adds an image to a product."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("POST")
        raw_data = request.read()
        print(raw_data)
        data = json.loads(raw_data)
        if not data.get("product_id") and not data.get("image"):
            return Response(status.HTTP_400_BAD_REQUEST)

        product_id = data.get('product_id')
        image = data.get('image')
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        if product.seller != request.user:
            return Response(status.HTTP_403_FORBIDDEN)
        ProductImage(url=image, product=product).save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class AddProductGroup(APIView):
    """POST: Adds a group to a product.
    Creates the group if it doesn't exist yet."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]



    def post(self, request):

        print("POST")
        raw_data = request.read()
        print(raw_data)
        data = json.loads(raw_data)
        if not data.get("product_id") and not data.get("group"):
            return Response(status.HTTP_400_BAD_REQUEST)

        product_id = data.get('product_id')
        group = data.get('group')

        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        if product.seller != request.user:
            return Response(status.HTTP_403_FORBIDDEN)

        if group in [grp.name for grp in Group.objects.all()]:
            real_group = Group.objects.get(name=group)
        else:
            real_group = Group(name=group)
            real_group.save()
        product.group.add(real_group)
        product.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class ToggleProductVisibility(APIView):
    """POST: Toggles the visibility of a product.
    Requires admin privileges."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):

        print("POST")
        raw_data = request.read()
        print(raw_data)
        data = json.loads(raw_data)
        if not data.get("product_id"):
            return Response(status.HTTP_400_BAD_REQUEST)

        product_id = data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        product.hidden = not product.hidden
        product.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class Groups(APIView):
    """GET: Gets the list of groups.
    POST: Adds a group."""
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        return Response(GroupSerializer(Group.objects.all(), many=True).data, status=status.HTTP_200_OK)


# class AddToCart(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request):
#         """Add a product to the cart."""
#         product_id = request.POST['product_id']
#         quantity = request.POST['quantity']
#         try:
#             quantity = int(quantity)
#         except ValueError:
#             return Response(status.HTTP_400_BAD_REQUEST)
#         if quantity <= 0:
#             return Response(status.HTTP_400_BAD_REQUEST)
#
#         user = request.user
#         try:
#             product = Product.objects.get(id=product_id)
#         except ObjectDoesNotExist:
#             return Response(status.HTTP_400_BAD_REQUEST)
#         if product.seller == request.user:
#             return Response(status.HTTP_400_BAD_REQUEST)
#
#         try:  # Check if the user already has the product in their cart and thus is just increasing the quantity
#             user_instance = ProductInstance.objects.get(client=user, product=product, sold=False)
#             if user_instance.quantity + quantity > product.stock:
#                 print(
#                     f'Not enough stock of {product.name} for {user.username} ({user_instance.quantity + quantity}/{product.stock})')
#                 return Response(status.HTTP_400_BAD_REQUEST)
#             user_instance.quantity += quantity
#             user_instance.save()
#             print(f'Increased quantity of {product} in {user}\'s cart by {quantity}')
#             return Response(ProductInstanceSerializer(user_instance).data, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist:
#             if quantity > product.stock:
#                 return Response(status.HTTP_400_BAD_REQUEST)
#
#             product_instance = ProductInstance(
#                 product=product,
#                 quantity=quantity,
#                 client=user,
#                 sold=False
#             )
#             product_instance.save()
#             print(f'Instance of product {product} added to {user}\'s cart')
#
#         return Response(ProductInstanceSerializer(product_instance).data, status=status.HTTP_200_OK)
#
#
# class RemoveFromCart(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def delete(self, request):
#         product_id = request.DELETE['productInstance']
#         prod_insts = ProductInstance.objects.filter(id=product_id)
#         if prod_insts:
#             prod_insts.delete()
#             return Response(status.HTTP_200_OK)
#         return Response(status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_group(request, i):
#     """Get a group by ID (404 if it doesn't exist)."""
#     try:
#         group = Group.objects.get(id=i)
#     except Group.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(GroupSerializer(group).data)


# @api_view(['GET'])
# def get_groups(request):
#     """Get the list of groups."""
#     groups = Group.objects.all()
#     if 'num' in request.GET:
#         num = int(request.GET['num'])
#         groups = groups[:num]
#     return Response(GroupSerializer(groups, many=True).data)


# @api_view(['GET'])
# def get_product(request, i):
#     """Get a product by ID (404 if it doesn't exist)."""
#     try:
#         product = Product.objects.get(id=i)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(ProductSerializer(product).data)


# @api_view(['GET'])
# def get_products(request):
#     """Get the list of products."""
#     products = Product.objects.all()
#     if 'num' in request.GET:
#         num = int(request.GET['num'])
#         products = products[:num]
#     return Response(ProductSerializer(products, many=True).data)


# @api_view(['GET'])
# def get_product_image(request, i):
#     """Get a product image by ID (404 if it doesn't exist)."""
#     try:
#         product_image = ProductImage.objects.get(id=i)
#     except ProductImage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(ProductImageSerializer(product_image).data)


# @api_view(['GET'])
# def get_product_images(request):
#     """Get the list of product images."""
#     product_images = ProductImage.objects.all()
#     if 'num' in request.GET:
#         num = int(request.GET['num'])
#         product_images = product_images[:num]
#     return Response(ProductImageSerializer(product_images, many=True).data)


# @api_view(['GET'])
# def get_sale(request, i):
#     """Get a sale by ID (404 if it doesn't exist)."""
#     try:
#         sale = Sale.objects.get(id=i)
#     except Sale.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(SaleSerializer(sale).data)


# @api_view(['GET'])
# def get_sales(request):
#     """Get the list of sales."""
#     sales = Sale.objects.all()
#     if 'num' in request.GET:
#         num = int(request.GET['num'])
#         sales = sales[:num]
#     return Response(SaleSerializer(sales, many=True).data)


# @api_view(['GET'])
# def get_product_instance(request, i):
#     """Get a product instance by ID (404 if it doesn't exist)."""
#     try:
#         product_instance = ProductInstance.objects.get(id=i)
#     except ProductInstance.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(ProductInstanceSerializer(product_instance).data)
#
#
# @api_view(['GET'])
# def get_product_instances(request):
#     """Get the list of product instances."""
#     product_instances = ProductInstance.objects.all()
#     if 'num' in request.GET:
#         num = int(request.GET['num'])
#         product_instances = product_instances[:num]
#     return Response(SaleSerializer(product_instances, many=True).data)
