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

logger = logging.getLogger("UNO CPI Application")

dirname = os.path.dirname(__file__)
county_file = os.path.join(dirname, 'home/static/GEOJSON/USCounties_final.geojson')
district_file = os.path.join(dirname, 'home/static/GEOJSON/ID3.geojson')
output_filename = os.path.join(dirname,
                               'home/static/GEOJSON/Partner.geojson')  # The file will be saved under static/GEOJSON
currentDT = datetime.datetime.now()
ACCESS_ID = settings.AWS_ACCESS_KEY_ID
ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
                    aws_access_key_id=ACCESS_ID,
                    aws_secret_access_key=ACCESS_KEY)

with open(county_file) as f:
    geojson1 = json.load(f)
county = geojson1["features"]
# Get lat long details of all the districts within State Nebraska to get populate Legislative Districts
with open(district_file) as f:
    geojson = json.load(f)
district = geojson["features"]

# setup connection to database
conn = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                        password=settings.DATABASES['default']['PASSWORD'],
                        host=settings.DATABASES['default']['HOST'],
                        port=settings.DATABASES['default']['PORT'],
                        database=settings.DATABASES['default']['NAME'],
                        sslmode="require")
if (conn):
    cursor = conn.cursor()
    logger.info("Connection Successful!")
else:
    logger.info("Connection Error!")

collection = {'type': 'FeatureCollection', 'features': []}


# Function that generates GEOJSON
def feature_from_row(Community, commId, Address, Mission, MissionType, City, CommunityType, longitude, latitude,
                     Website, Cec_status, legislative_district):
    feature = {'type': 'Feature',
               'properties': {'CommunityPartner': '', 'Address': '', 'Projects': '',
                              'College Name': '', 'Mission Type': '', 'Project Name': '',
                              'Legislative District Number': '', 'Number of projects': '',
                              'Income': '', 'City': '', 'County': '', 'Mission Area': '',
                              'CommunityType': '', 'Campus Partner': '',
                              'Academic Year': '', 'Website': '', 'Community CEC Status': ''},
               'geometry': {'type': 'Point', 'coordinates': []},
               'communityprojects': [
                   {'name': '', 'academicYear': [], 'campuspartner': [], 'engagementType': '', 'collegeNames': []}]
               }
    feature['geometry']['coordinates'] = [longitude, latitude]
    coord = Point([longitude, latitude])
    print('latitude--', latitude, ' longitude--', longitude, ' address--', Address, ' Community--', Community)
    for i in range(len(district)):  # iterate through a list of district polygons
        property = district[i]
        polygon = shape(property['geometry'])  # get the polygons
        if polygon.contains(coord):  # check if a partner is in a polygon
            # print('property["properties"]--',property["properties"]["id"])
            # print('legislative_district--from database,',legislative_district)
            feature['properties']['Legislative District Number'] = property["properties"]["DISTRICT"]  # assign the district number to a partner
    for m in range(len(county)):  # iterate through the County Geojson
        properties2 = county[m]
        polygon = shape(properties2['geometry'])  # get the polygon
        if polygon.contains(coord):  # check if the partner in question belongs to a polygon
            feature['properties']['County'] = properties2['properties']['NAME']
            feature['properties']['Income'] = properties2['properties']['Income']

    feature['properties']['CommunityPartner'] = Community
    feature['properties']['CommunityType'] = CommunityType
    feature['properties']['Website'] = Website
    feature['properties']['Community CEC Status'] = Cec_status
    feature['properties']['Mission Area'] = Mission
    feature['properties']['Mission Type'] = MissionType
    feature['properties']['City'] = City

    get_project_sql = "SELECT  project_name, (select academic_year from projects_academicyear ay where ay.id = p.academic_year_id) as startyear , \
    (select academic_year from projects_academicyear where id = COALESCE(p.end_academic_year_id,p.academic_year_id)) as endyear, \
    pem.name as engagement_type , array_agg(distinct pc2.name) as campus_partner ,\
    array_agg(um.college_name) as collegeList \
    FROM projects_project P \
    join projects_academicyear pa on P.academic_year_id = pa.id \
    join projects_projectcampuspartner pc on P.id = pc.project_name_id \
    join projects_projectcommunitypartner ppc on P.id = ppc.project_name_id \
    join partners_communitypartner ppcp on ppc.community_partner_id = ppcp.id \
    join partners_campuspartner pc2 on  pc.campus_partner_id= pc2.id \
    join university_college um on um.id = pc2.college_name_id \
    join projects_engagementtype pem on p.engagement_type_id = pem.id \
    join projects_status ps on ps.id = p.status_id \
    WHERE ps.name != 'Drafts' and ppcp.id = %s group by  project_name, \
    startyear, endyear, engagement_type"
    communityprojectsList = []
    count = 0
    yearlist = []
    campuslist = []
    cursor.execute(get_project_sql, (str(commId),))
    # print('project cursor.fetchall()--',cursor.fetchall())
    projectsCount = cursor.fetchall()
    if len(projectsCount) > 0:
        count = len(projectsCount)

        for x in projectsCount:
            projYearList = []
            name = x[0]
            start_academic_year = x[1]
            end_academic_year = x[2]
            eng_type = x[3]
            campList = x[4]
            collegeList = x[5]

            for x in campList:
                if x not in campuslist:
                    campuslist.append(x)

            if (start_academic_year not in yearlist):
                yearlist.append(start_academic_year)
            if (start_academic_year not in projYearList):
                projYearList.append(start_academic_year)

            if (end_academic_year not in yearlist):
                yearlist.append(end_academic_year)
            if (end_academic_year not in projYearList):
                projYearList.append(end_academic_year)

            if (start_academic_year is not None and end_academic_year is not None):
                cursor.execute("select academic_year from projects_academicyear \
                    where id < (select id from projects_academicyear where academic_year = %s) \
                    and id > (select id from projects_academicyear where academic_year = %s)",
                               (str(end_academic_year), str(start_academic_year),))
                academicList = cursor.fetchall()
                if len(academicList) != 0:
                    for obj in academicList:
                        if (obj[0] not in yearlist):
                            yearlist.append(obj[0])
                        if (obj[0] not in projYearList):
                            projYearList.append(obj[0])
                else:
                    print('Academic Year not found')

            projname = ''
            try:
                Projectname = name.split(':')
            except ValueError:
                print('name does not have year')
                projname = Projectname
            else:
                for i in range(0, len(Projectname) - 1):
                    projname += Projectname[i]

            projObj = {'name': str(projname) + ';' + str(start_academic_year), 'academicYear': projYearList,
                       'campuspartner': campList, 'engagementType': eng_type, 'collegeNames': collegeList}
            communityprojectsList.append(projObj)

        feature['properties']['Number of projects'] = count

        if len(yearlist) > 0:
            yearlist.sort()
        feature['properties']['Academic Year'] = yearlist
        feature['properties']['Campus Partner'] = campuslist
        feature['communityprojects'] = communityprojectsList

    return feature


