from decimal import Decimal


class ProductCreation:

    def __init__(self, product_dict):
        self.product_dict = product_dict

    def product_base_fields(self) -> dict:
        return dict(
            main_color=self.product_dict.get("main_color"),
            secondary_color=self.product_dict.get("secondary_color"),
            brand=self.product_dict.get("brand"),
            price=Decimal(self.product_dict.get("price")),
            initial_stock=int(self.product_dict.get("initial_stock")),
            current_stock=int(self.product_dict.get("current_stock"))
        )

    def product_specific_fields(self) -> list:
        data = self.product_base_fields()

        return {k: self.product_dict[k]
                for k in set(self.product_dict) - set(data)}
