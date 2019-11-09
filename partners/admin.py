from django.contrib import admin
from .models import CommunityPartner,CommunityPartnerUser,CampusPartnerUser,  CommunityType,  CampusPartner, CommunityPartnerMission, CecPartActiveYrs, CecPartnerStatus, PartnerStatus
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class CommunityPartnerResource(resources.ModelResource):
    community_type = fields.Field(attribute='community_type', column_name="Community Type")

    class Meta:
        model = CommunityPartner
        fields = ('id','name', 'website_url', 'community_type', 'k12_level','address_line1', 'address_line2', 'country', 'county', 'city', 'state', 'zip', 'latitude','longitude','active', 'weitz_cec_part','legislative_district')
        import_id_fields = ['id','name', 'website_url', 'community_type', 'k12_level','address_line1', 'address_line2', 'country', 'county', 'city', 'state', 'zip', 'latitude','longitude','active', 'weitz_cec_part','legislative_district']

class CommunityPartnerList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'website_url', 'community_type', 'k12_level',

                     'address_line1', 'address_line2', 'country', 'county','city', 'state', 'zip', 'latitude', 'longitude',
                    'active', 'weitz_cec_part','legislative_district', 'partner_status', 'cec_partner_status')

    search_fields = ('name', 'county','city', 'website_url', 'active','partner_status', 'cec_partner_status')

    resource_class = CommunityPartnerResource

class CampusPartnerResource(resources.ModelResource):
    education_system = fields.Field(attribute='education_system', column_name="Education System")
    university = fields.Field(attribute='university', column_name="University")
    college_name = fields.Field(attribute='college_name', column_name="College Name")


    class Meta:
        model = CampusPartner
        fields = ('id','name', 'college_name','department','weitz_cec_part','active', 'university', 'education_system',
                  'cec_partner_status', 'partner_status')
        import_id_fields = ['id','name', 'college_name','department','weitz_cec_part','active', 'university', 'education_system','cec_partner_status', 'partner_status']

class CampusPartnerList(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ('name', 'college_name','department','weitz_cec_part','active','partner_status', 'cec_partner_status')

    search_fields = ('name', 'college_name__college_name','department__department_name','weitz_cec_part','active',
                     'partner_status__name', 'cec_partner_status__name')

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


class CecPartnerStatusResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name="CEC Status")
    description = fields.Field(attribute='description', column_name="CEC Status Description")

    class Meta:
        model = CecPartnerStatus
        fields = ('id','name', 'description')
        import_id_fields = ['id','name','description']


class CecPartnerStatusList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description')

    search_fields = ('name', 'description')

    resource_class = CecPartnerStatusResource


class CecPartActiveYrsResource(resources.ModelResource):
    start_semester = fields.Field(attribute='start_semester', column_name="CEC Partner Start Semester")
    start_acad_year = fields.Field(attribute='start_acad_year', column_name="CEC Partner Start AY")
    end_semester = fields.Field(attribute='end_semester', column_name="CEC Partner End Semester")
    end_acad_year = fields.Field(attribute='end_acad_year', column_name="CEC Partner End AY")
    comm_partner = fields.Field(attribute='comm_partner', column_name="Community Partner")
    camp_partner = fields.Field(attribute='camp_partner', column_name="Campus Partner")

    class Meta:
        model = CecPartActiveYrs
        fields = ('start_semester', 'start_acad_year','end_semester', 'end_acad_year','comm_partner','camp_partner')


class CecPartActiveYrsList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('start_semester', 'start_acad_year','end_semester', 'end_acad_year','comm_partner','camp_partner')

    search_fields = ('start_semester', 'start_acad_year','end_semester', 'end_acad_year','comm_partner','camp_partner')

    resource_class = CecPartActiveYrsResource


class PartnerStatusResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name="Partner Status")
    description = fields.Field(attribute='description', column_name="Partner Status Description")

    class Meta:
        model = PartnerStatus
        fields = ('id','name', 'description')
        import_id_fields = ['id','name','description']



class PartnerStatusList(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description')

    search_fields = ('name', 'description')

    resource_class = PartnerStatusResource

# class CommunityTypeList(admin.ModelAdmin):
#     list_display = ('community_type')
#     search_fields = ('community_type')


admin.site.register(CommunityPartner,CommunityPartnerList)
admin.site.register(CommunityPartnerUser,CommunityPartnerUserList)
admin.site.register(CommunityType, SimpleHistoryAdmin)
admin.site.register(CommunityPartnerMission,CommunityPartnerMissionList)
admin.site.register(CampusPartner,CampusPartnerList)
admin.site.register(CampusPartnerUser,CampusPartnerUserList)
admin.site.register(CecPartnerStatus,CecPartnerStatusList)
admin.site.register(CecPartActiveYrs,CecPartActiveYrsList)
admin.site.register(PartnerStatus,PartnerStatusList)
