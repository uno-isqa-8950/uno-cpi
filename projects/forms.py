from django import forms
from django import forms
from projects.models import Project, ProjectCommunityPartner, ProjectMission
from django.forms import ModelForm

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name','engagement_type','facilitator','description')

class missionform(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('mission_type','mission')


class ProjectCommunityPartnerForm(forms.ModelForm):
    class Meta:
        model = ProjectCommunityPartner
        fields = ('project_name','community_partner','total_hours','total_people','wages')