import pandas as pd
import googlemaps
import json
import psycopg2
from pandas import DataFrame
import datetime
from shapely.geometry import shape, Point
from django.conf import settings
from googlemaps import Client


#setup connection to database
#TODO - MAP THE DATABASE CREDENTIALS USING ENV VARIABLES
#setup connection to database --LOCAL
conn = psycopg2.connect("dbname=postgres user=postgres password=admin")
#setup connection to database --SERVER
# conn = psycopg2.connect(user= "nbzsljiyoqyakc",
#                         password="56c6e80a45b37276d84917e4258a7798e2df7c1ec6eee012d160edc9de2ce6c1",
#                         host="ec2-54-227-241-179.compute-1.amazonaws.com",
#                         port="5432",
#                         database="d46q2igt2d4vbg",
#                         sslmode="require")
try:
    connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()

    # WAY 1 - Query the Database
    cursor.execute("SELECT project_name,pe.name as engagement_type, pa.name as activity_type, "
                   "pro.description,ay.academic_year, semester, total_uno_students, total_uno_hours, total_k12_students, total_k12_hours, total_other_community_members, "
                   "total_uno_faculty,total_economic_impact, other_details, outcomes,  pc.name as community_partner, p.name as campus_partner, hm.mission_name as mission ,pp.mission_type as mission_type,"
                   "ps.name as status, pro.address_line1, pro.address_line2, pro.city, pro.state, pro.zip, uc.college_name"
                   " FROM projects_project pro left join projects_projectcommunitypartner proCommPartnerLink on pro.id = proCommPartnerLink.project_name_id"
                                             " inner join partners_communitypartner pc on proCommPartnerLink.community_partner_id = pc.id"
                                             " left join projects_projectcampuspartner proCampPartnerLink on pro.id=proCampPartnerLink.project_name_id"
                                             " inner join partners_campuspartner p on proCampPartnerLink.campus_partner_id = p.id"
                                             " left join projects_projectmission pp on pro.id = pp.project_name_id"
                                             " inner join home_missionarea hm on pp.mission_id = hm.id"
                                             " left join projects_engagementtype pe on pro.engagement_type_id = pe.id"
                                             " left join projects_activitytype pa on pro.activity_type_id = pa.id"
                                             " left join projects_academicyear ay on pro.academic_year_id = ay.id"
                                             " left join projects_status ps on pro.status_id = ps.id"
                                             " inner join university_college uc on p.college_name_id = uc.id")
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    # print("PostgreSQL connection is closed")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()

#Another way of querying the database
df = pd.read_sql_query("SELECT project_name,pe.name as engagement_type, pa.name as activity_type, pro.description,ay.academic_year, semester, total_uno_students, total_uno_hours, total_k12_students, total_k12_hours, total_other_community_members, total_uno_faculty,total_economic_impact, other_details, outcomes,  pc.name as community_partner, p.name as campus_partner, hm.mission_name as mission ,pp.mission_type as mission_type, ps.name as status, pro.address_line1 as Address_Line1, pro.address_line2, pro.city as City, pro.state as State, pro.zip as Zip, uc.college_name FROM projects_project pro left join projects_projectcommunitypartner proCommPartnerLink on pro.id = proCommPartnerLink.project_name_id inner join partners_communitypartner pc on proCommPartnerLink.community_partner_id = pc.id left join projects_projectcampuspartner proCampPartnerLink on pro.id=proCampPartnerLink.project_name_id inner join partners_campuspartner p on proCampPartnerLink.campus_partner_id = p.id left join projects_projectmission pp on pro.id = pp.project_name_id inner join home_missionarea hm on pp.mission_id = hm.id left join projects_engagementtype pe on pro.engagement_type_id = pe.id left join projects_activitytype pa on pro.activity_type_id = pa.id left join projects_academicyear ay on pro.academic_year_id = ay.id left join projects_status ps on pro.status_id = ps.id inner join university_college uc on p.college_name_id = uc.id", con=conn)

conn.close()

gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)
collection = {'type': 'FeatureCollection', 'features': []}
# df['fulladdress'] = df[["address_line1", "state", "city", "zip"]].apply(lambda x: ' '.join(x.astype(str)), axis=1)

with open('static/GEOJSON/ID2.geojson') as f:
    geojson = json.load(f)

district = geojson["features"]
#
def feature_from_row(Projectname, Engagement, Activity, Description, Year, College, Campus, Community, Mission, Address, City, State, Zip):
    feature = {'type': 'Feature', 'properties': {'Project Name': '', 'Engagement Type': '', 'Activity Type': '',
                                                 'Description': '', 'Academic Year': '',
                                                 'Legislative District Number':'','College Name': '',
                                                 'Campus Partner': '', 'Community Partner':'', 'Mission Area':'',
                                                 'Address Line1':'', 'City':'', 'State':'', 'Zip':''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    if (Address != "nan"):
        if (Address):
            fulladdress = str(Address) + ' ' + str(City) + ' ' + str(State)
            geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
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
            feature['properties']['Address Line1'] = Address
            feature['properties']['City'] = City
            feature['properties']['State'] = State
            feature['properties']['Zip'] = Zip
            collection['features'].append(feature)
            return feature


geojson_series = df.apply(lambda x: feature_from_row(x['project_name'], x['engagement_type'], x['activity_type'], x['description'],x['academic_year'], x['college_name'], x['campus_partner'], x['community_partner'],x['mission'], str(x['address_line1']), str(x['city']), str(x['state']), str(x['zip'])), axis=1)
jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/Project.geojson' #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()
print("Project GeoJSON  "+ repr(len(df)) + " records are generated at "+ str(currentDT))

with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))