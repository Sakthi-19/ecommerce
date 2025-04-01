from django.urls import path, include
from rest_framework import routers
from .views import (
    RegisterView, LoginView,
    CategoryViewSet, ProductViewSet,
    CartViewSet, OrderViewSet, CouponViewSet
)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'coupons', CouponViewSet, basename='coupons')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
