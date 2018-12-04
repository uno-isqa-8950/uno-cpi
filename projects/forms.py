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
            'total_hours': ('Hours'),
            'total_people':('Volunteers'),
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
                    'longitude','academic_year')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'total_uno_hours': forms.Textarea(attrs={'readonly': True, 'rows': 1, 'cols': 8}),
        }
        labels = {
            'project_name': 'Project Name',
            'engagement_type': 'Engagement Type',
            'activity_type': 'Activity Type',
            'total_uno_students': 'Total Number of UNO Students',
            'total_uno_hours': 'Total Number of UNO Students Hours',
            'total_k12_students': 'Total Number of K-12 Students',
            'total_k12_hours': 'Total Number of K-12 Hours',
            'total_uno_faculty': 'Total Number of UNO Faculty/Staff',
            'start_date': 'Project Start Date',
            'end_date': 'Project End Date',
            'other_details': 'Other Important Details',
            'outcomes': 'Outcomes',
            'address_line1': 'Address Line',
            'total_other_community_members':  'Total Other Participants',
            'academic_year': 'Academic Year'
        }
    
    def clean_facilitator(self):
        facilitator = self.cleaned_data['facilitator']

        if any(char.isdigit() for char in facilitator):
            raise forms.ValidationError("Facilitator cannot have numbers")

        return facilitator

    def clean_semester(self):
        semester = self.cleaned_data['semester']
        sem = semester.split('-')

        if len(sem) < 0:
            raise forms.ValidationError("Semester should contain -")
        if sem[0] not in ['fall', 'spring', 'summer']:
            raise forms.ValidationError("Please enter summer, spring or fall")
        if len(int(sem[1])) == 4:
            raise forms.ValidationError("Year should contain 4 digits")

    def clean_total_uno_students(self):
        total_uno_students = self.cleaned_data['total_uno_students']
    
        if type(total_uno_students) != int:
            raise forms.ValidationError("Students cannot have Decimals")
        return total_uno_students

    def clean_total_uno_hours(self):
        total_uno_hours = self.cleaned_data['total_uno_hours']

        if type(total_uno_hours) not in [int, float]:
            raise forms.ValidationError("Hours cannot have characters")

    def clean_total_k12_students(self):
        total_k12_students = self.cleaned_data['total_k12_students']
        
        if type(total_k12_students) != int:
            raise forms.ValidationError("K12 Students cannot have Decimals")
        return total_k12_students

    def clean_total_k12_hours(self):
        total_k12_hours = self.cleaned_data['total_k12_hours']

        if type(total_k12_hours) not in [int, float]:
            raise forms.ValidationError("K12 Hours cannot have characters")
        return total_k12_hours

    def clean_total_uno_faculty(self):
        total_uno_faculty = self.cleaned_data['total_uno_faculty']

        if type(total_uno_faculty) != int:
            raise forms.ValidationError("Faculty cannot have Decimals")
        return total_uno_faculty
    
    def clean_total_other_community_members(self):
        total_other_community_members = self.cleaned_data['total_other_community_members']
        
        if type(total_other_community_members) != int:
            raise forms.ValidationError("Participants cannot have Decimals")
        return total_other_community_members

    def clean_country(self):
        country = self.cleaned_data['country']
        
        if any(char.isdigit() for char in country):
            raise forms.ValidationError("Invalid Country Name")
        return country

    def clean_state(self):
        state = self.cleaned_data['state']

        if any(char.isdigit() for char in state):
            raise forms.ValidationError("Invalid State Name")
        return state

    def clean_city(self):
        city = self.cleaned_data['city']

        if any(char.isdigit() for char in city):
            raise forms.ValidationError("Invalid City Name")
        return city

    def clean_zip(self):
        zip = self.cleaned_data['zip']
        if type(zip) != int:
            raise forms.ValidationError("Invalid ZIP Code")
        return zip


