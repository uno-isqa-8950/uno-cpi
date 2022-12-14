import json
import datetime
from shapely.geometry import shape, Point
from googlemaps import Client

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnoCPI.settings")
django.setup()

from partners.models import *

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


partner_list = CommunityPartner.objects.all().exclude(latitude__isnull=False)
print('partner list')
print(partner_list)

for part in partner_list:
    print(part)
    if part.address_line1 != '' and not None:
        try:
            print("Address " + part.address_line1)
            print("City " + part.city)
            print("State " + part.state)
            fulladdress = part.address_line1 + " " + part.city + " " + part.state
            print("Full Address "+fulladdress)
            print("USING GEOCODE NOW ON ADDRESS "+fulladdress+" UNDER Update_Partner.py")
            geocode_result = gmaps.geocode(str(fulladdress))
            print(geocode_result[0])
            if (geocode_result[0]):
                latitude = geocode_result[0]['geometry']['location']['lat']
                longitude = geocode_result[0]['geometry']['location']['lng']
                print(latitude)
                print(longitude)
                # for some reason the below isnt update the object, figure it out
                current_part = CommunityPartner.objects.get(id=part.id)
                current_part.latitude = latitude
                current_part.longitude = longitude
                current_part.save()
                print("New latitude " + CommunityPartner.objects.get(id=part.id).latitude)
                print("New longitude " + CommunityPartner.objects.get(id=part.id).longitude)
        except Exception as e:
            print(e)
    else:
        print("No address")

for part in partner_list:
    try:
        current_part = CommunityPartner.objects.get(id=part.id)
        coord = Point([current_part.longitude, current_part.latitude])
        legi_district = ''
        for i in range(len(district)):  # iterate through a list of district polygons
            property = district[i]
            polygon = shape(property['geometry'])  # get the polygons
            if polygon.contains(coord):  # check if a partner is in a polygon
                legi_district = property["properties"]["DISTRICT"]
                current_part.legislative_district = legi_district
                current_part.save()
    except Exception as e:
        print(e)