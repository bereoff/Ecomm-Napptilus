from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListProductView, NewProductView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("products/", ListProductView.as_view(), name="products"),
    path("products/new/", NewProductView.as_view(), name="new_product"),
]
