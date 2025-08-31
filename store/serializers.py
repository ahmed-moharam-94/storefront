from ast import Delete
from dataclasses import field, fields
from decimal import Decimal
from pyexpat import model
from tkinter import TRUE
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from core.admin import User
from likes.models import LikedItem
from rest_framework import serializers


from store.signals import order_created
from store.models import CartItem, Customer, Order, OrderItem, Product, Collection, Review, Cart, ProductImage



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

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return ProductImage.objects.create(product_id=self.context['product_id'], **validated_data)
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'inventory',
                  'price_with_tax', 'collection', 'collection_id', 'images']
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
        view_name='collection-detail',
        read_only=True
    )

    def calculate_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'customer',
                  'customer_id', 'description', 'date']

    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class UpdateCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
    )

    def save(self, **kwargs):
        # check if the product exist in the cart item then update else create
        print("Serializer context:", self.context)

        cart_id = self.context.get('cart_id')
        product = self.validated_data.get('product')
        quantity = self.validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product.id)
            # update the cart item
            cart_item.quantity += quantity
            cart_item.save()
            ################ IMPORTANT: always update self.instance & return self.instance #######################
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # create a new cart item with the given product and quantity
            # CartItem.objects.create(cart_id=cart_id, quantity=quantity, product_id=product_id)
            cart_item = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
            self.instance = cart_item
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='calculate_total_price'
    )

    def calculate_total_price(self, cartItem: CartItem):
        return cartItem.quantity * cartItem.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product',  'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    # id should be read only because client side should call a POST request to create a Cart and
    # id is generated in the server side
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField(
        method_name='calculate_cart_total_price',
        read_only=True,
    )

    def calculate_cart_total_price(self, cart: Cart):
        return sum(item.product.unit_price * item.quantity for item in cart.items.all())

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

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


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='calculate_order_items_total_price'
    )

    def calculate_order_items_total_price(self, orderItem: OrderItem):
        return orderItem.quantity * orderItem.unit_price

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(
        method_name='calculate_order_total_price',
    )

    def calculate_order_total_price(self, order: Order):
        return sum(item.quantity * item.unit_price for item in order.items.all())

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status',
                  'customer', 'items', 'total_price',
                  ]

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

 # validate if the cart exists and if the cart is not empty
    def validate_cart_id(self, cart_id):
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            # This catches the case where the cart doesn't exist
            raise serializers.ValidationError('No cart with this id was found.')

        if cart.items.count() == 0:
            # This checks if the existing cart is empty
            raise serializers.ValidationError('The cart is empty.')

        return cart_id
    
    

    def save(self, **kwargs):
        # make sure that all save methods even success together or non 
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(
                user_id=self.context['user_id'])

            # create order at first with the given customer
            order = Order.objects.create(customer=customer)

            # get cart items and create order items depending on cart items
            cart_items = CartItem.objects\
                .select_related('product')\
                .filter(cart_id=cart_id)

            # map cart items to order items
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price
                ) for item in cart_items
            ]

            # create order items
            OrderItem.objects.bulk_create(order_items)

            # delete cart 
            Cart.objects.get(pk=cart_id).delete()

            # fire order_created signal
            order_created.send_robust(self.__class__, order=order)
            # return order to use it in view create method
            return order
        


# because we have a custom implementation to create method
# we will extend from Serializer and not ModelSerializer
class LikeProductSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    def save(self, **kwargs):
        user = self.context['request'].user
        product = self.validated_data['product_id']

        # get the product content type
        product_content_type = ContentType.objects.get_for_model(Product)

        # check if the user has liked this product
        already_liked = user.likeditem_set.filter(object_id=product.id).exists()

        if already_liked:
            # delete the liked item
            liked_item = LikedItem.objects.filter(user=user, object_id=product.id)
            liked_item.delete()
            return None
        else:
            # create a liked item
            liked_item = LikedItem.objects.create(user=user, content_type=product_content_type, object_id=product.id)
            return liked_item
        

class LikedItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(
        method_name='get_product',
    )

    # get the liked item and then get the product object
    def get_product(self, liked_item: LikedItem):
        # check if the content object exists and is a product instance
        if liked_item.content_object and isinstance(liked_item.content_object, Product):
            # if it exists serialize it and return it's data
            return ProductSerializer(liked_item.content_object, context=self.context).data
        return None


    class Meta:
        model = LikedItem
        fields = ['product']
        read_only_fields = ['product']


class CustomerLikesSerializer(serializers.ModelSerializer):
    liked_items = serializers.SerializerMethodField()

    def get_liked_items(self, customer:Customer):
        # get the user by customer id
        user = customer.user

        # get the customer likeditem_set 
        # eager load content object
        liked_item_queryset = user.likeditem_set.all().prefetch_related('content_object')
        # return the serializer data not the serializer it self
        return LikedItemSerializer(liked_item_queryset, many=True, context=self.context).data
    

    class Meta:
        model = Customer
        fields = ['liked_items']
        read_only_fields = ['liked_items']