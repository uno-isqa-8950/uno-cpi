from django.db import models

# Create your models here.
class client(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    username=models.CharField(max_length=255)
    email = models.EmailField()
    password=models.CharField(max_length=255)

