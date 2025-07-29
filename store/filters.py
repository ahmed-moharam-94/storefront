from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        # define what fields you want to use as filters
        fields = {
            'collection_id': ['exact'], # define a list to describe how filters can work
            'unit_price': ['gt', 'lt']
        }