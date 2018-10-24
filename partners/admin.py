from django.contrib import admin
from .models import CommunityPartner,CommunityPartnerUser,CampusPartnerUser,  CommunityType,  CampusPartner, CommunityPartnerMission


class CommunityPartnerList(admin.ModelAdmin):

    list_display = ('name', 'website_url', 'community_type', 'k12_level',

                     'address_line1', 'address_line2', 'country', 'county','city', 'state', 'zip', 'latitude', 'longitude',
                    'active', 'weitz_cec_part')

    search_fields = ('name', 'county','city', 'website_url', 'active')


class CampusPartnerList(admin.ModelAdmin):

    list_display = ('name', 'college_name','department','weitz_cec_part','active')

    search_fields = ('name', 'college_name','department','weitz_cec_part','active')


class CampusPartnerUserList(admin.ModelAdmin):

    list_display = ('campus_partner', 'user')

    search_fields = ('campus_partner', 'user')


class CommunityPartnerUserList(admin.ModelAdmin):
    list_display = ('community_partner', 'user')

    search_fields = ('community_partner', 'user')


class CommunityPartnerMissionList(admin.ModelAdmin):
    list_display = ('mission_type', 'mission_area','community_partner')

    search_fields = ('mission_type', 'mission_area','community_partner')


# class CommunityTypeList(admin.ModelAdmin):
#     list_display = ('community_type')
#     search_fields = ('community_type')


admin.site.register(CommunityPartner,CommunityPartnerList)
admin.site.register(CommunityPartnerUser,CommunityPartnerUserList)
admin.site.register(CommunityType)
admin.site.register(CommunityPartnerMission,CommunityPartnerMissionList)
admin.site.register(CampusPartner,CampusPartnerList)
admin.site.register(CampusPartnerUser,CampusPartnerUserList)



