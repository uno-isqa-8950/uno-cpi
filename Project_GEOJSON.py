import pandas as pd
import googlemaps
import json
import datetime
import boto3
from pandas import DataFrame
import logging
import os
from shapely.geometry import shape, Point
import psycopg2
from django.conf import settings
from UnoCPI import settings
from googlemaps import Client

#Get lat long details of all US counties in json format

dirname = os.path.dirname(__file__)
county_file = os.path.join(dirname,'home/static/GEOJSON/USCounties_final.geojson')
district_file = os.path.join(dirname,'home/static/GEOJSON/ID2.geojson')
output_filename = os.path.join(dirname,'home/static/GEOJSON/Project.geojson') #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()

conn = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                              password=settings.DATABASES['default']['PASSWORD'],
                              host=settings.DATABASES['default']['HOST'],
                              port=settings.DATABASES['default']['PORT'],
                              database=settings.DATABASES['default']['NAME'],
                              sslmode="require")
##Get Projects from the database
df_projects = pd.read_sql_query("select  project_name, pro.address_line1 as Address_Line1,mis.mission_type, pro.description,pro.city as City, pro.state as State, pro.zip as Zip FROM projects_project pro  join projects_projectmission  mis on pro.id = mis.project_name_id where (pro.address_line1 not in ('','NA','N/A') or pro.city not in ('','NA','N/A') or pro.state not in ('','NA','N/A'))  and lower(mis.mission_type)='primary'",con=conn)
##Get all the Campus Partners and College Names
df = pd.read_sql_query("select pro.project_name, pc.name as campus_partner ,uc.college_name , p.name as community_partner , pa.name as activity_type, pe.name as engagement_type,a.academic_year, hm.mission_name,c.community_type from projects_project pro left join projects_projectcampuspartner procamp on pro.id = procamp.project_name_id join partners_campuspartner pc on procamp.campus_partner_id = pc.id join university_college uc on pc.college_name_id = uc.id  left join projects_projectcommunitypartner pp on pro.id = pp.project_name_id left join partners_communitypartner p on pp.community_partner_id = p.id left join projects_activitytype pa on pro.activity_type_id = pa.id left join projects_engagementtype pe on pro.engagement_type_id = pe.id left join projects_academicyear a on pro.academic_year_id = a.id left join projects_projectmission pp2 on pro.id = pp2.project_name_id join home_missionarea hm on pp2.mission_id = hm.id left join partners_communitytype c on p.community_type_id = c.id",con=conn)
conn.close()
gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)

collection = {'type': 'FeatureCollection', 'features': []}
df_projects['fulladdress'] = df_projects[["address_line1", "city","state"]].apply(lambda x: ' '.join(x.astype(str)), axis=1)
with open(district_file) as f:
    geojson = json.load(f)
district = geojson["features"]

def feature_from_row(Projectname,Description,  FullAddress,Address_line1, City, State, Zip):
    feature = {'type': 'Feature', 'properties': {'Project Name': '', 'Engagement Type': '', 'Activity Type': '',
                                                 'Description': '', 'Academic Year': '',
                                                 'Legislative District Number':'','College Name': '',
                                                 'Campus Partner': '', 'Community Partner':'', 'Mission Area':'','Community Partner Type':'',
                                                 'Address Line1':'', 'City':'', 'State':'', 'Zip':''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }

    geocode_result = gmaps.geocode(FullAddress)
    if (geocode_result[0]):
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        feature['geometry']['coordinates'] = [longitude, latitude]
        coord = Point([longitude, latitude])
        for i in range(len(district)):  # iterate through a list of district polygons
            property = district[i]
            polygon = shape(property['geometry'])  # get the polygons
            if polygon.contains(coord):  # check if a partner is in a polygon
                feature['properties']['Legislative District Number'] = property["properties"][
                    "id"]  # assign the district number to a partner
    yearlist = []
    campusPartnersList = []
    communityPartnerList = []
    communityTypeList = []
    collegeList = []
    missionAreaList = []
    activityTypeList = []
    engagementTypeList = []
    projects = df['project_name']
    campusPartners = df['campus_partner']
    academicYear = df['academic_year']
    communityPartners = df['community_partner']
    missionAreas = df['mission_name']
    communityPartnerType = df['community_type']
    activityType = df['activity_type']
    colleges = df['college_name']
    engagementType = df['engagement_type']

    for n in range(len(projects)):
        if (projects[n] == Projectname):
            if (campusPartners[n] not in campusPartnersList):
                campusPartnersList.append(campusPartners[n])
            if (colleges[n] not in collegeList):
                collegeList.append(colleges[n])
            if (academicYear[n] not in yearlist):
                yearlist.append(academicYear[n])
            if (communityPartners[n] not in communityPartnerList):
                communityPartnerList.append(communityPartners[n])
            if (communityPartnerType[n] not in communityTypeList):
                communityTypeList.append(communityPartnerType[n])
            if (missionAreas[n] not in missionAreaList):
                missionAreaList.append(missionAreas[n])
            if (activityType[n] not in activityTypeList):
                activityTypeList.append(activityType[n])
            if (engagementType[n] not in engagementTypeList):
                engagementTypeList.append(engagementType[n])

    feature['properties']['Project Name'] = Projectname
    feature['properties']['Engagement Type'] = engagementTypeList
    feature['properties']['Activity Type'] = activityTypeList
    feature['properties']['Description'] = Description
    feature['properties']['Academic Year'] = yearlist
    feature['properties']['College Name'] = collegeList
    feature['properties']['Campus Partner'] = campusPartnersList
    feature['properties']['Community Partner'] = communityPartnerList
    feature['properties']['Mission Area'] = missionAreaList
    feature['properties']['Community Partner Type']=communityTypeList
    feature['properties']['Address Line1'] = Address_line1
    feature['properties']['City'] = City
    feature['properties']['State'] = State
    feature['properties']['Zip'] = Zip
    collection['features'].append(feature)
    return feature

geojson_series = df_projects.apply(lambda x: feature_from_row(x['project_name'], x['description'], str(x['fulladdress']),str(x['address_line1']), str(x['city']), str(x['state']), str(x['zip'])), axis=1)
jsonstring = pd.io.json.dumps(collection)

print("Project GeoJSON  "+ repr(len(df_projects)) + " records are generated at "+ str(currentDT))

with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))

#writing into amazon aws s3
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Project.geojson').put(Body=format(jsonstring))

print("Project GEOJSON file written to S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at "+str(currentDT))