import json
import datetime
from shapely.geometry import shape, Point
from googlemaps import Client

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnoCPI.settings")
django.setup()

from projects.models import *

dirname = os.path.dirname(__file__)
county_file = os.path.join(dirname,'home/static/GEOJSON/USCounties_final.geojson')
district_file = os.path.join(dirname,'home/static/GEOJSON/ID3.geojson')
output_filename = os.path.join(dirname,'home/static/GEOJSON/Partner.geojson') #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()

with open(county_file) as f:
    geojson1 = json.load(f)
county = geojson1["features"]
# Get lat long details of all the districts within State Nebraska to get populate Legislative Districts
with open(district_file) as f:
    geojson = json.load(f)
district = geojson["features"]

gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)

if(gmaps):
    print("GMAPS API works!")
else:
    print("GMAPS API Error!")


project_list = Project.objects.all().exclude(latitude__isnull=False)
print('project list')
print(project_list)

for proj in project_list:
    print(proj)
    if proj.address_line1 != '' and not None:
        try:
            print("Address " + proj.address_line1)
            print("City " + proj.city)
            print("State " + proj.state)
            fulladdress = proj.address_line1 + " " + proj.city + " " + proj.state
            print("Full Address "+fulladdress)
            print("USING GEOCODE NOW FOR PROJECT UPDATE ON ADDRESS "+fulladdress+" UNDER Update_Project.py")
            geocode_result = gmaps.geocode(str(fulladdress))
            if (geocode_result[0]):
                latitude = geocode_result[0]['geometry']['location']['lat']
                longitude = geocode_result[0]['geometry']['location']['lng']
                print(latitude)
                print(longitude)
                # for some reason the below isnt update the object, figure it out
                current_proj = Project.objects.get(id=proj.id)
                current_proj.latitude = latitude
                current_proj.longitude = longitude
                current_proj.save()
                print("New latitude " + Project.objects.get(id=proj.id).latitude)
                coord = Point([longitude, latitude])
                legi_district = ''
                for i in range(len(district)):  # iterate through a list of district polygons
                    property = district[i]
                    polygon = shape(property['geometry'])  # get the polygons
                    if polygon.contains(coord):  # check if a partner is in a polygon
                        legi_district = property["properties"]["DISTRICT"]
                        proj.legislative_district = legi_district


        except Exception as e:
            print(e)
    else:
        print("No address")