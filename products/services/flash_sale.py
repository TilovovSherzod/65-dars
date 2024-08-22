from datetime import datetime, timedelta
from rest_framework import generics, serializers, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters import rest_framework as django_filters

from products.filters import FlashSaleFilter
from products.models import FlashSale, Product, ProductViewHistory


class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = ['id', 'product', 'discount_percentage', 'start_time', 'end_time']

    serializer_class = FlashSaleSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = FlashSaleFilter




@api_view(['get'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExists:
        return Response({'error': 'Product Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    """user bu productni oldin ko'rganligini tekshiramiz"""
    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists() #Bu yerda exist() ning vazifasi bolean javob qaytishini taminlash


    """Yaqinlashayotgan skidkani tekshiramiz"""
    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now() + timedelta(hours=24) #boshlanishiga 24 soat dan kam vaqt qolgan skidkalarni filtrlaydi
    ).first()            # first() -->  Filtrlangan datadan faqat bittasini qaytaradi


    """Agar user ko'rgan bo'lsa va skidka vaqti yaqinlashayotgan bo'lsa
    Yuqoridagi filtrlardan o'tib qaytgan productning atributlarini qaytarish uchun belgilaymiz:"""

    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time

        return Response({
            'message': f"This product will be on a {discount}% of flash sale!",
            'start_time': start_time,
            'end_time': end_time
        })
    else:
        return Response("No upcoming flash sales for this product!")



