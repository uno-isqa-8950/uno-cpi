from projects.models import Project, ProjectCommunityPartner, ProjectMission
from django.forms import ModelForm, ModelChoiceField

from university.models import Course
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
        widgets = {

            'wages': forms.Textarea(attrs={'readonly': True, 'rows': 1, 'cols': 70}),

        }

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm2(ModelForm):
    class Meta:
        model = Project
        fields = ('project_name','engagement_type','activity_type','facilitator','description','semester','total_uno_students','total_uno_hours','total_k12_students','total_k12_hours',
                    'total_uno_faculty','total_other_community_members','start_date','end_date' ,'other_details','outcomes',
                    'status','total_economic_impact', 'address_line1' ,'address_line1' ,'country' ,'city', 'state','zip','latitude',
                    'longitude',)
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'total_uno_hours': forms.Textarea(attrs={'readonly': True, 'rows': 1, 'cols': 8}),
        }
        labels = {
            'total_other_community_members':  'Total Other Participants',

        }

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
        fields = ('community_partner','total_hours','total_people',)



class ProjectCampusPartnerForm(ModelForm):
    class Meta:
        model = ProjectCampusPartner
        fields = ('campus_partner','total_hours','total_people',)


class StatusForm(ModelForm):
    class Meta:
        model= Status
        fields = ('name','description',)

class EngagementTypeForm(ModelForm):
    name = ModelChoiceField(EngagementType.objects.all(), empty_label= 'Select Enagagement Type')
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

class ProjectSearchForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name',)
        labels = {
            'project_name':('Project Name'),
         }
     # def __init__(self, *args, **kwargs):
    #     super(ProjectSearchForm, self).__init__(*args, **kwargs)
    #     self.fields['project_name'].widget = forms.TextInput(attrs={
    #         'id': 'id_project_name'})


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name','prefix', 'number')
        labels = {
            'name': ('Course Name'),
            'prefix': ('Prefix'),
            'number': ('Course Number')
        }