from projects.models import Project, ProjectCommunityPartner, ProjectMission
from django.forms import ModelForm, ModelChoiceField
from django.db.models import Max
from university.models import Course
from .models import Project,ProjectMission ,ProjectCommunityPartner ,ProjectCampusPartner ,Status ,EngagementType,ActivityType,AcademicYear, ProjectSubCategory
from partners.models import CecPartnerStatus
from django import forms
from django.forms import ModelForm


K12_CHOICES = [
    ('All', 'All'),
    ('Yes', 'Yes'),
    ('No', 'No')]


class K12ChoiceForm(forms.Form):
    k12_choice = forms.ChoiceField(label="K-12 Choices", choices=K12_CHOICES, required=False)


CEC_CHOICES = [
    ('All', 'All (CEC/Non-CEC Partners)'),
    ('CURR_COMM', 'Current Community Building Partners'),
    ('CURR_CAMP', 'Current Campus Building Partners'),
    ('FORMER_COMM', 'Former Community Building Partners'),
    ('FORMER_CAMP', 'Former Campus Building Partners')]
'''
    ('FORMER_CAMP', 'Former Campus Building Partners'),
    ('NEVER', 'Never CEC Building Partner')]
'''


class CecPartChoiceForm(forms.Form):
    cec_choice = forms.ChoiceField(label="CEC Partner Choices", choices=CEC_CHOICES, required=False)


COMM_CEC_CHOICES = [
    ('All', 'All (CEC/Non-CEC Partners)'),
    ('CURR_COMM', 'Current Community Building Partners'),
    ('FORMER_COMM', 'Former Community Building Partners')]
'''
    ('FORMER_CAMP', 'Former Campus Building Partners'),
    ('NEVER', 'Never CEC Building Partner')]
'''


class OommCecPartChoiceForm(forms.Form):
    cec_choice = forms.ChoiceField(label="Comm CEC Partner Choices", choices=COMM_CEC_CHOICES, required=False)

