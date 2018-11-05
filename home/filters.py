import django_filters
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, \
    ProjectCommunityPartner, ProjectMission
from partners.models import CommunityPartner


class ProjectFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = ['semester', 'engagement_type']


class ProjectMissionFilter(django_filters.FilterSet):

    class Meta:
        model = ProjectMission
        fields = ['mission', ]

class SemesterFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = ['semester', ]


class communityPartnerFilter(django_filters.FilterSet):

    class Meta:
        model = CommunityPartner
        fields = ["weitz_cec_part"]

