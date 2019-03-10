from django.contrib import admin
from .models import CommunityPartner,CommunityPartnerUser,CampusPartnerUser,  CommunityType,  CampusPartner, CommunityPartnerMission
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CommunityPartnerResource(resources.ModelResource):

    class Meta:
        model = CommunityPartner

class CommunityPartnerList(ImportExportModelAdmin):

    list_display = ('name', 'website_url', 'community_type', 'k12_level',

                     'address_line1', 'address_line2', 'country', 'county','city', 'state', 'zip', 'latitude', 'longitude',
                    'active', 'weitz_cec_part')

    search_fields = ('name', 'county','city', 'website_url', 'active')

    resource_class = CommunityPartnerResource

class CampusPartnerResource(resources.ModelResource):

    class Meta:
        model = CampusPartner

class CampusPartnerList(ImportExportModelAdmin):

    list_display = ('name', 'college_name','department','weitz_cec_part','active')

    search_fields = ('name', 'college_name','department','weitz_cec_part','active')

    resource_class = CampusPartnerResource

class CampusPartnerUserResource(resources.ModelResource):

    class Meta:
        model = CampusPartnerUser

class CampusPartnerUserList(ImportExportModelAdmin):

    list_display = ('campus_partner', 'user')

    search_fields = ('campus_partner', 'user')

    resource_class = CampusPartnerUserResource


class CommunityPartnerUserResource(resources.ModelResource):

    class Meta:
        model = CommunityPartnerUser

class CommunityPartnerUserList(ImportExportModelAdmin):
    list_display = ('community_partner', 'user')

    search_fields = ('community_partner', 'user')

    resource_class = CommunityPartnerUserResource


class CommunityPartnerMissionResource(resources.ModelResource):

    class Meta:
        model = CommunityPartnerMission

class CommunityPartnerMissionList(ImportExportModelAdmin):
    list_display = ('community_partner','mission_area','mission_type')

    search_fields = ('community_partner','mission_area','mission_type')

    resource_class = CommunityPartnerMissionResource




# class CommunityTypeList(admin.ModelAdmin):
#     list_display = ('community_type')
#     search_fields = ('community_type')


admin.site.register(CommunityPartner,CommunityPartnerList)
admin.site.register(CommunityPartnerUser,CommunityPartnerUserList)
admin.site.register(CommunityType)
admin.site.register(CommunityPartnerMission,CommunityPartnerMissionList)
admin.site.register(CampusPartner,CampusPartnerList)
admin.site.register(CampusPartnerUser,CampusPartnerUserList)



