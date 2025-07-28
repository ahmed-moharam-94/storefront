from typing import Collection
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from store import serializers
from store.serializers import CollectionSerializer, ProductSerializer

# from store.serializers import ProductSerializer
from .models import OrderItem, Product, Collection

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            # Eager load 'collection' for GET requests
            return Product.objects.select_related('collection').all()
        # Use basic queryset for POST, PUT, DELETE
        return Product.objects.all()

    

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.get(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Can\'t delete this product because it\'t associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    
    # def delete(self, request, pk: int):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Can\'t delete this product because it\'t associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}
    
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer
    



# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             products, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(
#         data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# @api_view(['GET', 'POST'])
# def product_list(request: Request) -> Response | None:
#     if request.method == 'GET':
#         products = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             products, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(
#             data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # validated_data = serializer.validated_data
#         # print(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetails(APIView):

#     def get(self, request, id: int):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
    
#     def put(self, request, id: int):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(
#         product, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def delete(self, request, id: int):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Can\'t delete this product because it\'t associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        

# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'id'

#     def delete(self, request, pk: int):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Can\'t delete this product because it\'t associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(
#             product, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Can\'t delete this product because it\'t associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk: int):
        collection = get_object_or_404(Collection, pk=pk)
        # check if the collection is attached to a product
        if collection.product_set.count() > 0:
            return Response(data={'error': 'Can\'t delete this collection because it\'s associated with products'})
        collection.delete()
        return Response(data={'message': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer



# collections
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         collections = Collection.objects.all()
#         serializer = CollectionSerializer(collections, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk: int):
#         collection = get_object_or_404(Collection, pk=pk)
#         # check if the collection is attached to a product
#         if collection.product_set.count() > 0:
#             return Response(data={'error': 'Can\'t delete this collection because it\'s associated with products'})
#         collection.delete()
#         return Response(data={'message': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_details(request, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({
#             'message': 'Updated Successfully',
#             'data': serializer.data,
#         },
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'DELETE':
#         # check if the collection is attached to a product
#         if collection.product_set.count() > 0:
#             return Response(data={'error': 'Can\'t delete this collection because it\'s associated with products'})
#         collection.delete()
#         return Response(data={'message': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
