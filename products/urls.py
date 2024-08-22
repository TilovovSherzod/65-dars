from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .services.flash_sale import FlashSaleListCreateView, check_flash_sale
from .services.product_view_history import ProductViewHistoryCreate
from .views import *


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('check-sale/<int:product_id>', check_flash_sale, name='check_flash_sale'),
    path('product-view', ProductViewHistoryCreate.as_view(), name='sale'),
]

