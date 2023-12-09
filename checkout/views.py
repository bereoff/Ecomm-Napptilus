from datetime import datetime
from decimal import Decimal

from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status, views

from utils.product_handler import ProductHandler

from . import models
from .serializers import (ProductAttributeSerializer,
                          ProductCategorySerializer, ProductSerializer)


class ListProductView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.annotate(
            custom_order=Case(
                When(category__name="Cap", then=1),
                output_field=IntegerField())
        ).order_by('custom_order').order_by('-created_at')


class ProductCategoryView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductAttributeView(generics.ListAPIView):
    queryset = models.ProductAttribute.objects.all().order_by(
        "-created_at", "description")
    serializer_class = ProductAttributeSerializer


class NewProductView(views.APIView):
    def post(self, request):

        product_data = request.data.dict()

        try:
            file = request.FILES[next(iter(request.FILES))]
            product_data.pop("image")
        except Exception:
            error_msg = {
                "detail": "It was not possible to create the product without an image"}
            return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_category = product_data.get(
                "category") if product_data.get("category") else None
            product_data.pop("category")
            if not product_category:
                error_msg = {
                    "detail": f"""It was not possible to create the category '{product_data.get("category")}' for this product."""}
                return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            error_msg = {
                "detail": f"""It was not possible to create the category '{product_data.get("category")}' for this product."""}
            return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

        category_obj, _ = models.ProductCategory.objects.get_or_create(
            defaults={"name": product_category.title},
            name__iexact=product_category)

        base_product_fields = ProductHandler(
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

        specific_product_fields = ProductHandler(
            product_data).product_specific_fields()

        for attr, value in specific_product_fields.items():
            if value:
                try:
                    attribute_obj, _ = models.ProductAttribute.objects.get_or_create(
                        defaults={"description": attr.title},
                        description__iexact=attr
                    )

                except Exception:
                    error_msg = {
                        "detail": f"""It was not possible to create the attribute '{attr}' for this product."""}
                    return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

                product_attribute_value_obj, _ = product_obj.product.get_or_create(
                    defaults={"product": product_obj},
                    value=value,
                    attribute=attribute_obj
                )

        return response.Response(data={"detail": "successfully created."}, status=status.HTTP_201_CREATED)


class UpdateProductView(generics.UpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):

        product_data = request.data.dict()

        try:
            file = request.FILES[next(iter(request.FILES))]
            product_data.pop("image")
        except Exception:
            error_msg = {
                "detail": "It was not possible to create the product without an image"}
            return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

        category_obj = get_object_or_404(
            models.ProductCategory, id=product_data.get("category"))

        product_data.pop("category")

        new_product_values = ProductHandler(
            product_data).product_base_fields()

        new_product_values.pop("initial_stock")

        product_id = request.parser_context.get("kwargs").get("pk")

        if models.Product.objects.filter(pk=product_id).exists():

            models.Product.objects.filter(pk=product_id).update(
                main_color=new_product_values.get("main_color"),
                secondary_color=new_product_values.get("secondary_color"),
                brand=new_product_values.get("brand"),
                price=Decimal(new_product_values.get("price")),
                current_stock=int(new_product_values.get("current_stock")),
                url=f"product/{category_obj.name.title()}/{file}",
                description=f'{category_obj.name} {new_product_values.get("brand")} {new_product_values.get("main_color")}/{new_product_values.get("secondary_color")} {datetime.today().year}',
                category=category_obj
            )
        else:
            error_msg = {"detail": "Product not found."}
            return response.Response(data=error_msg, status=status.HTTP_404_NOT_FOUND)

        current_attribute_values = models.Product.objects.get(
            pk=product_id).product.all()

        new_attribute_values = ProductHandler(
            product_data).product_specific_fields()

        new_attributes = [new_attr.title() for new_attr,
                          new_val in new_attribute_values.items() if new_val]
        new_attributes.sort()

        current_attributes = [
            current_value.attribute.description.title() for current_value in current_attribute_values]
        current_attributes.sort()

        print(current_attribute_values)
        print(current_attributes)

        if new_attributes == current_attributes and len(new_attributes) == len(current_attributes):

            for attr, value in new_attribute_values.items():
                if value:

                    attribute_obj = get_object_or_404(
                        models.ProductAttribute, description__iexact=attr)

                    product_obj = models.Product.objects.get(pk=product_id)

                    product_obj.product.create(
                        value=value,
                        attribute=attribute_obj,
                        product=product_obj
                    )

            try:
                [current_attribute_value.delete()
                 for current_attribute_value in current_attribute_values]
            except Exception:
                error_msg = {
                    "detail": "It was not possible to delete the old attributes"}
                return response.Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(product_obj).data

            return response.Response(data=serializer, status=status.HTTP_200_OK)
