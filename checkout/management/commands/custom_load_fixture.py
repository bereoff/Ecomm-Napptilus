import json
import os

from django.core.management import BaseCommand

from core import settings

from ...models import (Product, ProductAttribute, ProductAttributeValue,
                       ProductCategory)

base_dir = settings.BASE_DIR


class Command(BaseCommand):
    help = "clean database"

    def handle(self, *args, **kwargs):

        file_path = os.path.join(
            base_dir,
            "initial_fixture.json"
        )

        with open(file_path) as file:
            file_content = file.read()

        product_data = json.loads(file_content)

        category = []
        category_count = 0
        product = []
        product_count = 0
        product_attribute = []
        product_attribute_count = 0
        product_attribute_value = []
        product_attribute_value_count = 0

        for line in product_data:
            try:
                category_obj, category_created = ProductCategory.objects.get_or_create(
                    name=line.get("category_name")
                )
                if category_created:
                    category_count += 1
                category.append(("category", category_obj, category_created))
            except Exception as e:
                category.append(("category", line.get("category_id"), e))

            try:
                attribute_obj, attribute_created = ProductAttribute.objects.get_or_create(
                    description=line.get("product_attribute_description")
                )
                if attribute_created:
                    product_attribute_count += 1
                product_attribute.append(
                    ("attribute", attribute_obj, attribute_created))
            except Exception as e:
                category.append(
                    ("attribute", line.get("product_attribute_id"), e))

            try:
                product_obj, product_created = Product.objects.get_or_create(
                    main_color=line.get("product_main_color"),
                    secondary_color=line.get("product_secondary_color"),
                    brand=line.get("product_brand"),
                    price=line.get("product_price"),
                    initial_stock=line.get("product_initial_stock"),
                    current_stock=line.get("product_current_stock"),
                    description=line.get("product_description"),
                    url=line.get("product_url"),
                    category=category_obj
                )
                if product_created:
                    product_count += 1
                product.append(("product", product_obj, product_created))
            except Exception as e:
                product.append(("product", line.get("product_id"), e))

            try:
                if not ProductAttributeValue.objects.filter(pk=line.get("product_attribute_value_id")).exists():

                    product_attribute_value_obj, attribute_value_created = ProductAttributeValue.objects.get_or_create(
                        product=product_obj,
                        attribute=attribute_obj,
                        value=line.get("product_attribute_value_value")
                    )
                else:
                    product_attribute_value_obj = ProductAttributeValue.objects.filter(
                        pk=line.get("product_attribute_value_id")).first()
                    attribute_value_created = False

                    if attribute_value_created:
                        product_attribute_value_count += 1

                    product_attribute_value.append("attribute value",
                                                   (product_attribute_value_obj, attribute_value_created))

            except Exception as e:
                product_attribute_value.append(
                    ("attribute value", line.get("product_attribute_value_id"), e))

        # print("Total category objects created:", category_count)
        # print("Total attribute objects created:", product_attribute_count)
        # print("Total product objects created:", product_count)
        # print("Total attribute values objects created:",
        #       product_attribute_value_count)

        total = category_count + product_attribute_count + \
            product_count + product_attribute_value_count
        print("Total fixture created:", total)
