import pandas as pd
import json
import datetime
import boto3
import logging
import os
import psycopg2
from UnoCPI import settings

currentDT = datetime.datetime.now()
logger=logging.getLogger("UNO CPI Application")
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
cursor = conn.cursor()

dirname = os.path.dirname(__file__)
project_file = os.path.join(dirname,'home/static/charts_json/projects.json')

q = "SELECT p.id, project_name, legislative_district, k12_flag, pm.mission_id, ma.mission_name, engagement_type_id, " \
    "(select name from projects_engagementtype where id = engagement_type_id) as engagement_type_name, " \
    "(select array_to_string (array (select community_partner_id from projects_projectcommunitypartner " \
    "   where project_name_id = p.id), ', ') as community_partner_ids), " \
    "(select array_to_string (array (select campus_partner_id from projects_projectcampuspartner " \
    "	where project_name_id = p.id), ', ') as campus_partner_ids), " \
    "(select array_to_string (array (select sub_category_id from projects_projectsubcategory " \
    "	where project_name_id = p.id), ', ') as subcategory_ids), " \
    "(select array_to_string (array (select id from projects_academicyear " \
    "	where id >= academic_year_id and (id <= end_academic_year_id or end_academic_year_id is null)), ', ') as yr_ids) " \
    "FROM projects_project p " \
    "LEFT JOIN projects_projectmission pm " \
    "	ON p.id = pm.project_name_id " \
    "	AND mission_type = 'Primary' " \
    "LEFT JOIN home_missionarea ma " \
    "   ON pm.mission_id = ma.id " \
    "WHERE status_id <> (SELECT id FROM projects_status WHERE name = 'Drafts') ;"
cursor.execute(q)
projects = cursor.fetchall()
records = len(projects)
projs = []
for p in projects:
    mission = {'mission_id': p[4], 'mission_name': p[5]}
    engagement = {'engagement_type_id': p[6], 'engagement_type_name': p[7]}
    if (p[8]):
        community_partner_ids = [int(e) for e in p[8].split(', ')]
    else:
        community_partner_ids = []
    if (p[9]):
        campus_partner_ids = [int(e) for e in p[9].split(', ')]
    else:
        campus_partner_ids = []
    if (p[10]):
        subcats = [int(e) for e in p[10].split(', ')]
    else:
        subcats = []
    if (p[11]):
        yrs = [int(e) for e in p[11].split(', ')]
    else:
        yrs = []
    res = {'project_id': p[0], 'project_name': p[1], 'primary_mission_area':mission, 'engagement_type':engagement,'legislative_district': p[2], 'k12_flag': p[3], 'community_partner_ids': community_partner_ids, 'campus_partner_ids': campus_partner_ids, 'subcategories': subcats, 'years':yrs}
    projs.append(res)
jsonstring = pd.io.json.dumps(projs)

if records != 0:
    logger.info("Write Projects JSON for charts  in output directory")
    with open(project_file, 'w') as output_file:
        output_file.write(format(jsonstring))

#writing into amazon aws s3
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

if records == 0:
    print("Projects JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Projects JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
else:
    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json').put(Body=format(jsonstring))
    print("Projects JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Projects JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))

