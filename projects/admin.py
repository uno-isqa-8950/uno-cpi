from django.contrib import admin
from .models import Project , ProjectMission,ProjectCommunityPartner, ProjectCampusPartner , EngagementType, ActivityType, Status

admin.site.register(Project)
admin.site.register(ProjectMission)
admin.site.register(ProjectCommunityPartner)
admin.site.register(ProjectCampusPartner)
admin.site.register(EngagementType)
admin.site.register(ActivityType)
admin.site.register(Status)