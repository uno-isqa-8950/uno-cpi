from django.contrib import admin
from .models import Project, ProjectMission, ProjectCommunityPartner, ProjectCampusPartner, EngagementType, \
    ActivityType, Status, AcademicYear
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ProjectResource(resources.ModelResource):

    class Meta:
        model = Project

class ProjectList(ImportExportModelAdmin):

    list_display = ('project_name', 'engagement_type', 'activity_type', 'legislative_district','facilitator', 'description', 'semester',
                    'total_uno_students', 'total_uno_hours', 'total_k12_students','total_k12_hours',
                    'total_uno_faculty', 'total_other_community_members', 'start_date', 'end_date', 'other_details',
                    'outcomes', 'status', 'total_economic_impact', 'address_line1', 'address_line2', 'country', 'city',
                    'state', 'zip', 'latitude', 'longitude')

    search_fields = ('name', 'engagement_type', 'status', 'activity_type', 'facilitator', 'semester', 'city',
                     'start_date', 'end_date', 'country')

    resource_class = ProjectResource


class ProjectMissionResource(resources.ModelResource):

    class Meta:
        model = ProjectMission


class ProjectMissionList(ImportExportModelAdmin):

    list_display = ('project_name', 'mission_type', 'mission')

    search_fields = ('project_name', 'mission_type', 'mission')

    resource_class = ProjectMissionResource


class ProjectCommunityPartnerResource(resources.ModelResource):

    class Meta:
        model = ProjectCommunityPartner

class ProjectCommunityPartnerList(ImportExportModelAdmin):

    list_display = ('project_name', 'community_partner', 'total_hours', 'total_people', 'wages')

    search_fields = ('project_name', 'community_partner', 'no_people')

    resource_class = ProjectCommunityPartnerResource


class ProjectCampusPartnerResource(resources.ModelResource):

    class Meta:
        model = ProjectCampusPartner

class ProjectCampusPartnerList(ImportExportModelAdmin):

    list_display = ('project_name', 'campus_partner', 'total_hours', 'total_people', 'wages')

    search_fields = ('project_name', 'campus_partner', 'no_people')

    resource_class = ProjectCampusPartnerResource


class EngagementTypeResource(resources.ModelResource):

    class Meta:
        model = EngagementType

class EngagementTypeList(ImportExportModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)

    resource_class = EngagementTypeResource


class ActivityTypeResource(resources.ModelResource):

    class Meta:
        model = ActivityType

class ActivityTypeList(ImportExportModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)

    resource_class = ActivityType


class StatusList(admin.ModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)


class AcademicYearResource(resources.ModelResource):

    class Meta:
        model = AcademicYear

class AcademicYearList(ImportExportModelAdmin):

    list_display = ('academic_year', 'description')

    search_fields = ('academic_year',)

    resource_class = AcademicYearResource


admin.site.register(Project, ProjectList)
admin.site.register(ProjectMission, ProjectMissionList)
admin.site.register(ProjectCommunityPartner, ProjectCommunityPartnerList)
admin.site.register(ProjectCampusPartner, ProjectCampusPartnerList)
admin.site.register(EngagementType, EngagementTypeList)
admin.site.register(ActivityType, ActivityTypeList)
admin.site.register(Status, StatusList)
admin.site.register(AcademicYear, AcademicYearList)
