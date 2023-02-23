import django_filters
from projects.models import Project


class SearchProjectFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter()

    class Meta:
        model = Project
        fields = ['project_name', 'engagement_type','academic_year','k12_flag',]
        labels = {
            'project_name': ('Project Name'),
            'academic_year': ('Academic Year'),
           }