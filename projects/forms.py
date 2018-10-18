from projects.models import Project, ProjectCommunityPartner, ProjectMission
from django.forms import ModelForm
from .models import Project,ProjectMission ,ProjectCommunityPartner ,ProjectCampusPartner ,Status ,EngagementType,ActivityType
from django import forms
from django.forms import ModelForm

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name',)
        labels = {
            'project_name': ('Project Name'),
        }
        widgets = {
            #'name': forms.Field
            'project_name': forms.Textarea(attrs={'readonly': True,'rows':1, 'cols':80}),

        }

class missionform(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('mission_type','mission')


class ProjectCommunityPartnerForm(forms.ModelForm):
    class Meta:
        model = ProjectCommunityPartner
        fields = ('project_name','total_hours','total_people','wages')
        labels = {
            'total_hours': ('Community Hours'),
            'total_people':('Community Volunteer'),
        }


class ProjectForm2(ModelForm):
    class Meta:
        model = Project
        fields = ('project_name','engagement_type','activity_type','facilitator','description','semester','total_uno_students','total_uno_hours','total_k12_students','total_k12_hours',
                    'total_uno_faculty','total_other_community_members','start_date','end_date' ,'other_details','outcomes',
                    'status','total_economic_impact', 'address_line1' ,'address_line1' ,'country' ,'city', 'state','zip','latitude',
                    'longitude',)


class ProjectMissionForm(ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('project_name','mission_type' , 'mission',)
        labels = {
            'mission_type': ('Select mission type'),
            'mission': ('Select mission'),
        }


class ProjectCommunityPartnerForm2(ModelForm):
    class Meta:
        model = ProjectCommunityPartner
        fields = ('community_partner','total_hours','total_people','wages',)

class ProjectCampusPartnerForm(ModelForm):
    class Meta:
        model = ProjectCampusPartner
        fields = ('campus_partner','total_hours','total_people','wages',)


class StatusForm(ModelForm):
    class Meta:
        model= Status
        fields = ('name','description',)

class EngagementTypeForm(ModelForm):
    class Meta:
        model = EngagementType
        fields =('name','description',)


class ActivityTypeForm(ModelForm):
    class Meta:
        model = ActivityType
        fields =('name','description',)

class ProjectMissionFormset(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('mission_type', 'mission',)
        labels = {
            'mission_type': ('Select mission type'),
            'mission': ('Select mission'),
                    }