# Get all the Community Partners from the database
select_comm_partner = "SELECT distinct pc.name as Community_Partner, pc.id as commId, pc.address_line1, pc.address_line2, \
    pc.city, pc.state,pc.zip, hm.mission_name ,pm.mission_type, \
    pc.legislative_district,pc.median_household_income, pct.community_type,\
    pc.website_url, pc.longitude, pc.latitude, COALESCE(ces.name, 'Never') as name \
    FROM partners_communitypartner PC \
    join projects_projectcommunitypartner pcp on PC.id = pcp.community_partner_id \
    join projects_project proj on pcp.project_name_id = proj.id \
    join projects_status ps on ps.id = proj.status_id \
    join projects_projectcampuspartner pcam on proj.id = pcam.project_name_id \
    join partners_communitypartnermission pm on PC.id = pm.community_partner_id \
    join home_missionarea hm on pm.mission_area_id = hm.id \
    join partners_communitytype pct on PC.community_type_id = pct.id \
    left join partners_cecpartnerstatus ces on PC.cec_partner_status_id = ces.id \
    where  \
    (pc.address_line1 not in ('','NA','N/A') or pc.city not in ('','NA','N/A') or pc.state not in ('','NA','N/A')) \
    and pc.longitude is not null \
    and pc.latitude is not null \
    and ps.name != 'Drafts' \
    and lower(pm.mission_type) = 'primary'"

cursor.execute(select_comm_partner)
commPartnerList = cursor.fetchall()
if commPartnerList is not None:
    print('length of comm partners---', len(commPartnerList))
    for obj in commPartnerList:
        fulladdress = str(obj[2]) + ' ' + str(obj[4]) + ' ' + str(obj[5])
        print('fulladdress--', fulladdress)
        print(
            'Community, commId, Address, Mission, MissionType, City, CommunityType, longitude,latitude, Website,Cec_status,legislative_district')

        print('-feature row-', obj[0], obj[1], fulladdress, obj[7], obj[8], obj[4], obj[11], obj[13], obj[14], obj[12],
              obj[15], obj[9])
        feature = feature_from_row(obj[0], obj[1], str(fulladdress), obj[7], obj[8], obj[4], obj[11], obj[13], obj[14],
                                   obj[12], obj[15], obj[9])
        collection['features'].append(feature)
    jsonstring = pd.io.json.dumps(collection)
    logger.info("Community Partners GEOSON is written at output directory" + str(output_filename))
    with open(output_filename, 'w') as output_file:
        output_file.write(format(jsonstring))
    # print('jsonstring--',jsonstring)
    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Partner.geojson').put(Body=format(jsonstring))
    print("Partner GEOJSON file written having total records of " + repr(
        len(commPartnerList)) + " in S3 bucket " + settings.AWS_STORAGE_BUCKET_NAME + " at " + str(currentDT))
    logger.info("Partner GEOJSON file written having total records of " + repr(
        len(commPartnerList)) + " in S3 bucket " + settings.AWS_STORAGE_BUCKET_NAME + " at " + str(currentDT))
else:
    print("Partner GEOJSON file NOT written having total records of " + repr(
        len(commPartnerList)) + " in S3 bucket " + settings.AWS_STORAGE_BUCKET_NAME + " at " + str(currentDT))
    logger.info("Partner GEOJSON file NOT written having total records of " + repr(
        len(commPartnerList)) + " in S3 bucket " + settings.AWS_STORAGE_BUCKET_NAME + " at " + str(currentDT))

cursor.close()
conn.close()