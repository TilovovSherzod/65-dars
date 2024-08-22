from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from .filters import ProductFilter


class ReviewPagination(PageNumberPagination):  # Umumiy paginatsiyadan voris olib uning atributini  o'zimizga mosladik
    page_size = 3


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['name']


class ProductPagination(PageNumberPagination):
    page_size = 5


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]      # default = AllowAny
    pagination_class = ProductPagination

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']


    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
            })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:3]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        if reviews.count() == 0:
            return Response({'average_rating': 'No reviews yet'})
        average_rating = sum([review.rating for review in reviews]) / reviews.count()
        return Response({'average_rating': average_rating})



