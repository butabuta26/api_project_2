from django.urls import path, include
from .views import UserViewSet, RegisterViewSet, ResetPasswordViewSet, ResetPasswordConfirmViewSet
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('users', UserViewSet, basename='urls')
router.register('register', RegisterViewSet, basename='register')
router.register('reset_password', ResetPasswordViewSet, basename='reset_password')

urlpatterns = [
    path('', include(router.urls)),
    path('password_reset_confirm/<uidb64>/<token>', 
         ResetPasswordConfirmViewSet.as_view({'post': 'create'}), 
         name='password_reset_confirm')
]
