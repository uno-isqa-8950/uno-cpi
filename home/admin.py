from django.contrib import admin
from .models import  Contact,  Project, ProjectMission, MissionArea,Address,CampusPartner,  CampusPartnerContact
from partners.models import CommunityType, CommunityPartner, CommunityPartnerMission

admin.site.register(CommunityPartner)
admin.site.register(Contact)
admin.site.register(CommunityType)
admin.site.register(Project)
admin.site.register(ProjectMission )
admin.site.register(CommunityPartnerMission)
admin.site.register(MissionArea)
admin.site.register(Address)
admin.site.register(CampusPartner)
admin.site.register(CampusPartnerContact)
