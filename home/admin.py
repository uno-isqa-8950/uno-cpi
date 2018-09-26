from django.contrib import admin
from .models import CommunityPartner,CommunityPartnerUser,CampusPartnerUser, Contact, CommunityType, Project,  MissionArea,CampusPartner,  CampusPartnerContact


admin.site.register(CommunityPartner)

admin.site.register(Contact)
admin.site.register(CommunityType)
admin.site.register(Project)
#admin.site.register(ProjectMission )
#admin.site.register(CommunityPartnerMission)
admin.site.register(MissionArea)
#admin.site.register(Address)
admin.site.register(CampusPartner)
admin.site.register(CampusPartnerContact)
admin.site.register(CampusPartnerUser)
admin.site.register(CommunityPartnerUser)

