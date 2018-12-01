import django_filters
from projects.models import Project


class SearchProjectFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter()

    class Meta:
        model = Project
        fields = ['project_name', 'academic_year']
        labels = {
            'project_name': ('Project Name'),
            'academic_year': ('Academic Year'),
           }