'''
class CecPartChoiceForm(forms.ModelForm):

    class Meta:
        model = CecPartnerStatus
        fields = ('name','description')
        labels = {
            'name': ('CEC Building Partner',)
        }
        widgets = {
            'name': forms.Textarea(attrs={'readonly': True,'rows':1, 'cols':80}),

        }
'''


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
            'total_hours': ('Hours'),
            'total_people':('Volunteers'),
        }
        widgets = {

            'wages': forms.Textarea(attrs={'readonly': True, 'rows': 1, 'cols': 70}),

        }

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm2(ModelForm):
    SEMESTER = [
        ("", "----------"), ("Fall", "Fall"), ("Spring", "Spring"), ("Summer", "Summer")]
    address_line1 = forms.CharField(required=False)
    country = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False, label="State or Province")
    zip = forms.CharField(required=False, label="Zip or Postal Code")
    semester = forms.ChoiceField(required=False, choices=SEMESTER)
    end_semester = forms.ChoiceField(required=False, choices=SEMESTER)
    k12_flag = forms.BooleanField(required=False)

    class Meta:
        model = Project
        fields = ('project_name','engagement_type','activity_type','facilitator','description','semester','total_uno_students',
                  'total_uno_hours','k12_flag','total_k12_students','total_k12_hours',
                  'total_uno_faculty','total_other_community_members','start_date','end_date' ,'other_details','outcomes',
                  'status','total_economic_impact', 'address_line1' ,'country' ,'city','zip', 'state','latitude',
                  'longitude','academic_year', 'end_academic_year', 'end_semester','other_sub_category','campus_lead_staff','project_type','other_activity_type')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
        labels = {
            'project_name': 'Project Name',
            'engagement_type': 'Engagement Type',
            'activity_type': 'Activity Type',
            'total_uno_students': 'Number of UNO Students',
            'total_uno_hours': 'Number of UNO Students Hours',
            'total_k12_students': 'Number of K-12 Students',
            'total_k12_hours': 'Number of K-12 Hours',
            'total_uno_faculty': 'Number of UNO Faculty/Staff',
            'start_date': 'Project Start Date',
            'end_date': 'Project End Date',
            'other_details': 'Other Important Details',
            'outcomes': 'Outcomes',
            'address_line1': 'Address',
            'total_other_community_members':  'Number of Other Participants',
            'academic_year': 'Start Academic Year',
            'end_academic_year': 'End Academic Year',
            'end_semester':'End semester',
            'semester': 'Start semester',
            'zip': 'Zip or Postal Code',
            'state': 'State or Province',

        }


    # def clean_facilitator(self):
    #     facilitator = self.cleaned_data['facilitator']
    #
    #     if any(char.isdigit() for char in facilitator):
    #         raise forms.ValidationError("Facilitator cannot have numbers")
    #
    #     return facilitator
    #
    # def clean_semester(self):
    #     semester = self.cleaned_data['semester']
    #     sem = semester.split('-')
    #
    #     if len(sem) < 0:
    #         raise forms.ValidationError("Semester should contain -")
    #     if sem[0] not in ['Fall', 'Spring', 'Summer']:
    #         raise forms.ValidationError("Please enter Summer, Spring or Fall")
    #     if len(int(sem[1])) != 4:
    #         raise forms.ValidationError("Year should contain 4 digits")
    #
    # def clean_total_uno_students(self):
    #     total_uno_students = self.cleaned_data['total_uno_students']
    #
    #     if type(total_uno_students) != int:
    #         raise forms.ValidationError("Students cannot have Decimals")
    #     return total_uno_students
    #
    # def clean_total_uno_hours(self):
    #     total_uno_hours = self.cleaned_data['total_uno_hours']
    #
    #     if type(total_uno_hours) not in [int, float]:
    #         raise forms.ValidationError("Hours cannot have characters")
    #
    # def clean_total_k12_students(self):
    #     total_k12_students = self.cleaned_data['total_k12_students']
    #
    #     if type(total_k12_students) != int:
    #         raise forms.ValidationError("K12 Students cannot have Decimals")
    #     return total_k12_students
    #
    # def clean_total_k12_hours(self):
    #     total_k12_hours = self.cleaned_data['total_k12_hours']
    #
    #     if type(total_k12_hours) not in [int, float]:
    #         raise forms.ValidationError("K12 Hours cannot have characters")
    #     return total_k12_hours
    #
    # def clean_total_uno_faculty(self):
    #     total_uno_faculty = self.cleaned_data['total_uno_faculty']
    #
    #     if type(total_uno_faculty) != int:
    #         raise forms.ValidationError("Faculty cannot have Decimals")
    #     return total_uno_faculty
    #
    # def clean_total_other_community_members(self):
    #     total_other_community_members = self.cleaned_data['total_other_community_members']
    #
    #     if type(total_other_community_members) != int:
    #         raise forms.ValidationError("Participants cannot have Decimals")
    #     return total_other_community_members
    #
    # def clean_country(self):
    #     country = self.cleaned_data['country']
    #
    #     if any(char.isdigit() for char in country):
    #         raise forms.ValidationError("Invalid Country Name")
    #     return country
    #
    # def clean_state(self):
    #     state = self.cleaned_data['state']
    #
    #     if any(char.isdigit() for char in state):
    #         raise forms.ValidationError("Invalid State Name")
    #     return state
    #
    # def clean_city(self):
    #     city = self.cleaned_data['city']
    #
    #     if any(char.isdigit() for char in city):
    #         raise forms.ValidationError("Invalid City Name")
    #     return city
    #
    # def clean_zip(self):
    #     zip = self.cleaned_data['zip']
    #     if type(zip) != int:
    #         raise forms.ValidationError("Invalid ZIP Code")
    #     return zip

