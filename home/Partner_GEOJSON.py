import pandas as pd
import googlemaps
import json
import datetime
from pandas import DataFrame
import os
from shapely.geometry import shape, Point
import psycopg2
from django.conf import settings
from googlemaps import Client

#TODO - MAP THE DATABASE CREDENTIALS USING ENV VARIABLES
#Get lat long details of all US counties in json format
with open('static/GEOJSON/USCounties_final.geojson') as f:
    geojson1 = json.load(f)
county = geojson1["features"]
#Get lat long details of all the districts within State Nebraska to get populate Legislative Districts
with open('static/GEOJSON/ID2.geojson') as f:
    geojson = json.load(f)
district = geojson["features"]

#setup connection to database --LOCAL
# conn = psycopg2.connect("dbname=postgres user=postgres password=admin")

#setup connection to database --SERVER
conn = psycopg2.connect(user= "nbzsljiyoqyakc",
                        password="56c6e80a45b37276d84917e4258a7798e2df7c1ec6eee012d160edc9de2ce6c1",
                        host="ec2-54-227-241-179.compute-1.amazonaws.com",
                        port="5432",
                        database="d46q2igt2d4vbg",
                        sslmode="require")
#Get all the Community Partners from the database
dfCommunity = pd.read_sql_query("SELECT pc.name as Community_Partner,pc.address_line1, pc.address_line2, pc.city, pc.state,pc.zip, hm.mission_name ,p.mission_type, pc.legislative_district,pc.median_household_income, pc2.community_type,pc.website_url FROM partners_communitypartner PC join partners_communitypartnermission p on PC.id = p.community_partner_id join home_missionarea hm on p.mission_area_id = hm.id join partners_communitytype pc2 on PC.community_type_id = pc2.id",con=conn)
#Get all the Projects from the database and get their Campus Partners , Community Partners associated
dfProjects = pd.read_sql_query("SELECT  project_name,academic_year , pc2.name as campus_partner ,um.college_name,ppcp.name as community_partner FROM projects_project P join projects_academicyear pa on P.academic_year_id = pa.id join projects_projectcampuspartner pc on P.id = pc.project_name_id join projects_projectcommunitypartner ppc on P.id = ppc.project_name_id join partners_communitypartner ppcp on ppc.community_partner_id = ppcp.id join partners_campuspartner pc2 on  pc.campus_partner_id= pc2.id join university_college um on um.id = pc2.college_name_id WHERE p.id IN (SELECT project_name_id FROM projects_projectcommunitypartner)",con=conn)
conn.close()
gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)
collection = {'type': 'FeatureCollection', 'features': []}

dfCommunity['fulladdress'] = dfCommunity[['address_line1', 'city', 'state']].apply(lambda x: ' '.join(x.astype(str)), axis=1)
#Function that generates GEOJSON
def feature_from_row(Community, Address, Mission, MissionType,City,CommunityType, Website):
    feature = {'type': 'Feature', 'properties': {'CommunityPartner': '', 'Address': '','Projects': '',
                                                 'College Name':'','Mission Type':'', 'Project Name': '',
                                                 'Legislative District Number': '', 'Number of projects': '',
                                                 'Income': '', 'City':'','County': '', 'Mission Area': '',
                                                 'CommunityType': '', 'Campus Partner': '',
                                                 'Academic Year': '', 'Website': ''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    geocode_result = gmaps.geocode(Address)  # get the coordinates
    if (geocode_result[0]):
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        feature['geometry']['coordinates'] = [longitude, latitude]
        coord = Point([longitude, latitude])
        for i in range(len(district)):  # iterate through a list of district polygons
            property = district[i]
            polygon = shape(property['geometry'])  # get the polygons
            if polygon.contains(coord):  # check if a partner is in a polygon
                feature['properties']['Legislative District Number'] = property["properties"]["id"]  # assign the district number to a partner
        for m in range(len(county)):  # iterate through the County Geojson
            properties2 = county[m]
            polygon = shape(properties2['geometry'])  # get the polygon
            if polygon.contains(coord):  # check if the partner in question belongs to a polygon
                feature['properties']['County'] = properties2['properties']['NAME']
                feature['properties']['Income'] = properties2['properties']['Income']
        projectlist = 0
    yearlist = []
    campuslist = []
    projectList =[]
    collegeList = []
    partners = dfProjects['community_partner']
    years = dfProjects['academic_year']
    campuses =dfProjects['campus_partner']
    projects = dfProjects['project_name']
    colleges =dfProjects['college_name']
    count = 0
    for n in range(len(partners)):
        if (partners[n] == Community):
            if (years[n] not in yearlist):
                yearlist.append(years[n])
            if (campuses[n] not in campuslist):
                campuslist.append(campuses[n])
            if (projects[n] not in projectList):
                projectList.append(projects[n])
            if (colleges[ n] not in collegeList):
                collegeList.append(colleges[n])
            count += 1
    feature['properties']['Number of projects'] = count
    feature['properties']['Campus Partner'] = campuslist
    feature['properties']['Academic Year'] = yearlist
    feature['properties']['Projects'] = projectList
    feature['properties']['College Name'] = collegeList
    feature['properties']['CommunityPartner'] = Community
    feature['properties']['CommunityType'] = CommunityType
    feature['properties']['Website'] = Website
    feature['properties']['Mission Area'] = Mission
    feature['properties']['Mission Type'] = MissionType
    feature['properties']['City'] = City

    collection['features'].append(feature)
    return feature


geojson_series = dfCommunity.apply(lambda x: feature_from_row(x['community_partner'], x['fulladdress'], x['mission_name'],x['mission_type'], x['city'], x['community_type'], x['website_url']), axis=1)
#
jsonstring = pd.io.json.dumps(collection)

output_filename = 'static/GEOJSON/Partner.geojson' #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()
#Log when the Script ran
print("Community Partners of  "+ repr(len(dfCommunity)) + " records are generated at "+ str(currentDT))
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))
