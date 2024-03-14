from django.urls import path

from store.apps import StoreConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from store.views import CartList, CategoryList, SubCategoryList, ProductList, CartProductCreate, CartProductDelete, \
    CartClearView, CartProductUpdate

app_name = StoreConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("cart/", CartList.as_view(), name="cart_list"),
    path("cats/", CategoryList.as_view(), name="cat_list"),
    path("<slug:cat>/sub_cats/", SubCategoryList.as_view(), name="sub_cat_list"),
    path("products/", ProductList.as_view(), name="product_list"),
    path("products/<slug:prod>/add/", CartProductCreate.as_view(), name="add_to_cart"),
    path("products/<slug:prod>/change/", CartProductUpdate.as_view(), name="update_cart"),
    path("products/<slug:prod>/remove/", CartProductDelete.as_view(), name="remove_from_cart"),
    path("cart/clear/", CartClearView.as_view(), name="clear_cart"),
]
