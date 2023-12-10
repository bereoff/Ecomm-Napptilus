from django.db.models import (CASCADE, CharField, DateTimeField, DecimalField,
                              ForeignKey, ImageField, IntegerField, Manager,
                              ManyToManyField, Model, TextField)

from base_model.db import BaseUUIDModel, DefaultModel


class ProductCategory(DefaultModel):
    name = CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.pk}-{self.name}"


class NotDeletedProducts(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Product(BaseUUIDModel):
    main_color = CharField(max_length=255, blank=True, null=True)
    secondary_color = CharField(max_length=255, blank=True, null=True)
    brand = CharField(max_length=255, blank=True, null=True)
    price = DecimalField(max_digits=15, decimal_places=4,
                         blank=True, null=True)
    initial_stock = IntegerField(blank=True, null=True)
    current_stock = IntegerField(blank=True, null=True)
    description = CharField(max_length=255, blank=True, null=True)
    category = ForeignKey(
        ProductCategory, related_name="category", on_delete=CASCADE)

    def product_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
        return f"product/{self.category.name}/{filename}"

    url = ImageField(upload_to=product_directory_path, blank=True, null=True)

    objects_with_deleted = Manager()  # The default manager.
    objects = NotDeletedProducts()  # Only Product Not Deleted


class ProductAttribute(DefaultModel):
    description = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk}-{self.description}"


class ProductAttributeValue(DefaultModel):
    product = ForeignKey(Product, related_name="product", on_delete=CASCADE)
    attribute = ForeignKey(
        ProductAttribute, related_name="attribute", on_delete=CASCADE)
    value = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk}-{self.value}"


class Cart(Model):
    PENDING = 'pending'
    PURCHASED = 'purchased'

    CHOICES_STATE = (
        (PENDING, 'Pending'),
        (PURCHASED, 'Purchased')
    )
    created_at = DateTimeField(
        auto_created=True, editable=False, auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True, db_index=True)
    session_id = CharField(max_length=255, null=True, blank=True)
    state = CharField(choices=CHOICES_STATE, max_length=30, default=PENDING)
    products = ManyToManyField(
        Product, related_name='products_cart', through='CartProduct')

    def __str__(self):
        return f"{self.session_id}-{self.created_at.today()}"


class CartProduct(Model):
    created_at = DateTimeField(
        auto_created=True, editable=False, auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True, db_index=True)
    product = ForeignKey(
        Product, related_name="product_interm_cart", on_delete=CASCADE)
    cart = ForeignKey(
        Cart, related_name="cart_interm_product", on_delete=CASCADE)
