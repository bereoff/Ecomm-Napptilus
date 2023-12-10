import os

from rest_framework import serializers

from .models import Product, ProductAttribute, ProductCategory

APP_DOMAIN = os.environ.get('APP_DOMAIN')


class ProductSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('initial_stock', )

    def get_attributes(self, obj):
        attrs = obj.product.all()
        attributes_list = list()

        for attr in attrs:
            attribute = attr.attribute.description
            value = attr.value
            pair = {f"{attribute}": f"{value}"}
            attributes_list.append(pair)

        return attributes_list


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="pk")
    quantity = serializers.SerializerMethodField()
    image_url = serializers.CharField(source="url")

    class Meta:
        model = Product
        fields = ["product_id", "description",
                  "quantity", "price", "image_url"]

    def get_quantity(self, obj):
        quantity = obj.product_interm_cart.all().count()
        return quantity

    def to_representation(self, instance):
        data = super(ProductCartSerializer, self).to_representation(instance)
        url = data.get("image_url")
        data.pop("image_url")
        data.update({"image_url": str(APP_DOMAIN) + "media/" + str(url)})
        return data
