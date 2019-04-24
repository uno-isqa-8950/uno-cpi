from django.contrib import admin
from .models import Project, ProjectMission, ProjectCommunityPartner, ProjectCampusPartner, EngagementType, \
    ActivityType, Status, AcademicYear
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

class ProjectResource(resources.ModelResource):
    project_name = fields.Field(attribute='project_name', column_name="Project Name")
    # engagement_type = fields.Field(attribute='engagement_type', column_name="Engagement Type")
    # activity_type = fields.Field(attribute='activity_type', column_name="Activity Type")
    # status = fields.Field(attribute='status', column_name="Status")

    class Meta:
        model = Project
        fields = ('id','project_name', 'engagement_type', 'activity_type', 'legislative_district','facilitator', 'description',
                    'semester', 'end_semester', 'academic_year', 'end_academic_year', 'total_uno_students', 'total_uno_hours', 
                    'total_k12_students','total_k12_hours', 'total_uno_faculty', 'total_other_community_members', 'start_date', 
                    'end_date', 'other_details', 'outcomes', 'status', 'total_economic_impact', 'address_line1', 'address_line2', 
                    'country', 'city', 'state', 'zip', 'latitude', 'longitude')

class ProjectList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('project_name', 'engagement_type', 'activity_type', 'legislative_district','facilitator', 'description', 'semester',
                    'total_uno_students', 'end_semester', 'academic_year', 'end_academic_year', 'total_uno_hours', 'total_k12_students',
                    'total_k12_hours', 'total_uno_faculty', 'total_other_community_members', 'start_date', 'end_date', 'other_details',
                    'outcomes', 'status', 'total_economic_impact', 'address_line1', 'address_line2', 'country', 'city',
                    'state', 'zip', 'latitude', 'longitude')

    search_fields = ('project_name', 'engagement_type__name', 'status__name', 'activity_type__name', 'facilitator', 'semester', 'city',
                     'start_date', 'end_date', 'country')

    resource_class = ProjectResource


class ProjectMissionResource(resources.ModelResource):
    # project_name = fields.Field(attribute='project_name', column_name="Project Name")
    # mission = fields.Field(attribute='mission', column_name="Mission Name")
    class Meta:
        model = ProjectMission
        fields = ('id', 'project_name', 'mission_type', 'mission')

class ProjectMissionList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('project_name', 'mission_type', 'mission')

    search_fields = ('project_name__project_name', 'mission_type', 'mission__mission_name')

    resource_class = ProjectMissionResource


class ProjectCommunityPartnerResource(resources.ModelResource):
    # project_name = fields.Field(attribute='project_name', column_name="Project Name")
    # community_partner = fields.Field(attribute='community_partner', column_name="Community Partner")
    class Meta:
        model = ProjectCommunityPartner
        fields = ('id', 'project_name', 'community_partner', 'total_hours', 'total_people', 'wages')

class ProjectCommunityPartnerList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('project_name', 'community_partner', 'total_hours', 'total_people', 'wages')

    search_fields = ('project_name__project_name', 'community_partner__name')

    resource_class = ProjectCommunityPartnerResource


class ProjectCampusPartnerResource(resources.ModelResource):
    # project_name = fields.Field(attribute='project_name', column_name="Project Name")
    # campus_partner = fields.Field(attribute='campus_partner', column_name="Campus Partner")
    class Meta:
        model = ProjectCampusPartner
        fields = ('id', 'project_name', 'campus_partner', 'total_hours', 'total_people', 'wages')

class ProjectCampusPartnerList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('project_name', 'campus_partner', 'total_hours', 'total_people', 'wages')

    search_fields = ('project_name__project_name', 'campus_partner__name')

    resource_class = ProjectCampusPartnerResource


class EngagementTypeResource(resources.ModelResource):

    class Meta:
        model = EngagementType

class EngagementTypeList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)

    resource_class = EngagementTypeResource


class ActivityTypeResource(resources.ModelResource):

    class Meta:
        model = ActivityType

class ActivityTypeList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)

    resource_class = ActivityType


class StatusList(admin.ModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)


class AcademicYearResource(resources.ModelResource):

    class Meta:
        model = AcademicYear

class AcademicYearList(SimpleHistoryAdmin, ImportExportModelAdmin):

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
