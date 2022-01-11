"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ws/api-token-auth', obtain_auth_token),  # Built-in view for authentication
    path('ws/signup', views.signup),
    path('ws/groups', views.get_groups),
    path('ws/groups/<int:i>', views.get_group),
    path('ws/products', views.get_products),
    path('ws/products/<int:i>', views.ProductView.as_view()),
    path('ws/productimages', views.get_product_images),
    path('ws/productimages/<int:i>', views.get_product_image),
    path('ws/sales', views.get_sales),
    path('ws/sales/<int:i>', views.get_sale),
    path('ws/productinstances', views.get_product_instances),
    path('ws/productinstances/<int:i>', views.get_product_instance),
    path('ws/test_token', views.TestToken.as_view()),
    path('ws/myproducts', views.MyProducts.as_view()),
    path('ws/cart', views.Cart.as_view())

    # path('products/<int:i>', views.product_page),
    # path('', views.index),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # path('signup/', views.signup, name='signup'),
    # path('dashboard/', views.dashboard),
    # path('cart/', views.cart),
    # path('cart/checkout', views.checkout),
    # path('dashboard/', views.dashboard),
    # path('myproducts/', views.myproducts, name='myproducts'),
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    # path('newproduct/', views.newproduct, name='newproduct'),
    # path('history/', views.history, name='history'),
    # path('add_stock/', views.add_stock, name='add_stock'),
    # path('add_group/', views.add_group, name='add_group'),
    # path('add_image/', views.add_image, name='add_image'),
    # path('product_hidden_toggle/', views.product_hidden_toggle, name='product_hidden_toggle'),
    # path('message/', views.message, name='message'),
    # path('removefromcart/', views.remove_from_cart, name='delete'),
]
