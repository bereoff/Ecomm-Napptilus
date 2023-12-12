import logging

from django.core.management import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from ...models import (Cart, CartProduct, Product, ProductAttribute,
                       ProductAttributeValue, ProductCategory)


class Command(BaseCommand):
    help = 'clean database'

    def handle(self, *args, **kwargs):

        ProductCategory.objects.all().delete()
        CartProduct.objects.all().delete()
        Product.objects_with_deleted.all().delete()
        ProductAttribute.objects.all().delete()
        ProductAttributeValue.objects.all().delete()
        Cart.objects.all().delete()

        try:
            sequence_sql = connection.ops.sequence_reset_sql(
                no_style(), [ProductCategory, CartProduct, ProductAttribute, ProductAttributeValue, Cart])
            with connection.cursor() as cursor:
                for sql in sequence_sql:
                    cursor.execute(sql)
        except Exception as e:
            logging.error(e)
