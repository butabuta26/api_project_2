from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .permissions import IsObjectOwnerReadOnly
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from .models import Cart, ProductTag, FavoriteProduct, Product, Review, ProductImage, CartItem
from .serializers import (CartSerializer, ProductTagSerializer,
                          FavoriteProductSerializer, ProductSerializer, ReviewSerializer, ProductImageSerializer, CartItemSerializer)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .pagination import ProductPagination

from products.filters import ProductFilter, ReviewFilter
from rest_framework.exceptions import PermissionDenied

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle

from rest_framework.parsers import MultiPartParser, FormParser
import time

class ProductViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Product.objects.all().prefetch_related('tags', 'reviews')
    serializer_class = ProductSerializer 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = ProductPagination
    throttle_classes = [UserRateThrottle]
    # filterset_fields = ['price', 'categories__name']
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    
    # def get_serialized_data(self):
    #     cache_key = 'products_list'
    #     data = cache.get(cache_key)
        
    #     if data:
    #         return data
        
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     cache.set(cache_key, serializer.data, 60*5)
    #     return serializer.data 
    
    # def list(self, request, *args, **kwargs):
    #     start = time.time()
    #     data = self.get_serialized_data()
    #     end = time.time()
    #     print(end-start)
    #     return Response(data)
        
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    # def perform_update(self, serializer):
    #     review = self.get_object()
    #     print(review.user, self.request.user, "-"*10)
    #     if review.user != self.request.user:
    #         raise PermissionDenied("You can't change this review")
    #     serializer.save()
        
    # def perform_destroy(self, instance):
    #     if instance.user != self.request.user:
    #         raise PermissionDenied("You can't delete this review")
    #     instance.delete()
    
class FavoriteProductViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = FavoriteProductSerializer
    queryset = FavoriteProduct.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'likes'
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
class CartViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)

    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review.")
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this item.")
        serializer.save()
    
class ProductTagViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ProductTagSerializer
    queryset = ProductTag.objects.all()
    permission_classes = [IsAuthenticated]
    
class ProductImageViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])