from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Count, DecimalField, ExpressionWrapper, Min, Max, Sum, Avg, Value, Func
from django.db.models.functions import Concat
from django.db import transaction, connection
from store.models import Customer, Product, OrderItem, Order, Collection
from tags.models import Tag, TaggedItem


# @transaction.atomic()
def say_hello(request):
    # query_set = Product.objects.all()
    # query_set = query_set.filter().filter().filter().order_by()

    # product = Product.objects.get(pk=-1)

    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt= 20))

    # query_set = Product.objects.filter(inventory=F('unit_price'))

    # query_set = Product.objects.order_by('-title')

    # query_set = Product.objects.values_list('id', 'title', 'collection__title')

    # get the order products ids
    # order_products_ids_queryset = OrderItem.objects.values('product_id').distinct()

    # query_set = Product.objects.filter(pk__in=order_products_ids_queryset).order_by('title')

    # query_set = Product.objects.defer('description')

    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # get the last 5 orders
    # query_set = Order.objects.select_related('customer').order_by('-placed_at')[:5].prefetch_related('orderitem_set__product').all()

    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))

    # number of orders
    result = Order.objects.aggregate(count=Count('id'))

    # how many units of product 1 we have sold
    result = OrderItem.objects.filter(
        product__id=1).aggregate(count=Sum('quantity'))

    # how many orders has customer 1 placed
    result = Order.objects.filter(customer__id=1).aggregate(count=Count('id'))

    result = Order.objects.filter(customer__id=1).count()

    # min, max, avg prices in products in collection 3
    result = Product.objects.filter(collection__id=3).aggregate(
        min=Min('unit_price'), max=Max('unit_price'), avg=Avg('unit_price'))

    query_set = Customer.objects.annotate(new_id=F('id') + 4)

    query_set = Customer.objects.annotate(full_name=Func(
        'first_name', Value(' '), 'last_name', function='Concat'))

    query_set = Concat('first_name', Value(' '), 'last_name')

    query_set = Customer.objects.annotate(orders_count=Count('order'))

    discounted_price_wrapper = ExpressionWrapper(
        F('unit_price') * 0.80, output_field=DecimalField())
    query_set = Product.objects.annotate(
        discounted_price=discounted_price_wrapper)

    # Query models with content type
    # first get the content type
    content_type = ContentType.objects.get_for_model(Product)
    # second get the tag based on product & tagged item
    # query_set = TaggedItem.objects\
    #     .select_related('tag').\
    #     filter(content_type=content_type, object_id=1)
    
    # create custom manager
    query_set = TaggedItem.objects.get_tag_for(obj_type=Product, obj_id=1) 


    collection = Collection.objects.get(pk=1)
    collection.featured_product = Product(pk=1)
    collection.save()

    Collection.objects.filter(pk=1).update(featured_product_id=2)

    # Collection.objects.create(title='test', featured_product_id=1)

    
    collection = Collection(pk=11)
    collection.delete()


    Collection.objects.filter(id__in=[8,9,10]).delete()

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        order_item = OrderItem()
        order_item.order = order
        order_item.product = Product(pk=1)
        order_item.quantity = 1
        order_item.unit_price = 10.00


        # executing raw sql queries using model objects
        Product.objects.raw('SELECT * FROM store_product')

        # executing raw sql queries using a cursor 
        # always use try finally block to make sure the connection is closed
        try:
            cursor = connection.cursor()
            data = cursor.execute('SELECT * FROM store_product')
            print(data)
            query_set =cursor.fetchall()
            # close the cursor after finishing
        finally:
            cursor.close()


        # using with block so we don't need to manually close the connection
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM store_product')
        

    query_set = Order.objects.annotate(products_count=Count('orderitem_set'))

    return render(request, 'hello.html', {'name': 'Mosh', 'result': list(query_set)})
