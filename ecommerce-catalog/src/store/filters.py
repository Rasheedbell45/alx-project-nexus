import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr='iexact')
    in_stock = django_filters.BooleanFilter(field_name="in_stock")

    class Meta:
        model = Product
        fields = ['category', 'in_stock', 'min_price', 'max_price', 'title']
