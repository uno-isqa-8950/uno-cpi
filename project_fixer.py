import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnoCPI.settings")
django.setup()

from projects.models import *

for projmis in ProjectMission.objects.all():
    for proj in Project.objects.all():
        if proj.id == projmis.project_name.id:
            print("Match on: ")
            print(projmis.project_name)
            print(proj.project_name)
            print(projmis.mission)
            Project.objects.get(id=proj.id).mission_area.add(projmis.mission)

for projcamp in ProjectCampusPartner.objects.all():
    for proj in Project.objects.all():
        if proj.id == projcamp.project_name.id:
            print("Match on: ")
            print(projcamp.project_name)
            print(proj.project_name)
            Project.objects.get(id=proj.id).campus_partner.add(projcamp.campus_partner)

for projcom in ProjectCommunityPartner.objects.all():
    for proj in Project.objects.all():
        if proj.id == projcom.project_name.id:
            print("Match on: ")
            print(projcom.project_name)
            print(proj.project_name)
            Project.objects.get(id=proj.id).community_partner.add(projcom.community_partner)

for projsub in ProjectSubCategory.objects.all():
    for proj in Project.objects.all():
        if proj.id == projsub.project_name.id:
            print("Match on: ")
            print(projsub.project_name)
            print(proj.project_name)
            Project.objects.get(id=proj.id).subcategory.add(projsub.sub_category)