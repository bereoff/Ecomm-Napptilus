import json
import os
from datetime import datetime
from decimal import Decimal

from django.db.models import Case, Count, IntegerField, When
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status, views
from rest_framework.exceptions import APIException, ParseError

from utils.product_handler import ProductHandler

from . import filters, models
from .serializers import (ProductAttributeSerializer, ProductCartSerializer,
                          ProductCategorySerializer, ProductSerializer)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


class ListProductView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    rql_filter_class = filters.ProductFilters

    def get_queryset(self):
        return models.Product.objects.annotate(
            custom_order=Case(
                When(category__name__iexact="Cap", then=1),
                output_field=IntegerField())
        ).order_by("custom_order", "-created_at")


class ProductCategoryView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductAttributeView(generics.ListAPIView):
    queryset = models.ProductAttribute.objects.all().order_by(
        "-created_at", "description")
    serializer_class = ProductAttributeSerializer


class NewProductView(views.APIView):
    def post(self, request):
        try:
            product_data = request.data.dict()
        except ParseError as e:
            return e

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

        try:
            product_data = request.data.dict()
        except ParseError as e:
            return e

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


class ProductSoftDeleteView(views.APIView):
    def put(self, request):

        try:
            product_data = json.loads(request.body)
        except APIException as e:
            return e

        products = list()
        for product in product_data:
            product_id = product.get("product_id")
            product_state = product.get("is_deleted")

            try:
                models.Product.objects.get(pk=product_id)
            except models.Product.DoesNotExist:
                raise Http404

            product_obj = models.Product.objects.filter(
                pk=product_id).update(is_deleted=product_state)

            products.append(product_obj)

        return response.Response(status=status.HTTP_200_OK)


class ProductHardDeleteView(generics.DestroyAPIView):
    queryset = models.Product.objects_with_deleted.all()
    serializer_class = ProductSerializer


class ListCartView(views.APIView):

    def get(self, request):
        try:
            session_id = request.COOKIES["session_id"]
        except Exception:
            session_id = "Z4z9rppEXqNYLEJKWaG9ifs4Wiq8sR"

        cart = models.Cart.objects.filter(
            session_id=session_id, state=models.Cart.PENDING)

        if not cart.exists():
            return response.Response(data=list(), status=status.HTTP_200_OK)

        products = cart.first().products.all()

        total_products = cart.first().cart_interm_product.count()

        serializer = ProductCartSerializer(products, many=True).data

        return response.Response(data={"products": serializer, "total": total_products}, status=status.HTTP_200_OK)


class AddProductCartView(views.APIView):
    def post(self, request):

        try:
            session_id = request.COOKIES["session_id"]
        except Exception:
            session_id = "Z4z9rppEXqNYLEJKWaG9ifs4Wiq8sR"

        try:
            product_data = json.loads(request.body)
        except APIException as e:
            return e

        product_id = product_data.get("product_id")
        product_quantity = product_data.get("quantity")

        try:
            product_obj = models.Product.objects_with_deleted.get(
                pk=product_id)

            if product_obj.is_deleted:
                msg = "Product no longer available."
                return response.Response(data={"detail": msg}, status=status.HTTP_200_OK)

        except models.Product.DoesNotExist:
            error_msg = {"detail": "Product not found."}
            return response.Response(data=error_msg, status=status.HTTP_404_NOT_FOUND)

        if models.Cart.objects.filter(session_id=session_id,
                                      state=models.Cart.PENDING,
                                      created_at__date=datetime.today().date()
                                      ).exists():

            cart = models.Cart.objects.get(session_id=session_id,
                                           state=models.Cart.PENDING,
                                           created_at__date=datetime.today().date()
                                           )

            if product_obj.current_stock > 0:
                while product_quantity > 0 and product_obj.current_stock > 0:
                    models.CartProduct.objects.create(
                        product=product_obj, cart=cart)
                    product_obj.current_stock -= 1
                    try:
                        product_obj.save()
                    except Exception as e:
                        raise e

                    product_quantity -= 1
            else:
                msg = "Out of stock."
                return response.Response(data={"detail": msg}, status=status.HTTP_200_OK)

        else:
            if product_obj.current_stock > 0:
                cart = product_obj.products_cart.create(
                    session_id=session_id)
                product_obj.current_stock -= 1
                product_obj.save()
                product_quantity -= 1
                while product_quantity > 0 and product_obj.current_stock > 0:
                    models.CartProduct.objects.create(
                        product=product_obj, cart=cart)
                    product_obj.current_stock -= 1
                    product_obj.save()
                    product_quantity -= 1
            else:
                msg = "Out of stock."
                return response.Response(data={"detail": msg}, status=status.HTTP_200_OK)

        return response.Response(status=status.HTTP_200_OK)


