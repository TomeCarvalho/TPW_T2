from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from rest_framework.authtoken.admin import User
from rest_framework.views import APIView

from .forms import SignUpForm, PaymentForm, SearchForm, ProductForm
from django.shortcuts import render
from app.models import Group, Product, Sale, ProductInstance, ProductImage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q

from itertools import zip_longest

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import GroupSerializer, ProductSerializer, ProductImageSerializer, SaleSerializer, \
    ProductInstanceSerializer, UserSerializer


@api_view(['GET'])
def get_group(request, i):
    """Get a group by ID (404 if it doesn't exist)."""
    try:
        group = Group.objects.get(id=i)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(GroupSerializer(group).data)


@api_view(['GET'])
def get_groups(request):
    """Get the list of groups."""
    groups = Group.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        groups = groups[:num]
    return Response(GroupSerializer(groups, many=True).data)


@api_view(['GET'])
def get_product(request, i):
    """Get a product by ID (404 if it doesn't exist)."""
    try:
        product = Product.objects.get(id=i)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ProductSerializer(product).data)


@api_view(['GET'])
def get_products(request):
    """Get the list of products."""
    products = Product.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        products = products[:num]
    return Response(ProductSerializer(products, many=True).data)


@api_view(['GET'])
def get_product_image(request, i):
    """Get a product image by ID (404 if it doesn't exist)."""
    try:
        product_image = ProductImage.objects.get(id=i)
    except ProductImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ProductImageSerializer(product_image).data)


@api_view(['GET'])
def get_product_images(request):
    """Get the list of product images."""
    product_images = ProductImage.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        product_images = product_images[:num]
    return Response(ProductImageSerializer(product_images, many=True).data)


@api_view(['GET'])
def get_sale(request, i):
    """Get a sale by ID (404 if it doesn't exist)."""
    try:
        sale = Sale.objects.get(id=i)
    except Sale.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(SaleSerializer(sale).data)


@api_view(['GET'])
def get_sales(request):
    """Get the list of sales."""
    sales = Sale.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        sales = sales[:num]
    return Response(SaleSerializer(sales, many=True).data)


@api_view(['GET'])
def get_product_instance(request, i):
    """Get a product instance by ID (404 if it doesn't exist)."""
    try:
        product_instance = ProductInstance.objects.get(id=i)
    except ProductInstance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ProductInstanceSerializer(product_instance).data)


@api_view(['GET'])
def get_product_instances(request):
    """Get the list of product instances."""
    product_instances = ProductInstance.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        product_instances = product_instances[:num]
    return Response(SaleSerializer(product_instances, many=True).data)


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


class TestToken(APIView):
    """Test: Return OK status if logged in (using token in auth header)."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(f'{request.user = }')
        return Response(status.HTTP_200_OK)


class MyProducts(APIView):
    """Get the list of the user's products.
    Allows filtering by: group, category, upper price, lower price."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(f'{request = }')
        req_get = request.GET
        group = req_get.get('group')
        category = req_get.get('category')
        upper = req_get.get('upper')
        lower = req_get.get('lower')
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
        return Response(ProductSerializer(product_list, many=True).data)

# def index(request):
#     return redirect(dashboard)
#
#
# @csrf_protect
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect(dashboard)
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form, 'logged': request.user.is_authenticated})
#
#
# def dashboard(request):
#     search_prompt = None
#     if request.method == 'POST':
#         print(request.POST)
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             print("VALID")
#             group = form.cleaned_data.get('by_group')
#             category = form.cleaned_data.get('by_category')
#             upper = form.cleaned_data.get('by_price_Upper')
#             lower = form.cleaned_data.get('by_price_Lower')
#             order = form.cleaned_data.get('order')
#
#             q = Q()
#             if group:
#                 q &= Q(group__name=group)
#             if category:
#                 q &= Q(category=category)
#             if upper:
#                 q &= Q(price__lte=upper)
#             if lower:
#                 q &= Q(price__gte=lower)
#             if request.user.is_authenticated:
#                 q &= ~Q(seller=request.user)
#                 if not request.user.is_superuser:
#                     q &= Q(hidden=False)
#             else:
#                 q &= Q(hidden=False)
#             product_list = Product.objects.filter(q)
#
#             if order:
#                 product_list = product_list.order_by(order)
#         else:
#             product_list = Product.objects.all()
#     else:
#         form = SearchForm()
#         search_prompt = request.GET.get('search_prompt', '')
#         product_list = Product.objects.filter(name__icontains=search_prompt) if search_prompt else Product.objects.all()
#     if request.user.is_authenticated:
#         product_list = product_list.exclude(seller=request.user)
#         if not request.user.is_superuser:
#             product_list = product_list.exclude(hidden=True)
#     else:
#         product_list = product_list.exclude(hidden=True)
#
#     pgs = zip_longest(*(iter(product_list),) * 3)  # chunky!
#     tparams = {
#         "logged": request.user.is_authenticated,
#         "three_page_group": pgs,
#         "search_prompt": search_prompt,
#         "form": form
#     }
#     return render(request, "dashboard.html", tparams)
#
#

