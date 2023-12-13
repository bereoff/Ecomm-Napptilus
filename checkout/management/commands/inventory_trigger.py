from datetime import datetime

from django.core.management import BaseCommand
from django.db.models import Count

from api.email_api.send_email import PromptEmail, report_email_sending
from checkout.views import SENDGRID_API_KEY
from core import settings

from ...models import CartProduct, Product

base_dir = settings.BASE_DIR

email = "bbereoff@gmail.com"


class Command(BaseCommand):
    help = "clean database"

    def handle(self, *args, **kwargs):
        report = []
        products_in_carts = CartProduct.objects.all().values(
            "product").annotate(total=Count("product")).order_by("product")

        products_in_stock = Product.objects.filter(
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
            report_email_sending(email, SENDGRID_API_KEY)
            prompt_email = PromptEmail.send_prompt_email_report(email)
            print(prompt_email)
        except Exception as e:
            print(e)
