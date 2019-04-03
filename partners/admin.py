from django.contrib import admin
from .models import CommunityPartner,CommunityPartnerUser,CampusPartnerUser,  CommunityType,  CampusPartner, CommunityPartnerMission
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class CommunityPartnerResource(resources.ModelResource):
    community_type = fields.Field(attribute='community_type', column_name="Community Type")

    class Meta:
        model = CommunityPartner
        fields = ('name', 'website_url', 'community_type', 'k12_level','address_line1', 'address_line2', 'country', 'county', 'city', 'state', 'zip', 'latitude','longitude','active', 'weitz_cec_part')

class CommunityPartnerList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'website_url', 'community_type', 'k12_level',

                     'address_line1', 'address_line2', 'country', 'county','city', 'state', 'zip', 'latitude', 'longitude',
                    'active', 'weitz_cec_part')

    search_fields = ('name', 'county','city', 'website_url', 'active')

    resource_class = CommunityPartnerResource

class CampusPartnerResource(resources.ModelResource):
    education_system = fields.Field(attribute='education_system', column_name="Education System")
    university = fields.Field(attribute='university', column_name="University")
    college_name = fields.Field(attribute='college_name', column_name="College Name")


    class Meta:
        model = CampusPartner
        fields = ('name', 'college_name','department','weitz_cec_part','active', 'university', 'education_system')

class CampusPartnerList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'college_name','department','weitz_cec_part','active')

    search_fields = ('name', 'college_name__college_name','department__department_name','weitz_cec_part','active')

    resource_class = CampusPartnerResource

class CampusPartnerUserResource(resources.ModelResource):
    campus_partner = fields.Field(attribute='campus_partner', column_name="Campus Partner")
    user = fields.Field(attribute='user', column_name="User Name")
    class Meta:
        model = CampusPartnerUser

class CampusPartnerUserList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('campus_partner', 'user')

    search_fields = ('campus_partner__name', 'user__email')

    resource_class = CampusPartnerUserResource


class CommunityPartnerUserResource(resources.ModelResource):
    community_partner = fields.Field(attribute='community_partner', column_name="Community Partner")
    user = fields.Field(attribute='user', column_name="User Name")
    class Meta:
        model = CommunityPartnerUser

class CommunityPartnerUserList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('community_partner', 'user')

    search_fields = ('community_partner__name', 'user__email')

    resource_class = CommunityPartnerUserResource


class CommunityPartnerMissionResource(resources.ModelResource):
    community_partner = fields.Field(attribute='community_partner', column_name="Community Partner")
    mission_area = fields.Field(attribute='mission_area', column_name="Mission Area")
    mission_type = fields.Field(attribute='mission_type', column_name="Mission Type")

    class Meta:
        model = CommunityPartnerMission

class CommunityPartnerMissionList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('community_partner','mission_area','mission_type')

    search_fields = ('community_partner__name','mission_area__mission_name','mission_type')

    resource_class = CommunityPartnerMissionResource




# class CommunityTypeList(admin.ModelAdmin):
#     list_display = ('community_type')
#     search_fields = ('community_type')


admin.site.register(CommunityPartner,CommunityPartnerList)
admin.site.register(CommunityPartnerUser,CommunityPartnerUserList)
admin.site.register(CommunityType, SimpleHistoryAdmin)
admin.site.register(CommunityPartnerMission,CommunityPartnerMissionList)
admin.site.register(CampusPartner,CampusPartnerList)
admin.site.register(CampusPartnerUser,CampusPartnerUserList)



