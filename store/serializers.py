from rest_framework import serializers
from .models import Category, SubCategory, Product, CartProduct, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products', 'total_price', 'total_count']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.products.all())

    def get_total_count(self, obj):
        return sum(item.quantity for item in obj.products.all())
