from django.utils import timezone
from django_filters import rest_framework as django_filters  #pip install django-filters
from .models import Product, FlashSale
from django.db.models import Q

class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # min_rating = django_filters.NumberFilter(field_name='reviews__rating', lookup_expr='gte')
    # max_rating = django_filters.NumberFilter(field_name='reviews__rating', lookup_expr='lte') # bu filter ishladi ammo logik xato ekan

    class Meta:
        model = Product
        fields = ['category', 'max_price', 'min_price']



class FlashSaleFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(method='filter_is_active')
    max_discount = django_filters.NumberFilter(field_name='discount_percentage', lookup_expr='lte')
    min_discount = django_filters.NumberFilter(field_name='discount_percentage', lookup_expr='gte')

    def filter_is_active(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(start_time__lte=now, end_time__gte=now)
        else:
            return queryset.filter(Q(start_time__gt=now) | Q(end_time__lt=now))

    class Meta:
        model = FlashSale
        fields = ['is_active', 'max_discount', 'min_discount']
