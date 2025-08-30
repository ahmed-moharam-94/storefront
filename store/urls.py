from codecs import lookup
from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
# basename must be defined if you override def get_queryset()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

############### Nested Routers ################
# products nested routes
# pass the parent router, parent prefix, lookup parameter ex: (product_pk) to tell nested router how to look in parent (products)
# products/{product_pk}/  for a detail view
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# register child resource: prefix, ViewSet, basename (the prefix that will be used to generate the nested route ex: product-reviews-list, product-reviews-detail)
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-images')

# carts nested routes
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
# when call /items/ in cart url it will use CartItemViewSet & will generate the basename(list, detail) cart-items-list, cart-items-detail 
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


# URLConf
urlpatterns = [
    path('products/like/', views.LikeProductApiView.as_view(), name='like-product'),
] + router.urls + products_router.urls + carts_router.urls
