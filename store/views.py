from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from store import serializers
from store.serializers import ProductSerializer

# from store.serializers import ProductSerializer
from .models import Product


@api_view(['GET', 'POST'])
def product_list(request: Request) -> Response | None:
    if request.method == 'GET':
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        validated_data = serializer.validated_data
        print(validated_data)
        return Response('OK')
     


@api_view()
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)


@api_view()
def collection_details(request, pk):
    return Response('OK')
