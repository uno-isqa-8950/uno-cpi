import pandas as pd
import googlemaps
import json
import datetime
from pandas import DataFrame
import boto3
import logging
import os
from shapely.geometry import shape, Point
import psycopg2
from django.conf import settings
from UnoCPI import settings
from googlemaps import Client
dirname = os.path.dirname(__file__)
county_file = os.path.join(dirname,'home/static/GEOJSON/USCounties_final.geojson')
district_file = os.path.join(dirname,'home/static/GEOJSON/ID2.geojson')
output_filename = os.path.join(dirname,'home/static/GEOJSON/Partner.geojson') #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()
global cursor

with open(county_file) as f:
    geojson1 = json.load(f)
county = geojson1["features"]
# Get lat long details of all the districts within State Nebraska to get populate Legislative Districts
with open(district_file) as f:
    geojson = json.load(f)
district = geojson["features"]
logger=logging.getLogger("UNO CPI Application")
# conn = psycopg2.connect("dbname=postgres user=postgres password=admin")
#setup connection to database
conn =   psycopg2.connect(user=settings.DATABASES['default']['USER'],
                              password=settings.DATABASES['default']['PASSWORD'],
                              host=settings.DATABASES['default']['HOST'],
                              port=settings.DATABASES['default']['PORT'],
                              database=settings.DATABASES['default']['NAME'],
                              sslmode="require")

if (conn):
    print("connection sucess",conn)
    logger.info("Connection Successful!")
else:
    logger.info("Connection Error!")

logger.info("Get all the Community Partners from the Database")

# Get all the Community Partners from the database
dfCommunity = pd.read_sql_query(
    "SELECT pc.name as Community_Partner,pc.address_line1, pc.address_line2, \
    pc.city, pc.state,pc.zip, hm.mission_name ,p.mission_type, \
    pc.legislative_district,pc.median_household_income, pc2.community_type,\
    pc.website_url FROM partners_communitypartner PC \
    join partners_communitypartnermission p on PC.id = p.community_partner_id \
    join home_missionarea hm on p.mission_area_id = hm.id \
    join partners_communitytype pc2 on PC.community_type_id = pc2.id \
    where  \
    (pc.address_line1 not in ('','NA','N/A') or pc.city not in ('','NA','N/A') or pc.state not in ('','NA','N/A')) \
    and pc.longitude is null \
    and pc.longitude is null \
    and pc.legislative_district is null \
    and lower(p.mission_type) = 'primary'",con=conn)

if len(dfCommunity) == 0:
    logger.critical("No Community Partners fetched from the Database on " + str(currentDT))
else:
    logger.info(repr(len(dfCommunity)) + "Community Partners are in the Database on " + str(currentDT))

cursor = conn.cursor()

gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)

if(gmaps):
    logger.info("GMAPS API works!")
else:
    logger.critical("GMAPS API Error!")

dfCommunity['fulladdress'] = dfCommunity[['address_line1', 'city', 'state']].apply(
    lambda x: ' '.join(x.astype(str)), axis=1)


# Function that generates GEOJSON
def feature_from_row(Community, Address):
    geocode_result = gmaps.geocode(Address)  # get the coordinates
    if (geocode_result[0]):
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        coord = Point([longitude, latitude])
        legi_district = ''
        for i in range(len(district)):  # iterate through a list of district polygons
            property = district[i]
            polygon = shape(property['geometry'])  # get the polygons
            if polygon.contains(coord):  # check if a partner is in a polygon
                legi_district = property["id"]

                logger.info("Update community partner records with longitude:" + str(round(longitude,7))+" ,latitude:" +str(round(latitude, 7)) + " ,legislative_district:"+ str(legi_district)+" ,name" +str(Community))
                cursor.execute("update partners_communitypartner set longitude= %s, latitude= %s,legislative_district= %s where name= %s",(str(round(longitude,7)),str(round(latitude, 7)),legi_district,str(Community)))
                conn.commit()


dfCommunity.apply(
    lambda x: feature_from_row(x['community_partner'], x['fulladdress']), axis=1)
cursor.close()
conn.close()


if len(dfCommunity) != 0:
    logger.info("Community Partners GEOSON is written at output directory" + str(output_filename)) 
    

# Log when the Script ran
logger.info("Community Partners of  " + repr(len(dfCommunity)) + " records are generated at " + str(currentDT))
