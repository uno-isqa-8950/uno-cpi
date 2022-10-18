import django_filters
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, \
    ProjectCommunityPartner, ProjectMission, ProjectSubCategory
from partners.models import CommunityPartner, CommunityPartnerMission, CampusPartner
from home.models import MissionArea
from django.db.models import Max, Min

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['engagement_type','academic_year','end_academic_year'  ]
    @property
    def qs(self):
        parent = super(ProjectFilter, self).qs
        x = ''
        y = ''
        if ('academic_year' in self.data.keys()):
            x = self.data['academic_year']
        if ('engagement_type' in self.data.keys()):
            y = self.data['engagement_type']
        if (x not in [None, "All", '']) and (y in [None, "All", '']):
            x = int(x)
            max_yr_id = Project.objects.aggregate(Max('academic_year_id'))
            min_yr_id = Project.objects.aggregate(Min('academic_year_id'))
            start = list(range(min_yr_id['academic_year_id__min'], (x + 1)))
            end = list(range(x, (max_yr_id['academic_year_id__max'] + 1)))
            proj_part1 = Project.objects.filter(academic_year__in=start).filter(end_academic_year=None)
            proj_part2 = Project.objects.filter(academic_year__in=start).filter(end_academic_year__in=end)
            proj_part = proj_part1 | proj_part2
            return proj_part
        elif (x in [None, "All", '']) and (y not in [None, "All", '']):
            return Project.objects.filter(engagement_type_id=y)
        elif (x not in [None, "All", '']) and (y not in [None, "All", '']):
            x = int(x)
            max_yr_id = Project.objects.aggregate(Max('academic_year_id'))
            min_yr_id = Project.objects.aggregate(Min('academic_year_id'))
            start = list(range(min_yr_id['academic_year_id__min'], (x + 1)))
            end = list(range(x, (max_yr_id['academic_year_id__max'] + 1)))
            proj_part1 = Project.objects.filter(academic_year__in=start).filter(end_academic_year=None).filter(engagement_type_id=y)
            proj_part2 = Project.objects.filter(academic_year__in=start).filter(end_academic_year__in=end).filter(engagement_type_id=y)
            proj_part = proj_part1 | proj_part2
            return proj_part
        else:
            return Project.objects.all()

class ProjectSubCategoryFilter(django_filters.FilterSet):

    class Meta:
        model = ProjectSubCategory
        fields = ['sub_category', ]

class FromProjectFilter(django_filters.FilterSet):
    # start=django_filters.filterset(queryset=Project.objects.filter(academic_year='academic_year').filter(end_academic_year=None))
    # end=django_filters.filterset(queryset=Project.objects.filter(academic_year='academic_year').filter(end_academic_year__gte='academic_year'))
    # fromProjects=list(set(start).intersection.set(end))
    class Meta:
        model = Project
        fields = ['engagement_type','academic_year','end_academic_year' ]


class ToProjectFilter(django_filters.FilterSet):
    # start = django_filters.filterset(queryset=Project.objects.filter(academic_year='academic_year').filter(end_academic_year=None))
    # end = django_filters.filterset(queryset=Project.objects.filter(academic_year='academic_year').filter(end_academic_year__gte='academic_year'))
    # toProjects = list(set(start).intersection.set(end))

    class Meta:
        model = Project
        fields = ['engagement_type','academic_year','end_academic_year' ]

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

class ProjectCommunityFilter(django_filters.FilterSet):

    class Meta:
        model = ProjectCommunityPartner
        fields = ['community_partner', ]


class communityPartnerFilter(django_filters.FilterSet):

    class Meta:
        model = CommunityPartner
        fields = ["weitz_cec_part", "community_type", "id"]


class CampusFilter(django_filters.FilterSet):

    class Meta:
        model = CampusPartner
        fields = ['name', 'college_name',]



class CommunityMissionFilter(django_filters.FilterSet):

    class Meta:
        model = CommunityPartnerMission
        fields = ["community_partner"]


class MissionAreaFilter(django_filters.FilterSet):

    class Meta:
        model = MissionArea
        fields = ["mission_name"]