class ProjectFormAdd(ModelForm):
    SEMESTER = [
        ("", "----------") ,  ("Fall", "Fall"), ("Spring", "Spring"), ("Summer", "Summer")]
    address_line1= forms.CharField(required=False)
    country = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False, label="State or Province")
    zip = forms.CharField(required=False, label="Zip or Postal Code")
    semester = forms.ChoiceField(required=False, choices=SEMESTER)
    end_semester = forms.ChoiceField(required=False, choices=SEMESTER)
    k12_flag = forms.BooleanField(required=False)
    class Meta:
        model = Project
        fields = ('project_name','engagement_type','activity_type','project_type','description','university', 'semester',
                  'status', 'address_line1','country','city', 'state','zip','latitude',
                  'longitude','academic_year', 'total_uno_students', 'total_uno_hours','k12_flag','total_k12_students','total_k12_hours',
                  'end_semester', 'other_sub_category', 'end_academic_year','campus_lead_staff','other_activity_type','total_uno_faculty','total_other_community_members')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

        labels = {
            'project_name': 'Project Name',
            'engagement_type': 'Engagement Type',
            'activity_type': 'Activity Type',
            'university': 'University',
            'total_uno_students': 'UNO Students',
            'total_uno_hours': 'UNO Student Service Hours',

            'start_date': 'Project Start Date',
            'end_date': 'Project End Date',

            'address_line1': 'Address',

            'academic_year': 'Academic Year',
            'end_academic_year': 'End Academic Year',
        }


class ProjectMissionForm(ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('project_name','mission_type' , 'mission',)
        labels = {
            'project_name' : ('Project Name'),
            'mission_type': ('Mission Type'),
            'mission': ('Mission'),
        }


class AddProjectCommunityPartnerForm(ModelForm):
    class Meta:
        model = ProjectCommunityPartner
        fields = ('community_partner',)
        labels = {
            'community_partner': (' '),

        }
class AddSubCategoryForm(ModelForm):
    class Meta:
        model = ProjectSubCategory
        fields = ('sub_category',)
        labels = {
            'sub_category': (' '),

        }

class AddProjectCampusPartnerForm(ModelForm):

    class Meta:
        model = ProjectCampusPartner
        fields = ('campus_partner',)
        labels = {
            'campus_partner':(' '),
        }

#    def clean_total_hours(self):
#        total_hours = self.cleaned_data['total_hours']
#        val = int(total_hours)
#        if val < 0:
#            raise forms.ValidationError("Hours cannot be negative")
#        return total_hours

#    def clean_total_people(self):
#        total_people = self.cleaned_data['total_people']
#        val = int(total_people)
#        if val < 0:
#            raise forms.ValidationError("Enter a positive number")
#        return total_people



class StatusForm(ModelForm):

    class Meta:
        model= Status
        fields = ('name','description',)

class EngagementTypeForm(ModelForm):
    name = ModelChoiceField(EngagementType.objects.all(), empty_label= 'Enagagement Type')
    class Meta:
        model = EngagementType
        fields =('name','description',)


class ActivityTypeForm(ModelForm):

    class Meta:
        model = ActivityType
        fields =('name','description',)

class ProjectMissionEditFormset(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('mission',)
        labels = {
            'mission': (' '),
        }

class projectfocusarea(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('mission',)
        labels = {
            'mission': (' '),
        }

class ProjectMissionFormset(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ( 'mission',)
        labels = {
            'mission': (' '),
        }


class ScndProjectMissionFormset(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ( 'mission',)
        labels = {
            'mission': ('Mission Area'),
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
    name = forms.CharField(required=False, label= 'Course Name')
    prefix = forms.CharField(required=False, label= 'Course Prefix')
    number = forms.CharField(required=False, label='Course Number' )
    section = forms.CharField(required=False, label='Course Section')

    class Meta:
        model = Course
        fields = ('name','prefix', 'number','section')
        labels = {
            'name': ('Course Name'),
            'prefix': ('Prefix'),
            'number': ('Course Number'),
            'section': ('Course Section')
        }