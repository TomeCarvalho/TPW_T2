from app.models import Group, Product, ProductImage, Sale, ProductInstance
from rest_framework import serializers
from django.contrib.auth import get_user_model


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    group = GroupSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class ProductInstanceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductInstance
        fields = '__all__'


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


