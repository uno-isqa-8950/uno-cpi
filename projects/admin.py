from django.contrib import admin
from .models import Project, ProjectMission, ProjectCommunityPartner, ProjectCampusPartner, EngagementType, \
    ActivityType, Status, AcademicYear,ProjectRelatedLink, ProjectSubCategory,SubCategory,MissionSubCategory,\
    EngagementActivityType, ProjectEngagementActivity
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
                  'semester', 'end_semester', 'academic_year', 'end_academic_year', 'campus_lead_staff', 'total_uno_students', 'total_uno_hours',
                  'k12_flag', 'total_k12_students','total_k12_hours', 'total_uno_faculty', 'total_other_community_members', 'start_date',
                  'end_date', 'other_details', 'outcomes', 'status', 'total_economic_impact', 'address_line1', 'address_line2', 
                  'country', 'city', 'state', 'zip', 'latitude', 'longitude', 'created_by', 'updated_by', 'project_type', 'other_sub_category',
                  'recursive_project')

class ProjectList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('project_name', 'engagement_type', 'activity_type', 'legislative_district','facilitator', 'description', 'semester',
                    'total_uno_students', 'end_semester', 'academic_year', 'end_academic_year', 'campus_lead_staff','total_uno_hours', 'k12_flag', 'total_k12_students',
                    'total_k12_hours', 'total_uno_faculty', 'total_other_community_members', 'start_date', 'end_date', 'other_details',
                    'outcomes', 'status', 'total_economic_impact', 'address_line1', 'address_line2', 'country', 'city',
                    'state', 'zip', 'latitude', 'longitude','created_by', 'updated_by', 'project_type', 'other_sub_category',
                    'recursive_project')

    search_fields = ('id','project_name', 'engagement_type__name', 'status__name', 'activity_type__name', 'facilitator', 'semester', 'city',
                     'start_date', 'end_date', 'country', 'project_type', 'other_sub_category', 'recursive_project')

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
        fields = ('id','name','description')
        import_id_fields = ['id','name','description']


class ActivityTypeList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)

    resource_class = ActivityTypeResource


class EngagementActivityTypeResource(resources.ModelResource):
     class Meta:
         model = EngagementActivityType
         import_id_fields = ['id','EngagementTypeName','ActivityTypeName']


class EngagementActivityTypeList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('EngagementTypeName', 'ActivityTypeName')

    search_fields = ('EngagementTypeName__name', 'ActivityTypeName__name')

    resource_class = EngagementActivityTypeResource


class ProjectEngagementActivityResource(resources.ModelResource):
    class Meta:
        model = ProjectEngagementActivity



class ProjectEngagementActivityList(admin.ModelAdmin):

    list_display = ('ProjectName', )
    #search_fields = ('projectname__project_name', 'ProjectEngagementActivityName__EngagementActivityType')
    resource_class = ProjectEngagementActivityResource


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

class ProjectRelatedLinksResource(resources.ModelResource):
    class Meta:
        model = ProjectRelatedLink


class ProjectRelatedLinksList (SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('project_name', 'link_descr', 'link', 'isAccessible')

    search_fields = ('project_name', )

    resource_class = ProjectRelatedLinksResource

class SubCategoryResource (resources.ModelResource):
    class Meta:
        model = SubCategory
        fields = ('id','sub_category', 'sub_category_descr')
        import_id_fields = ['id','sub_category','sub_category_descr']


class SubCategoryList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('sub_category', 'sub_category_descr')

    search_fields = ('sub_category',)

    resource_class = SubCategoryResource


class ProjectSubCategoryResource(resources.ModelResource):
    class Meta:
        model = ProjectSubCategory
        fields = ('project_name', 'sub_category')
        import_id_fields = ['project_name', 'sub_category']



class ProjectSubCategoryList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('project_name', 'sub_category')

    search_fields = ('project_name__project_name', 'sub_category__sub_category')

    resource_class = ProjectSubCategoryResource

class MissionSubCategoryResource(resources.ModelResource):
    class Meta:
        model = MissionSubCategory
        import_id_fields = ['id','sub_category','secondary_mission_area']


class MissionSubCategoryList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('secondary_mission_area', 'sub_category')

    search_fields = ('secondary_mission_area__mission_name', 'sub_category__sub_category')

    resource_class = MissionSubCategoryResource


admin.site.register(Project, ProjectList)
admin.site.register(ProjectMission, ProjectMissionList)
admin.site.register(ProjectCommunityPartner, ProjectCommunityPartnerList)
admin.site.register(ProjectCampusPartner, ProjectCampusPartnerList)
admin.site.register(EngagementType, EngagementTypeList)
admin.site.register(ActivityType, ActivityTypeList)
admin.site.register(Status, StatusList)
admin.site.register(AcademicYear, AcademicYearList)
admin.site.register(ProjectRelatedLink, ProjectRelatedLinksList)
admin.site.register(SubCategory, SubCategoryList)
admin.site.register(ProjectSubCategory, ProjectSubCategoryList)
admin.site.register(MissionSubCategory, MissionSubCategoryList)
admin.site.register(EngagementActivityType, EngagementActivityTypeList)
admin.site.register(ProjectEngagementActivity, ProjectEngagementActivityList)
#admin.site.register(engagement_type_inline)
