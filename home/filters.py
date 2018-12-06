import django_filters
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, \
    ProjectCommunityPartner, ProjectMission
from partners.models import CommunityPartner, CommunityPartnerMission
from home.models import MissionArea

class ProjectFilter(django_filters.FilterSet):
    legislative_district = django_filters.ModelChoiceFilter(
        queryset=Project.objects.values_list('legislative_district', flat=True).distinct())
    class Meta:
        model = Project
        fields = ['engagement_type','academic_year','legislative_district', ]


class legislativeFilter(django_filters.FilterSet):

   legislative_district = django_filters.ModelChoiceFilter(queryset=Project.objects.values_list('legislative_district', flat=True).distinct())

   # legislative_district =   django_filters.NumberFilter('legislative_district')

   class Meta:
        model = Project
        fields = ['legislative_district',]



class ProjectMissionFilter(django_filters.FilterSet):
    class Meta:
        model = ProjectMission
        fields = ['mission', ]


class AcademicYearFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = ['academic_year', ]


class ProjectCampusFilter(django_filters.FilterSet):

    class Meta:
        model = ProjectCampusPartner
        fields = ['campus_partner', ]


class communityPartnerFilter(django_filters.FilterSet):

    class Meta:
        model = CommunityPartner
        fields = ["weitz_cec_part", "community_type"]


class CommunityMissionFilter(django_filters.FilterSet):

    class Meta:
        model = CommunityPartnerMission
        fields = ["community_partner"]


class MissionAreaFilter(django_filters.FilterSet):

    class Meta:
        model = MissionArea
        fields = ["mission_name"]
