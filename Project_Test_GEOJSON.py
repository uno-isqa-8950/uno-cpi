import pandas as pd
import googlemaps
import json
import datetime
from pandas import DataFrame
import logging
import os
from shapely.geometry import shape, Point
import psycopg2
from django.conf import settings
from googlemaps import Client
#TODO - MAP THE DATABASE CREDENTIALS USING ENV VARIABLES
#Get lat long details of all US counties in json format

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

dirname = os.path.dirname(__file__)
county_file = os.path.join(dirname,'home/static/GEOJSON/USCounties_final.geojson')
district_file = os.path.join(dirname,'home/static/GEOJSON/ID2.geojson')
output_filename = os.path.join(dirname,'home/static/GEOJSON/Project.geojson') #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()

#TODO - MAP THE DATABASE CREDENTIALS USING ENV VARIABLES
#Get lat long details of all US counties in json format

# conn = psycopg2.connect("dbname=postgres user=postgres password=admin")

conn = psycopg2.connect(user="fhhzsyefbuyjdp",
                              password="e13f9084680555f19d5c0d2d48dd59d4b8b7a2fcbd695b47911335b514369304",
                              host="ec2-75-101-131-79.compute-1.amazonaws.com",
                              port="5432",
                              database="dal99elrltiq5q",
                              sslmode="require")


#Another way of querying the database
df = pd.read_sql_query("SELECT project_name,pe.name as engagement_type, pa.name as activity_type, pro.description,ay.academic_year, semester, total_uno_students, total_uno_hours, total_k12_students, total_k12_hours, total_other_community_members, total_uno_faculty,total_economic_impact, other_details, outcomes,  pc.name as community_partner, p.name as campus_partner, hm.mission_name as mission ,pp.mission_type as mission_type, ps.name as status, pro.address_line1 as Address_Line1, pro.address_line2, pro.city as City, pro.state as State, pro.zip as Zip, part_comm.community_type , uc.college_name FROM projects_project pro left join projects_projectcommunitypartner proCommPartnerLink on pro.id = proCommPartnerLink.project_name_id inner join partners_communitypartner pc on proCommPartnerLink.community_partner_id = pc.id left join projects_projectcampuspartner proCampPartnerLink on pro.id=proCampPartnerLink.project_name_id inner join partners_campuspartner p on proCampPartnerLink.campus_partner_id = p.id left join projects_projectmission pp on pro.id = pp.project_name_id inner join home_missionarea hm on pp.mission_id = hm.id left join projects_engagementtype pe on pro.engagement_type_id = pe.id left join projects_activitytype pa on pro.activity_type_id = pa.id left join projects_academicyear ay on pro.academic_year_id = ay.id left join projects_status ps on pro.status_id = ps.id inner join university_college uc on p.college_name_id = uc.id inner join partners_communitytype part_comm on pc.community_type_id = part_comm.id", con=conn)

conn.close()


gmaps = Client(key=GOOGLE_MAPS_API_KEY)
collection = {'type': 'FeatureCollection', 'features': []}
df['fulladdress'] = df[["address_line1", "city","state"]].apply(lambda x: ' '.join(x.astype(str)), axis=1)

with open(district_file) as f:
    geojson = json.load(f)

district = geojson["features"]
#
def feature_from_row(Projectname, Engagement, Activity, Description, Year, College, Campus, Community, Mission,CommunityType, Address, City, State, Zip):
    feature = {'type': 'Feature', 'properties': {'Project Name': '', 'Engagement Type': '', 'Activity Type': '',
                                                 'Description': '', 'Academic Year': '',
                                                 'Legislative District Number':'','College Name': '',
                                                 'Campus Partner': '', 'Community Partner':'', 'Mission Area':'','Community Partner Type':'',
                                                 'Address Line1':'', 'City':'', 'State':'', 'Zip':''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }


    if (Address != "N/A"):
        geocode_result = gmaps.geocode(Address)
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
            feature['properties']['Project Name'] = Projectname
            feature['properties']['Engagement Type'] = Engagement
            feature['properties']['Activity Type'] = Activity
            feature['properties']['Description'] = Description
            feature['properties']['Academic Year'] = Year
            feature['properties']['College Name'] = College
            feature['properties']['Campus Partner'] = Campus
            feature['properties']['Community Partner'] = Community
            feature['properties']['Mission Area'] = Mission
            feature['properties']['Community Partner Type']=CommunityType
            feature['properties']['Address Line1'] = Address
            feature['properties']['City'] = City
            feature['properties']['State'] = State
            feature['properties']['Zip'] = Zip
            collection['features'].append(feature)
            return feature


geojson_series = df.apply(lambda x: feature_from_row(x['project_name'], x['engagement_type'], x['activity_type'], x['description'],x['academic_year'], x['college_name'], x['campus_partner'], x['community_partner'],x['mission'],x['community_type'], str(x['address_line1']), str(x['city']), str(x['state']), str(x['zip'])), axis=1)
jsonstring = pd.io.json.dumps(collection)

print("Project GeoJSON  "+ repr(len(df)) + " records are generated at "+ str(currentDT))

with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))