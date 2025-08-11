from logging import raiseExceptions
from typing import Collection
from urllib import request
from venv import logger
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, DjangoModelPermissions
from .permissions import FullDjangoModelPermission, IsAdminOrReadOnlyPermission, OrderCreatedByThisCustomer, ViewCustomerHistoryPermission

from store import serializers
from store.pagination import DefaultPagination
from .filters import ProductFilter
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderItemSerializer, OrderSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer

# from store.serializers import ProductSerializer
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        # check if the product exists
        get_object_or_404(Product, pk=product_id)
        return Review.objects.filter(product_id=product_id).select_related('customer')

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk'], 'request': self.request}


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnlyPermission]

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            queryset = Product.objects.select_related('collection').all()
            # collection_id = self.request.query_params.get('collection_id')
            # if collection_id is not None:
            #     queryset = queryset.filter(collection_id=collection_id)
            # Eager load 'collection' for GET requests
            return queryset
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
    # set pagination class to None to return all collections without pagination
    pagination_class = None
    permission_classes = [IsAdminOrReadOnlyPermission]

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


# create a custom view set because here we don't need the ListModelMixin nor the UpdateModelMixin
# all we need is POST(CreateModelMixin), GET item(RetrieveModelMixin) & DELETE(DestroyModelMixin)
# also we need to extend GenericViewSet although it doesn't have any actions but it the base set of generic view behavior, such as the `get_object` and `get_queryset` methods.
class CartViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


# We need to list, retrieve cart items, update, delete so extend the ModelViewSet
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk'), 'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer

        else:
            return CartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs.get('cart_pk')
        # check if the cart exists
        get_object_or_404(Cart, pk=cart_id)
        return CartItem.objects.select_related(
            'product').filter(cart_id=cart_id)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        # xxxxxx use get_or_create so if we create a user without a profit it create it to us
        # use signals
        (customer, created) = Customer.objects.select_related('user').get(
            user_id=request.user.id)
        if request.method == 'GET':
            # serialize the customer object
            serializer = CustomerSerializer(customer)
        elif request.method == 'PATCH':
            serializer = CustomerSerializer(customer, data=request.data)
            # validate incoming data
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('OK')


# class OrderItemViewSet(ModelViewSet):
#     queryset = OrderItem.objects.select_related('product').all()
#     serializer_class = OrderItemSerializer()
#     # permission_classes = []


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    # eager loading for products
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]

        if self.action == 'list':
            if self.request.user.is_staff:
                return [IsAuthenticated(), IsAdminUser()]
            else:
                # non admin users should be able to list orders put they will only get there orders
                # check the override of the get_queryset
                return [IsAuthenticated()]

        if self.action == 'retrieve':
            return [IsAuthenticated(), OrderCreatedByThisCustomer()]

        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        # check if the user is admin then get all orders
        if self.request.user.is_staff:
            return Order.objects.select_related('customer').prefetch_related('items__product').all()

        # if the user is not admin only get his orders
        customer_id = Customer.objects.only(
            'id').get(user_id=self.request.user.id)

        return Order.objects.prefetch_related('items__product').filter(customer_id=customer_id).all()

    def list(self, request, *args, **kwargs):
        orders = self.get_queryset()
        serializer = self.get_serializer(
            orders, many=True, context={'request': request})
        return Response({'orders': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={
                                           'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