# def newproduct(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         print(request.POST)
#         post = request.POST
#         if form.is_valid():
#             # processar dados e inserir na bd!
#             category = form.cleaned_data['category']
#             name = form.cleaned_data['name']
#             stock = form.cleaned_data['stock']
#             description = form.cleaned_data['description']
#             price = form.cleaned_data['price']
#             group = form.cleaned_data['group']
#             img = form.cleaned_data['image']
#             if group in [grp.name for grp in Group.objects.all()]:
#                 real_group = Group.objects.get(name=group)
#             else:
#                 real_group = Group(name=group)
#                 real_group.save()
#             new_product = Product(category=category, name=name, stock=stock, description=description, price=price,
#                                   seller=request.user)
#             new_product.save()
#             new_product.group.add(real_group)
#             image = ProductImage(url=img, product=new_product)
#             image.save()
#             return redirect(dashboard)
#     else:
#         form = ProductForm()
#
#     return render(request, "newproduct.html", {
#         "form": form,
#         "logged": request.user.is_authenticated,
#     })
#
#
# def product_page(request, i, message=None):
#     """Returns the page of the product with ID i if it exists, or an error page if not."""
#     try:
#         product = Product.objects.get(id=i)
#         if product.hidden and not request.user.is_superuser:
#             return redirect(dashboard)
#         images = product.images
#         groups = product.group.all()
#         n = range(1, len(images))
#         params = {
#             'message': message,
#             'category': product.category.capitalize(),
#             'name': product.name,
#             'stock': product.stock,
#             'images': images,
#             'n': n,
#             'description': product.description,
#             'price': product.price,
#             'seller': product.seller,
#             'i': i,
#             'groups': groups,
#             'logged': request.user.is_authenticated,
#             'hidden': product.hidden,
#             'hidden_toggle_text': 'Unhide Product' if product.hidden else 'Hide Product',
#             'fa_icon': 'fa-eye' if product.hidden else 'fa-eye-slash'
#         }
#         return render(request, 'product_page.html', params)
#     except ObjectDoesNotExist:
#         return render(request, 'product_page_error.html', {'i': i})
#
#
# NOT_ENOUGH_STOCK_MSG = 'The seller doesn\'t have enough of this product in stock at the moment.'
# INVALID_QTY_MSG = 'Invalid quantity. It must be a positive number.'
# ADDED_MSG = 'Product added to cart!'
#
#
# @login_required
# def add_to_cart(request):
#     """Adds a product to the cart. Requires the user to be logged in."""
#     params = {'logged': request.user.is_authenticated}
#     if request.method == 'POST':
#         product_id = request.POST['product_id']
#         quantity = request.POST['quantity']
#     else:  # If a sneaky user types it into the URL bar
#         return redirect(dashboard)
#     try:
#         quantity = int(quantity)
#     except ValueError:
#         print(f'ValueError with {product_id = }, {quantity = }')
#         params['alert_class'] = 'alert-danger'
#         params['text'] = INVALID_QTY_MSG
#         return product_page(request, product_id, params)
#         # return render(request, 'message.html', params)
#     if quantity <= 0:
#         print(f'Invalid Quantity with {quantity = }')
#         params['alert_class'] = 'alert-danger'
#         params['text'] = INVALID_QTY_MSG
#         return product_page(request, product_id, params)
#
#     user = request.user
#     product = Product.objects.get(id=product_id)
#     try:  # Check if the user already has the product in their cart and thus is just increasing the quantity
#         user_instance = ProductInstance.objects.get(client=user, product=product, sold=False)
#         if user_instance.quantity + quantity > product.stock:
#             print(
#                 f'Not enough stock of {product.name} for {user.username} ({user_instance.quantity + quantity}/{product.stock})')
#             params['alert_class'] = 'alert-warning'
#             params['text'] = NOT_ENOUGH_STOCK_MSG
#             return product_page(request, product_id, params)
#         user_instance.quantity += quantity
#         user_instance.save()
#         print(f'Increased quantity of {product} in {user}\'s cart by {quantity}')
#         params['alert_class'] = 'alert-success'
#         params['text'] = ADDED_MSG
#         return product_page(request, product_id, params)
#     except ObjectDoesNotExist:
#         if quantity > product.stock:
#             params['alert_class'] = 'alert-warning'
#             params['text'] = NOT_ENOUGH_STOCK_MSG
#             return product_page(request, product_id, params)
#         ProductInstance(
#             product=product,
#             quantity=quantity,
#             client=user,
#             sold=False
#         ).save()
#         print(f'Instance of product {product} added to {user}\'s cart')
#
#     params['alert_class'] = 'alert-success'
#     params['text'] = ADDED_MSG
#     return product_page(request, product_id, params)
#
#
# def cart(request):
#     logged = request.user.is_authenticated
#     if logged:
#         product_instance_list = ProductInstance.objects.filter(client=request.user, sold=False)
#         total = 0
#         for product in product_instance_list:
#             total += product.product.price * product.quantity
#         tparams = {
#             "logged": logged,
#             "prod_insts": product_instance_list,
#             "total": total
#         }
#         return render(request, "cart.html", tparams)
#     else:
#         return redirect(dashboard)
#
#
# def checkout(request):
#     logged = request.user.is_authenticated
#     if logged:
#         if request.method == "POST":
#             form = PaymentForm(request.POST)
#             if form.is_valid():
#                 print("ei")
#                 prod_insts = ProductInstance.objects.filter(client=request.user, sold=False)
#                 if any(prod_inst.quantity > prod_inst.product.stock for prod_inst in prod_insts):
#                     return redirect(dashboard)  # TODO: handle this in a better fashion
#                 payment_method = form.cleaned_data['card']
#                 sale = Sale(client=request.user, paymentMethod=payment_method)
#                 sale.save()
#                 for prod_inst in prod_insts:
#                     product = prod_inst.product
#                     product.stock -= prod_inst.quantity
#                     prod_inst.sold = True
#                     prod_inst.sale = sale
#                     prod_inst.save()
#                     product.save()
#                 sale.save()
#                 return redirect(dashboard)
#             else:
#                 print("NEY")
#         else:
#             form = PaymentForm()
#         tparams = {
#             "logged": logged,
#             "form": form,
#         }
#         return render(request, "payment.html", tparams)
#     else:
#         return redirect(dashboard)
#
#
# @login_required
# def history(request):
#     """Returns the purchase and sale history of the user."""
#     logged = request.user.is_authenticated
#     user = request.user
#     purchases = ProductInstance.objects.filter(client=user, sold=True).select_related()
#     sales = ProductInstance.objects.filter(product__seller=user, sold=True).select_related()
#     print(f'{purchases = }\n{sales = }')
#     params = {
#         'logged': logged,
#         'purchases': purchases,
#         'sales': sales
#     }
#     return render(request, 'history.html', params)
#
#
# @login_required
# def remove_from_cart(request):
#     if request.method == 'POST':
#         product_id = request.POST['productInstance']
#     else:  # If a sneaky user types it into the URL bar
#         return redirect(dashboard)
#     ProductInstance.objects.filter(id=product_id).delete()
#     return redirect(cart)
#
#
# @login_required
# def add_stock(request):
#     """Increases the stock of a user's product"""
#     if request.method == 'POST':
#         product_id = request.POST['product_id']
#         quantity = request.POST['stock']
#     else:
#         return redirect(dashboard)
#     try:
#         quantity = int(quantity)
#     except ValueError:
#         # messages.info(request, INVALID_QTY_MSG)
#         print(f'ValueError with {product_id = }, {quantity = }')
#         return redirect(dashboard)
#     if quantity <= 0:
#         # messages.info(request, INVALID_QTY_MSG)
#         print(f'Invalid Quantity with {quantity = }')
#         return redirect(dashboard)
#     product = Product.objects.get(id=product_id)
#     product.stock += quantity
#     product.save()
#     print(f'Stock of {product.name} increased by {quantity}')
#     return redirect(product_page, product_id)
#
#
# @login_required
# def add_image(request):
#     if request.method == 'POST':
#         product_id = request.POST['product_id']
#         image = request.POST['image']
#     else:
#         return redirect(dashboard)
#     product = Product.objects.get(id=product_id)
#     image = ProductImage(url=image, product=product)
#     image.save()
#     return redirect(product_page, product_id)
#
#
# def add_group(request):
#     if request.method == 'POST':
#         product_id = request.POST['product_id']
#         group = request.POST['group']
#     else:
#         return redirect(dashboard)
#     if group in [grp.name for grp in Group.objects.all()]:
#         real_group = Group.objects.get(name=group)
#     else:
#         real_group = Group(name=group)
#         real_group.save()
#     product = Product.objects.get(id=product_id)
#     product.group.add(real_group)
#     product.save()
#     return redirect(product_page, product_id)
#
#
# @user_passes_test(lambda user: user.is_superuser)
# def product_hidden_toggle(request):
#     """Hides/Unhides a product from users that aren't admins."""
#     if request.method == 'POST':
#         product_id = request.POST['product_id']
#     else:
#         return redirect(dashboard)
#     product = Product.objects.get(id=product_id)
#     product.hidden = not product.hidden
#     product.save()
#     return redirect(dashboard)
#
#
# def message(request):
#     return None
