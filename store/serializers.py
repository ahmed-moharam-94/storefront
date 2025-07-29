from dataclasses import field
from decimal import Decimal

from pyexpat import model
from unittest import mock
from urllib import request
from wsgiref import validate
from rest_framework import serializers

from store.models import Customer, Product, Collection, Review

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'membership']




class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.SerializerMethodField(
        method_name='get_products_count'
    )

    def get_products_count(self, collection: Collection):
        print(f'featured:: {collection.featured_product}')
        return 0 if collection.featured_product == None else collection.featured_product.count()
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # featured_product = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(),
    #     allow_null=True
    # )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'inventory','price_with_tax', 'collection', 'collection_id']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
 
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_price_with_tax')
    collection_id = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        source='collection',
        write_only=True
    )

    collection = serializers.HyperlinkedRelatedField(
        # queryset = Collection.objects.all(),
        view_name = 'collection-detail',
        read_only = True
    )

    def calculate_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product' , 'customer', 'customer_id', 'description', 'date']

    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset = Customer.objects.all(),
        source = 'customer',
        write_only=True
    )

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)    
         
    
    # def validate(self, data):
    #     if data['password'] == data['confirm_password']:
    #         return data
    #     else:
    #         return serializers.ValidationError('Passwords doesn\'t match confirm password')


    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.description = 'This auto description'
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
