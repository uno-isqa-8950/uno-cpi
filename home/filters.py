import django_filters
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, \
    ProjectCommunityPartner, ProjectMission


class ProjectFilter(django_filters.FilterSet):
    semester = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['semester', 'engagement_type']


class ProjectMissionFilter(django_filters.FilterSet):
    pass