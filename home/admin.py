from django.contrib import admin
from .models import CommunityPartner, Contact, CommunityType, Project, ProjectMission, MissionArea,CommunityPartnerMission,Address,CampusPartner

admin.site.register(CommunityPartner)
admin.site.register(Contact)
admin.site.register(CommunityType)
admin.site.register(Project)
admin.site.register(ProjectMission )
admin.site.register(CommunityPartnerMission)
admin.site.register(MissionArea)
admin.site.register(Address)
admin.site.register(CampusPartner)