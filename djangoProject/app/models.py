from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Product(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group, blank=True)
    hidden = models.BooleanField(default=False)

    @property
    def images(self):
        return self.productimage_set.all()


class ProductImage(models.Model):
    url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Sale(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(prod_inst.product.price * prod_inst.quantity for prod_inst in self.productinstance_set.all())


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)
    sold = models.BooleanField()

    @property
    def price(self):
        return self.product.price * self.quantity


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Automatically generate auth tokens for users."""
    if created:
        Token.objects.create(user=instance)