class CartPurchasedView(views.APIView):
    def post(self, request):
        from api.email_api.send_email import (PromptEmail,
                                              purchase_email_sending)

        try:
            customer_data = json.loads(request.body)
        except APIException as e:
            return e

        prompt_email = PromptEmail(customer_data)

        try:
            session_id = request.COOKIES["session_id"]
        except Exception:
            session_id = "Z4z9rppEXqNYLEJKWaG9ifs4Wiq8sR"

        cart = get_object_or_404(models.Cart, session_id=session_id,
                                 state=models.Cart.PENDING,
                                 created_at__date=datetime.today().date())
        try:
            cart.state = models.Cart.PURCHASED
            cart.save()
        except Exception:
            msg = "Out of stock."
            return response.Response(data={"detail": msg}, status=status.HTTP_200_OK)

        try:

            if SENDGRID_API_KEY is not None:
                purchase_email_sending(customer_data, SENDGRID_API_KEY)
                print(prompt_email.send_prompt_email_purchase())
            else:
                print(prompt_email.send_prompt_email_purchase())
        except Exception as e:
            print(e)

        return response.Response(status=status.HTTP_200_OK)


class ProductInventoryAccuracyView(views.APIView):
    def put(self, request):
        from api.email_api.send_email import PromptEmail, report_email_sending

        try:
            email = request.data.get("analyst_email")
        except ParseError as e:
            return e

        report = []
        products_in_carts = models.CartProduct.objects.all().values(
            "product").annotate(total=Count("product")).order_by("product")

        products_in_stock = models.Product.objects.filter(
            pk__in=[product.get("product") for product in products_in_carts]).order_by("id")

        for product_in_cart, product_in_stock in zip(products_in_carts, products_in_stock):

            product_cart = product_in_cart.get("product")
            total_in_cart = product_in_cart.get("total")

            product_stock = product_in_stock.id

            if product_cart == product_stock:
                if product_in_stock.initial_stock == (product_in_stock.current_stock + total_in_cart):
                    report.append(
                        dict(
                            product=product_in_stock.id,
                            description=product_in_stock.description,
                            actual_stock=product_in_stock.current_stock,
                            total_purchased=total_in_cart,
                            status="in compliance",
                            report_date=datetime.now()
                        )
                    )
                else:
                    report.append(
                        dict(
                            product=product_in_stock.id,
                            description=product_in_stock.description,
                            actual_stock=product_in_stock.current_stock,
                            total_purchased=total_in_cart,
                            status="non-compliance",
                            report_date=datetime.now()
                        )
                    )
        try:
            if SENDGRID_API_KEY is not None:
                report_email_sending(email, SENDGRID_API_KEY)
                prompt_email = PromptEmail.send_prompt_email_report()
                print(prompt_email)
            else:
                prompt_email = PromptEmail.send_prompt_email_report()
                print(prompt_email)
        except Exception as e:
            print(e)

        return response.Response(data={"report": report}, status=status.HTTP_200_OK)
