from django.urls import path, include
from products.views import ProductViewSet, ReviewViewSet, CartViewSet, ProductTagViewSet, FavoriteProductViewSet, ProductImageViewSet, CartItemViewSet
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('favorite_products', FavoriteProductViewSet)
router.register('tags', ProductTagViewSet)
router.register('cart', CartViewSet)
router.register('cart_items', CartItemViewSet, basename='cart-items')

products_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)

products_router.register('images', ProductImageViewSet)
products_router.register('reviews', ReviewViewSet)
products_router.register('tags', ProductTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
