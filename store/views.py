from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets, serializers, status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import Category, SubCategory, Product, CartProduct, Cart
from .pagination import Pagination
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, CartProductSerializer, \
    CartSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = Pagination


class SubCategoryList(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    pagination_class = Pagination

    def get_queryset(self, *args, **kwargs):
        category_slug = self.kwargs.get("cat")
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                f"There's no any category with given slug {category_slug}"
            )
        return SubCategory.objects.filter(parent_category=category).order_by('id')


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = Pagination


class CartProductCreate(CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        prod_slug = self.kwargs.get("prod")
        try:
            product = Product.objects.get(slug=prod_slug)
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                f"There's no any product with given slug {prod_slug}"
            )
        cart_product, created = CartProduct.objects.get_or_create(
            user=request.user, product=product, defaults={'quantity': request.data.get("quantity")}
        )
        if not created:
            raise serializers.ValidationError("This product is already in your cart.")
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(cart_product)
        serializer = self.get_serializer(cart_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartProductUpdate(UpdateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        prod_slug = self.kwargs.get("prod")
        try:
            cart_product = CartProduct.objects.get(user=request.user, product__slug=prod_slug)
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError(
                f"There's no such product in your cart with slug {prod_slug}"
            )

        quantity = request.data.get("quantity")
        if quantity is not None:
            cart_product.quantity = quantity
            cart_product.save()

        serializer = self.get_serializer(cart_product)
        return Response(serializer.data)


class CartList(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        Cart.objects.get_or_create(user=user)
        return Cart.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartProductDelete(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        prod_slug = self.kwargs.get("prod")
        try:
            cart_product = CartProduct.objects.get(user=request.user, product__slug=prod_slug)
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError(
                f"There's no such product in your cart with slug {prod_slug} :)"
            )
        cart_product.delete()
        serializer = self.get_serializer(cart_product)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CartClearView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            cart_products = CartProduct.objects.filter(user=request.user)
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError(
                f"Your cart is empty :)"
            )
        cart_products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
