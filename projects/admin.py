from django.contrib import admin
from .models import Project , ProjectMission,ProjectCommunityPartner, ProjectCampusPartner

admin.site.register(Project)
admin.site.register(ProjectMission)
admin.site.register(ProjectCommunityPartner)
admin.site.register(ProjectCampusPartner)
