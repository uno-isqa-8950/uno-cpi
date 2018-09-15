from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator


class CommunityPartner (models.Model):
    TRUE_FALSE_CHOICES = (
        ('True', 'Yes'),
        ('False', 'No'),
    )

    name = models.CharField(max_length= 100)
    address_line1= models.CharField(max_length=50)
    address_line2= models.CharField(max_length=50 ,blank= True)
    country= models.CharField(max_length=55)
    city= models.CharField(max_length=25)
    state= models.CharField(max_length=15)
    Zip = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    website_url = models.TextField()
    college = models.CharField(max_length=50)
    k12_level =  models.CharField(max_length=20                                                                     )
    department = models.CharField(max_length=30)
    active = models.BooleanField(default= True)
    weitz_cec_part = models.CharField(max_length=6 , choices= TRUE_FALSE_CHOICES, default= False )


    def __str__(self):
        return str(self. name)


class CommunityType (models.Model):
    partner_name = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE)
    community_type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.partner_name)

    def __str__(self):
        return str(self.community_type)


class Project (models.Model):
    name = models.CharField(max_length=100)
    engagement_type = models.CharField(max_length=20)
    activity_type = models.CharField(max_length=20)
    facilitator = models.CharField(max_length=20)
    description = models.TextField()
    semester = models.CharField(max_length=20)
    no_uno_students = models.IntegerField()
    hours_uno = models.CharField(max_length=20)
    no_cp_members = models.IntegerField()
    hours_cp = models.CharField(max_length=10)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    details = models.CharField(max_length=100)
    no_uno_faculty = models.IntegerField()
    other_cp_members =models.IntegerField()
    outcomes = models.CharField(max_length=100)
    partners = models.ManyToManyField(CommunityPartner, related_name='p_name')

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    workphone= models.CharField(max_length=10,  validators=[MinLengthValidator(10)],
                                      help_text="Phone Number should be 10 digits")
    cellphone= models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                                      help_text="Phone Number should be 10 digits" , unique=True)
    contact_type = models.CharField(max_length=15)
    email_id = models.CharField(max_length=254)
    partner_name = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.first_name)

    def __str__(self):
        return str(self.last_name)


    def __str__(self):
        return str(self.partner_name)


class Missionarea (models.Model):
    mission_code = models.CharField(max_length=10,default= 0)
    mission_name = models.CharField(max_length=50)
    description = models.TextField()
  #  mission_code = models.ManyToManyField(CommunityPartner , through='CPMission')

    def __str__(self):
        return str(self.mission_name)


class CPMission (models.Model):
    partner_name = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20)
    mission_code = models.ForeignKey(Missionarea, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.partner_name)


class ProjectMission (models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    mission_type = models.CharField(max_length=20)
    mission_code = models.ForeignKey(Missionarea, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project_name)


#class ProjectPartner (models.Model):
   # project_id = models.ForeignKey(Project,  on_delete=models.CASCADE)
    #partner_id = models.ForeignKey(CommunityPartner, on_delete=models.CASCADE)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)








