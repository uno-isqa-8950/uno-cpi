from django.contrib import admin
from .models import Project, ProjectMission, ProjectCommunityPartner, ProjectCampusPartner, EngagementType, \
    ActivityType, Status, AcademicYear


class ProjectList(admin.ModelAdmin):

    list_display = ('project_name', 'engagement_type', 'activity_type', 'legislative_district','facilitator', 'description', 'semester',
                    'total_uno_students', 'total_uno_hours', 'total_k12_students','total_k12_hours',
                    'total_uno_faculty', 'total_other_community_members', 'start_date', 'end_date', 'other_details',
                    'outcomes', 'status', 'total_economic_impact', 'address_line1', 'address_line2', 'country', 'city',
                    'state', 'zip', 'latitude', 'longitude')

    search_fields = ('name', 'engagement_type', 'status', 'activity_type', 'facilitator', 'semester', 'city',
                     'start_date', 'end_date', 'country')


class ProjectMissionList(admin.ModelAdmin):

    list_display = ('project_name', 'mission_type', 'mission')

    search_fields = ('project_name', 'mission_type', 'mission')


class ProjectCommunityPartnerList(admin.ModelAdmin):

    list_display = ('project_name', 'community_partner', 'total_hours', 'total_people', 'wages')

    search_fields = ('project_name', 'community_partner', 'no_people')


class ProjectCampusPartnerList(admin.ModelAdmin):

    list_display = ('project_name', 'campus_partner', 'total_hours', 'total_people', 'wages')

    search_fields = ('project_name', 'campus_partner', 'no_people')


class EngagementTypeList(admin.ModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)


class ActivityTypeList(admin.ModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)


class StatusList(admin.ModelAdmin):

    list_display = ('name', 'description')

    search_fields = ('name',)


class AcademicYearList(admin.ModelAdmin):

    list_display = ('academic_year', 'description')
    search_fields = ('academic_year',)


admin.site.register(Project, ProjectList)
admin.site.register(ProjectMission, ProjectMissionList)
admin.site.register(ProjectCommunityPartner, ProjectCommunityPartnerList)
admin.site.register(ProjectCampusPartner, ProjectCampusPartnerList)
admin.site.register(EngagementType, EngagementTypeList)
admin.site.register(ActivityType, ActivityTypeList)
admin.site.register(Status, StatusList)
admin.site.register(AcademicYear, AcademicYearList)
