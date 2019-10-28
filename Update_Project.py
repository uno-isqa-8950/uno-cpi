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

logger=logging.getLogger("Run Update projects batch job")
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

# Get all the Projects from the database

df_projects = pd.read_sql_query("select  project_name, pro.address_line1 as Address_Line1,\
mis.mission_type, pro.description,pro.city as City, \
pro.state as State, pro.zip as Zip \
FROM projects_project pro  \
join projects_projectmission  mis on pro.id = mis.project_name_id \
where \
(pro.address_line1 not in ('','NA','N/A') \
or pro.city not in ('','NA','N/A') or pro.state not in ('','NA','N/A')) \
and (pro.longitude is null or pro.longitude is null or pro.legislative_district is null) \
and lower(mis.mission_type)='primary'",con=conn)
print('before checking query')
if len(df_projects) == 0:
    logger.info("No Projects fetched from the Database on " + str(currentDT))
    print("No Projects fetched from the Database on " + str(currentDT))
else:
    logger.info(repr(len(df_projects)) + " Projects are in the Database on " + str(currentDT))
    print(repr(len(df_projects)) + " Projects are in the Database on " + str(currentDT))
    cursor = conn.cursor()


gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)

if(gmaps):
    logger.info("GMAPS API works!")
else:
    logger.critical("GMAPS API Error!")

df_projects['fulladdress'] = df_projects[["address_line1", "city","state"]].apply(lambda x: ' '.join(x.astype(str)), axis=1)

# Function that generates GEOJSON
def feature_from_row(Projectname, FullAddress):
    geocode_result = gmaps.geocode(FullAddress)  # get the coordinates
    if (geocode_result[0]):
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        
        print('latitude--',latitude, ' longitude--',longitude, ' address--',FullAddress,' Projectname--', Projectname)
        coord = Point([longitude, latitude])
        legi_district = ''
        for i in range(len(district)):  # iterate through a list of district polygons
            property = district[i]
            polygon = shape(property['geometry'])  # get the polygons
            if polygon.contains(coord):  # check if a partner is in a polygon
                legi_district = property["id"]
                print('Found legislative district', legi_district, 'for--','latitude--',latitude, ' longitude--',longitude, ' address--',FullAddress,' Projectname--', Projectname)
                logger.info("Update projects records with longitude:" + str(round(longitude,7))+" ,latitude:" +str(round(latitude, 7)) + " ,legislative_district:"+ str(legi_district)+" ,name" +str(Projectname))
                cursor.execute("update projects_project set longitude= %s, latitude= %s,legislative_district= %s where project_name= %s",(str(round(longitude,7)),str(round(latitude, 7)),str(legi_district),str(Projectname)))
                conn.commit()


if len(df_projects) != 0:
    logger.info("Call update project function for each row") 
    df_projects.apply(lambda x: feature_from_row(x['project_name'], str(x['fulladdress'])), axis=1)
    cursor.close()
else:
    logger.info("Do not Call update project function for each row") 
    
conn.close()
# Log when the Script ran
logger.info("Projects of  " + repr(len(df_projects)) + " records are generated at " + str(currentDT))
