from rest_framework import serializers

from .models import Product, ProductAttribute, ProductCategory


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
