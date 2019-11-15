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
cursor = conn.cursor()

dirname = os.path.dirname(__file__)
campus_file = os.path.join(dirname,'home/static/charts_json/campus_partners.json')

q = "SELECT camp.id, camp.name, college_name_id, college_name, uni.name as university, cec_partner_status_id, cec.name," \
    "CASE WHEN cec_partner_status_id in (select id from partners_cecpartnerstatus where name in ('Former', 'Current')) " \
    "	THEN (select (select array_to_string (array (select id from projects_academicyear " \
    "			where id >= start_acad_year_id and (id <= end_acad_year_id or end_acad_year_id is null)), ', ')) " \
    "			from partners_cecpartactiveyrs where camp_partner_id = camp.id) " \
    "	END AS cec_active_yrs " \
    "FROM partners_campuspartner camp " \
    "LEFT JOIN university_college clg " \
    "	ON college_name_id = clg.id " \
    "LEFT JOIN university_university uni " \
    "	ON clg.university_id = uni.id " \
    "LEFT JOIN partners_cecpartnerstatus cec " \
    "	ON camp.cec_partner_status_id = cec.id " \
    "WHERE camp.id in (select distinct campus_partner_id from projects_projectcampuspartner) ;"
cursor.execute(q)
campus = cursor.fetchall()
records = len(campus)
camps = []
for c in campus:
    if (c[7]):
        cec_years = [int(e) for e in c[7].split(', ')]
    else:
        cec_years = []
    college = {'college_name_id': c[2], 'college_name': c[3]}
    cec_partner = {'cec_partner_status_id': c[5], 'cec_partner_status': c[6], 'cec_years':cec_years}
    res = {'campus_partner_id': c[0], 'campus_partner_name': c[1],
           'college': college, 'university': c[4], 'cec_partner': cec_partner}
    camps.append(res)
jsonstring = pd.io.json.dumps(camps)

if records != 0:
    logger.info("Write Projects JSON for charts  in output directory")
    with open(campus_file, 'w') as output_file:
        output_file.write(format(jsonstring))

#writing into amazon aws s3
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

if records == 0:
    print("Campus Partner JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Campus Partner JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
else:
    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json').put(Body=format(jsonstring))
    print("Campus Partner JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
    logger.info("Campus Partner JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))

