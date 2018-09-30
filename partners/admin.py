from django.contrib import admin
from .models import CommunityPartner,CommunityPartnerUser,CampusPartnerUser,  CommunityType,  CampusPartner, CommunityPartnerMission

admin.site.register(CommunityPartner)
admin.site.register(CommunityPartnerUser)
admin.site.register(CommunityType)
admin.site.register(CommunityPartnerMission)
admin.site.register(CampusPartner)
admin.site.register(CampusPartnerUser)