class ProjectFormAdd(ModelForm):
    address_line1= forms.CharField(required=True)
    country = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    zip = forms.IntegerField(required=True)

    class Meta:
        model = Project
        fields = ('project_name','engagement_type','activity_type','facilitator','description','semester','total_uno_students','total_uno_hours','total_k12_students','total_k12_hours',
                    'total_uno_faculty','total_other_community_members','start_date','end_date' ,'other_details','outcomes',
                    'status','total_economic_impact', 'address_line1'  ,'country' ,'city', 'state','zip','latitude',
                    'longitude','academic_year')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

        labels = {
            'project_name': 'Project Name',
            'engagement_type': 'Engagement Type',
            'activity_type': 'Activity Type',
            'total_uno_students': 'Total Number Of UNO Students',
            'total_uno_hours': 'Total Number Of UNO Students Hours',
            'total_k12_students': 'Total Number Of K-12 Students',
            'total_k12_hours': 'Total Number Of K-12 Hours',
            'total_uno_faculty': 'Total Number Of UNO Faculty/Staff',
            'start_date': 'Project Start Date',
            'end_date': 'Project End Date',
            'other_details': 'Other Important Details',
            'outcomes': 'Outcomes',
            'address_line1': 'Address Line',
            'total_other_community_members':  'Total Other Participants',
            'academic_year': 'Academic Year',
        }

    def clean_facilitator(self):
        facilitator = self.cleaned_data['facilitator']

        if any(char.isdigit() for char in facilitator):
            raise forms.ValidationError("Facilitator cannot have numbers")

        return facilitator

    def clean_semester(self):
        semester = self.cleaned_data['semester']
        sem = semester.split('-')

        if len(sem) < 0:
            raise forms.ValidationError("Semester should contain -")
        if sem[0] not in ['fall', 'spring', 'summer']:
            raise forms.ValidationError("Please enter summer, spring or fall")
        if len(int(sem[1])) == 4:
            raise forms.ValidationError("Year should contain 4 digits")

    def clean_total_uno_students(self):
        total_uno_students = self.cleaned_data['total_uno_students']
    
        if type(total_uno_students) != int:
            raise forms.ValidationError("Students cannot have Decimals")
        return total_uno_students

    def clean_total_uno_hours(self):
        total_uno_hours = self.cleaned_data['total_uno_hours']

        if type(total_uno_hours) not in [int, float]:
            raise forms.ValidationError("Hours cannot have characters")

    def clean_total_k12_students(self):
        total_k12_students = self.cleaned_data['total_k12_students']
        
        if type(total_k12_students) != int:
            raise forms.ValidationError("K12 Students cannot have Decimals")
        return total_k12_students

    def clean_total_k12_hours(self):
        total_k12_hours = self.cleaned_data['total_k12_hours']

        if type(total_k12_hours) not in [int, float]:
            raise forms.ValidationError("K12 Hours cannot have characters")
        return total_k12_hours

    def clean_total_uno_faculty(self):
        total_uno_faculty = self.cleaned_data['total_uno_faculty']

        if type(total_uno_faculty) != int:
            raise forms.ValidationError("Faculty cannot have Decimals")
        return total_uno_faculty
    
    def clean_total_other_community_members(self):
        total_other_community_members = self.cleaned_data['total_other_community_members']
        
        if type(total_other_community_members) != int:
            raise forms.ValidationError("Participants cannot have Decimals")
        return total_other_community_members

    def clean_country(self):
        country = self.cleaned_data['country']
        
        if any(char.isdigit() for char in country):
            raise forms.ValidationError("Invalid Country Name")
        return country

    def clean_state(self):
        state = self.cleaned_data['state']

        if any(char.isdigit() for char in state):
            raise forms.ValidationError("Invalid State Name")
        return state

    def clean_city(self):
        city = self.cleaned_data['city']

        if any(char.isdigit() for char in city):
            raise forms.ValidationError("Invalid City Name")
        return city

    def clean_zip(self):
        zip = self.cleaned_data['zip']
        if type(zip) != int:
            raise forms.ValidationError("Invalid ZIP Code")
        return zip


class ProjectMissionForm(ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('project_name','mission_type' , 'mission',)
        labels = {
            'project_name' : ('Project Name'),
            'mission_type': ('Mission Type'),
            'mission': ('Mission'),
        }


class ProjectCommunityPartnerForm2(ModelForm):
    class Meta:
        model = ProjectCommunityPartner
        fields = ('community_partner','total_hours','total_people',)
        labels = {
            'community_partner': ('Community Partner'),
            'total_hours': ('Hours'),
            'total_people': ('Volunteers'),
        }


class ProjectCampusPartnerForm(ModelForm):
    class Meta:
        model = ProjectCampusPartner
        fields = ('campus_partner','total_hours','total_people',)
        labels = {
            'campus_partner':('Campus Partner'),
            'total_hours': ('Hours'),
            'total_people': ('Volunteers'),
        }


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

class ProjectMissionFormset(forms.ModelForm):
    class Meta:
        model = ProjectMission
        fields = ('mission_type', 'mission',)
        labels = {
            'mission_type': ('Mission Type'),
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
    name = forms.CharField(required=False)
    prefix = forms.CharField(required=False)
    number = forms.CharField(required=False)

    class Meta:
        model = Course
        fields = ('name','prefix', 'number' , 'project_name')
        labels = {
            'name': ('Course Name'),
            'prefix': ('Prefix'),
            'number': ('Course Number')
        }