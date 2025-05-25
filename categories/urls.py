from django.urls import path, include
from .views import CategoryViewSet, CategroryDetailViewSet, CategoryImageViewSet
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('categories',CategoryViewSet)

categories_router = routers.NestedDefaultRouter(
    router,
    'categories',
    lookup='category'
)

categories_router.register('details', CategroryDetailViewSet)
categories_router.register('images', CategoryImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
]