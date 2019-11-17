import pandas as pd
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

dirname = os.path.dirname(__file__)
county_file = os.path.join(dirname,'home/static/GEOJSON/USCounties_final.geojson')
district_file = os.path.join(dirname,'home/static/GEOJSON/ID2.geojson')
output_filename = os.path.join(dirname,'home/static/GEOJSON/Partner.geojson') #The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()

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
    logger.info("Connection Successful!")
else:
    logger.info("Connection Error!")

logger.info("Get all the Community Partners from the Database")

# Get all the Community Partners from the database
dfCommunity = pd.read_sql_query(
    "SELECT distinct pc.name as Community_Partner,pc.address_line1, pc.address_line2, \
    pc.city, pc.state,pc.zip, hm.mission_name ,pm.mission_type, \
    pc.legislative_district,pc.median_household_income, pct.community_type,\
    pc.website_url, pc.longitude, pc.latitude, COALESCE(ces.name, 'Never') as name \
    FROM partners_communitypartner PC \
    join projects_projectcommunitypartner pcp on PC.id = pcp.community_partner_id \
    join projects_project proj on pcp.project_name_id = proj.id \
    join projects_projectcampuspartner pcam on proj.id = pcam.project_name_id \
    join partners_communitypartnermission pm on PC.id = pm.community_partner_id \
    join home_missionarea hm on pm.mission_area_id = hm.id \
    join partners_communitytype pct on PC.community_type_id = pct.id \
    left join partners_cecpartnerstatus ces on PC.cec_partner_status_id = ces.id \
    where  \
    (pc.address_line1 not in ('','NA','N/A') or pc.city not in ('','NA','N/A') or pc.state not in ('','NA','N/A')) \
    and pc.longitude is not null \
    and pc.latitude is not null \
    and lower(pm.mission_type) = 'primary'",con=conn)

if len(dfCommunity) == 0:
    logger.critical("No Community Partners fetched from the Database on " + str(currentDT))
else:
    logger.info(repr(len(dfCommunity)) + "Community Partners are in the Database on " + str(currentDT))

# Get all the Projects from the database and get their Campus Partners , Community Partners associated
dfProjects = pd.read_sql_query(
    "SELECT  project_name,academic_year , pc2.name as campus_partner ,\
    um.college_name,ppcp.name as community_partner \
    FROM projects_project P \
    join projects_academicyear pa on P.academic_year_id = pa.id \
    join projects_projectcampuspartner pc on P.id = pc.project_name_id \
    join projects_projectcommunitypartner ppc on P.id = ppc.project_name_id \
    join partners_communitypartner ppcp on ppc.community_partner_id = ppcp.id \
    join partners_campuspartner pc2 on  pc.campus_partner_id= pc2.id \
    join university_college um on um.id = pc2.college_name_id \
    WHERE p.id IN \
    (SELECT project_name_id FROM projects_projectcommunitypartner)",con=conn)
if len(dfProjects) == 0:
    logger.critical("No Projects are fetched from the Database as of " + str(currentDT))
else:
    logger.info(repr(len(dfProjects)) + "Projects are in the Database as of " + str(currentDT))
conn.close()

collection = {'type': 'FeatureCollection', 'features': []}

dfCommunity['fulladdress'] = dfCommunity[['address_line1', 'city', 'state']].apply(
    lambda x: ' '.join(x.astype(str)), axis=1)


# Function that generates GEOJSON
def feature_from_row(Community, Address, Mission, MissionType, City, CommunityType, longitude,latitude, Website,Cec_status,legislative_district):
    feature = {'type': 'Feature', 'properties': {'CommunityPartner': '', 'Address': '', 'Projects': '',
                                                 'College Name': '', 'Mission Type': '', 'Project Name': '',
                                                 'Legislative District Number': '', 'Number of projects': '',
                                                 'Income': '', 'City': '', 'County': '', 'Mission Area': '',
                                                 'CommunityType': '', 'Campus Partner': '',
                                                 'Academic Year': '', 'Website': '','Community CEC Status': ''},
               'geometry': {'type': 'Point', 'coordinates': []}
               }
    feature['geometry']['coordinates'] = [longitude, latitude]
    coord = Point([longitude, latitude])
    print('latitude--',latitude, ' longitude--',longitude, ' address--',Address,' Community--', Community)
    for i in range(len(district)):  # iterate through a list of district polygons
        property = district[i]
        polygon = shape(property['geometry'])  # get the polygons
        if polygon.contains(coord):  # check if a partner is in a polygon
            print('property["properties"]--',property["properties"]["id"])
            print('legislative_district--from database,',legislative_district)
            feature['properties']['Legislative District Number'] = legislative_district  # assign the district number to a partner
    for m in range(len(county)):  # iterate through the County Geojson
        properties2 = county[m]
        polygon = shape(properties2['geometry'])  # get the polygon
        if polygon.contains(coord):  # check if the partner in question belongs to a polygon
            feature['properties']['County'] = properties2['properties']['NAME']
            feature['properties']['Income'] = properties2['properties']['Income']
    projectlist = 0
    yearlist = []
    campuslist = []
    projectList = []
    collegeList = []
    partners = dfProjects['community_partner']
    years = dfProjects['academic_year']
    campuses = dfProjects['campus_partner']
    projects = dfProjects['project_name']
    colleges = dfProjects['college_name']
    count = 0
    for n in range(len(partners)):
        if (partners[n] == Community):
            if (years[n] not in yearlist):
                yearlist.append(years[n])
            if (campuses[n] not in campuslist):
                campuslist.append(campuses[n])
            if (projects[n] not in projectList):
                projectList.append(projects[n])
                count += 1
            if (colleges[n] not in collegeList):
                collegeList.append(colleges[n])

    feature['properties']['Number of projects'] = count
    feature['properties']['Campus Partner'] = campuslist
    feature['properties']['Academic Year'] = yearlist
    feature['properties']['Projects'] = projectList
    feature['properties']['College Name'] = collegeList
    feature['properties']['CommunityPartner'] = Community
    feature['properties']['CommunityType'] = CommunityType
    feature['properties']['Website'] = Website
    feature['properties']['Community CEC Status'] = Cec_status
    feature['properties']['Mission Area'] = Mission
    feature['properties']['Mission Type'] = MissionType
    feature['properties']['City'] = City    

    collection['features'].append(feature)
    return feature


geojson_series = dfCommunity.apply(
    lambda x: feature_from_row(x['community_partner'], x['fulladdress'], x['mission_name'],\
     x['mission_type'], x['city'], x['community_type'], \
      x['longitude'], x['latitude'], x['website_url'], \
      x['name'], x['legislative_district']), axis=1)
jsonstring = pd.io.json.dumps(collection)


if len(dfCommunity) != 0:
    logger.info("Community Partners GEOSON is written at output directory" + str(output_filename)) 
    with open(output_filename, 'w') as output_file:
        output_file.write(format(jsonstring))

# Log when the Script ran
logger.info("Community Partners of  " + repr(len(dfCommunity)) + " records are generated at " + str(currentDT))

#writing into amazon aws s3
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)
if len(dfCommunity) == 0:
    print("Partner GEOJSON file NOT written having total records of " +repr(len(dfCommunity))+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Partner GEOJSON file NOT written having total records of " +repr(len(dfCommunity))+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
else:
    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Partner.geojson').put(Body=format(jsonstring))
    print("Partner GEOJSON file written having total records of " +repr(len(dfCommunity))+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Partner GEOJSON file written having total records of " +repr(len(dfCommunity))+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
