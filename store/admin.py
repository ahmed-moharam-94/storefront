from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

from tags.models import Tag, TaggedItem
from . import models


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}"> {} </a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))

###############



class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 20
    list_select_related = ['collection']
    search_fields = ['title']
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['clear_inventory']
    



    # fields = ['title', 'slug']
    # exclude = ['promotions']
    # readonly_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection']


    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'Low' if product.inventory < 10 else 'OK'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were updated', messages.ERROR)


admin.site.register(models.Product, ProductAdmin)

################


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 50

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({'customer__id': str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))

################

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    max_num = 10
    min_num = 1
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

