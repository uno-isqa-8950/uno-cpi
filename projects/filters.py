import django_filters
from projects.models import Project


class SearchProjectFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['project_name', 'academic_year']