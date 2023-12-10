from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddProductCartView, CartPurchasedView, ListCartView,
                    ListProductView, NewProductView, ProductAttributeView,
                    ProductCategoryView, ProductHardDeleteView,
                    ProductSoftDeleteView, UpdateProductView)

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("products/", ListProductView.as_view(), name="products"),
    path("products/new/", NewProductView.as_view(), name="new_product"),
    path("products/soft-delete/", ProductSoftDeleteView.as_view(),
         name="soft_product_delete"),
    path("products/hard-delete/<uuid:pk>/", ProductHardDeleteView.as_view(),
         name="hard_product_delete"),
    path("products/alteration/<uuid:pk>/", UpdateProductView.as_view(),
         name="product_alteration"),
    path("products/category/", ProductCategoryView.as_view(),
         name="product_categories"),
    path("products/attribute/", ProductAttributeView.as_view(),
         name="product_attributes"),
    path("products/cart/", ListCartView.as_view(),
         name="cart"),
    path("products/cart/new-product/", AddProductCartView.as_view(),
         name="add_to_cart"),
    path("products/cart/purchased/", CartPurchasedView.as_view(),
         name="purchased-cart"),
]
