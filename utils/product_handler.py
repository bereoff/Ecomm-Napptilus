from decimal import Decimal


class ProductHandler:

    def __init__(self, product_dict):
        self.product_dict = product_dict

    def product_base_fields(self) -> dict:
        return dict(
            main_color=self.product_dict.get("main_color"),
            secondary_color=self.product_dict.get("secondary_color"),
            brand=self.product_dict.get("brand"),
            price=Decimal(self.product_dict.get("price")),
            initial_stock=int(self.product_dict.get(
                "initial_stock")) if self.product_dict.get("initial_stock") else None,
            current_stock=int(self.product_dict.get("current_stock"))
        )

    def product_specific_fields(self) -> dict:
        data = self.product_base_fields()

        specific_fields = {k: self.product_dict[k]
                           for k in set(self.product_dict) - set(data)}

        # specific_fields.pop("category")

        return specific_fields
