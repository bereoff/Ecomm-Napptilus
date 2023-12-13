from dj_rql.filter_cls import AutoRQLFilterClass, FilterLookups
from django.db.models import Q

from . import models


class ProductFilters(AutoRQLFilterClass):
    MODEL = models.Product
    FILTERS = (
        {
            'filter': 'product_id',
            'source': 'id',
            'ordering': True
        },
        {
            'filter': 'available',
            'source': 'is_deleted',
            'ordering': True
        },
        {
            'filter': 'category_name',
            'lookups': {FilterLookups.EQ, FilterLookups.IN},
            'custom': True,
            'ordering': True
        },
        {
            'filter': 'product_color',
            'lookups': {FilterLookups.EQ, FilterLookups.IN},
            'custom': True,
            'ordering': True
        },

    )

    def build_q_for_custom_filter(self, data):
        if data.filter_name == 'product_color':
            return (
                Q(main_color__icontains=data.str_value
                  ) | Q(secondary_color__icontains=data.str_value)
            )
        elif data.filter_name == 'category_name':
            return Q(category__name__icontains=data.str_value)
