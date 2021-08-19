import django_filters as filters
from django_filters.rest_framework import FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    year = filters.NumberFilter(field_name="year")
    genre = filters.CharFilter(field_name="genre__slug")
    category = filters.CharFilter(field_name="category__slug")

    class Meta:
        model = Title
        fields = ["name", "genre", "category", "year"]
