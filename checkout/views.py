import json
from datetime import datetime
from decimal import Decimal
from os import name
from unicodedata import category

from django.db.models import Case, CharField, F, IntegerField, Value, When
# from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status, views, viewsets

from utils.product_creation import ProductCreation

from . import models
from .serializers import ProductSerializer


class ListProductView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.annotate(
            custom_order=Case(
                When(category__name="Cap", then=1),
                output_field=IntegerField())
        ).order_by('custom_order').order_by('-created_at')


class NewProductView(views.APIView):
    def post(self, request):

        product_data = request.data.dict()

        try:
            file = request.FILES[next(iter(request.FILES))]
            product_data.pop("image")
        except Exception:
            error_msg = "It was not possible to create the product without an image"
            return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_category = product_data.get(
                "category") if product_data.get("category") else None
            product_data.pop("category")
            if not product_category:
                error_msg = f"""It was not possible to create the category '{product_data.get("category")}' for this product."""
                return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            error_msg = f"""It was not possible to create the category '{product_data.get("category")}' for this product."""
            return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

        category_obj, _ = models.ProductCategory.objects.get_or_create(
            defaults={"name": product_category.title},
            name__iexact=product_category)

        base_product_fields = ProductCreation(
            product_data).product_base_fields()

        product_obj, _ = models.Product.objects.get_or_create(
            defaults={
                "price": Decimal(base_product_fields.get("price")),
                "initial_stock": int(base_product_fields.get("initial_stock")),
                "current_stock": int(base_product_fields.get("current_stock")),
                "url": file,
            },
            main_color=base_product_fields.get("main_color"),
            secondary_color=base_product_fields.get("secondary_color"),
            brand=base_product_fields.get("brand"),
            description=f'{category_obj.name} {base_product_fields.get("brand")} {base_product_fields.get("main_color")}/{base_product_fields.get("secondary_color")} {datetime.today().year}',
            category=category_obj
        )

        specific_product_fields = ProductCreation(
            product_data).product_specific_fields()

        for attr, value in specific_product_fields.items():
            if value:
                try:
                    attribute_obj, _ = models.ProductAttribute.objects.get_or_create(
                        defaults={"description": attr.title},
                        description__iexact=attr
                    )

                except Exception:
                    error_msg = f"""It was not possible to create the attribute '{attr}' for this product."""
                    return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

                product_attribute_value_obj, _ = product_obj.product.get_or_create(
                    defaults={"product": product_obj},
                    value=value,
                    attribute=attribute_obj
                )

        return response.Response(status=status.HTTP_201_CREATED)
