# news/filters.py
import django_filters
from .models import News




class NewsFilter(django_filters.FilterSet):
    language = django_filters.CharFilter(method='filter_by_language')
    date_from = django_filters.DateFilter(field_name='published_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='published_at', lookup_expr='lte')
    
    class Meta:
        model = News
        fields = ['language', 'date_from', 'date_to']
    
    def filter_by_language(self, queryset, name, value):
        """Фильтрация по наличию перевода на указанный язык"""
        return queryset.filter(translations__language=value)