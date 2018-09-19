from django.contrib import admin
from .models import CommunityPartner, Contact, CommunityType, Project, ProjectMission, Missionarea,CPMission



admin.site.register(CommunityPartner)
admin.site.register(Contact )
admin.site.register(CommunityType )
admin.site.register(Project )
admin.site.register(ProjectMission )
admin.site.register(CPMission)
admin.site.register(Missionarea)