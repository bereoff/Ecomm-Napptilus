from rest_framework import serializers

from .models import Product


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
