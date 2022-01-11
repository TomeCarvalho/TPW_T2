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
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ws/token-auth', obtain_auth_token),  # Built-in view for authentication
    path('ws/signup', views.signup),
    path('ws/dashboard', views.Dashboard.as_view()),
    path('ws/my-products', views.MyProducts.as_view()),
    path('ws/products/<int:i>', views.ProductView.as_view()),
    path('ws/cart', views.Cart.as_view()),
    path('ws/cart/checkout', views.CartCheckout.as_view()),
    path('ws/history/purchases', views.PurchaseHistory.as_view()),
    path('ws/history/sales', views.SaleHistory.as_view()),
    path('ws/add-product-stock', views.AddStock.as_view()),
    path('ws/add-product-img', views.AddProductImage.as_view()),
    path('ws/add-product-group', views.AddProductGroup.as_view()),
    path('ws/toggle-product-visibility', views.ToggleProductVisibility.as_view()),
    # path('ws/test-token', views.TestToken.as_view())
]
