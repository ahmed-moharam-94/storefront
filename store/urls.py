from codecs import lookup
from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

# pass the parent router, parent prefix, lookup parameter ex: (product_pk) to tell nested router how to look in parent (products)
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# register child resource: prefix, ViewSet, basename (the prefix that will be used to generate the nested route ex: product-reviews-list, product-reviews-detail)
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')


# URLConf
urlpatterns = router.urls + products_router.urls
