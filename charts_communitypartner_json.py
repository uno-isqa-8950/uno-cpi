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
community_file = os.path.join(dirname,'home/static/charts_json/community_partners.json')

q = "SELECT comm.id, comm.name, legislative_district, community_type_id, type.community_type, " \
    "	cec_partner_status_id, cec.name, miss.mission_area_id, " \
    "(select array_to_string (array (select mission_area_id from partners_communitypartnermission " \
    "	where community_partner_id = comm.id and mission_type = 'Secondary'), ', ') as sec_mission_ids) " \
    "FROM partners_communitypartner comm " \
    "LEFT JOIN partners_communitytype type " \
    "	ON comm.community_type_id = type.id " \
    "LEFT JOIN partners_cecpartnerstatus cec " \
    "	ON comm.cec_partner_status_id = cec.id " \
    "   AND cec.name <> 'Inactive' " \
    "LEFT JOIN partners_communitypartnermission miss " \
    "	ON comm.id = miss.community_partner_id " \
    "	AND mission_type = 'Primary' ;"
cursor.execute(q)
communities = cursor.fetchall()
records = len(communities)
comms = []
for c in communities:
    type = {'community_type_id': c[3], 'community_type_name': c[4]}
    cec_partner = {'cec_partner_status_id': c[5], 'cec_partner_status': c[6]}
    if (c[8]):
        sec_mission_ids = [int(e) for e in c[8].split(', ')]
    else:
        sec_mission_ids = []
    res = {'community_partner_id': c[0], 'community_partner_name': c[1], 'legislative_district': c[2],
           'community_type': type, 'cec_partner': cec_partner,
           'primary_mission_id': c[7], 'secondary_mission_ids': sec_mission_ids}
    comms.append(res)
jsonstring = pd.io.json.dumps(comms)

if records != 0:
    logger.info("Write Community Partner JSON for charts  in output directory")
    with open(community_file, 'w') as output_file:
        output_file.write(format(jsonstring))
#
# #writing into amazon aws s3
# ACCESS_ID=settings.AWS_ACCESS_KEY_ID
# ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
# s3 = boto3.resource('s3',
#          aws_access_key_id=ACCESS_ID,
#          aws_secret_access_key= ACCESS_KEY)
#
# if records == 0:
#     print("Community Partner JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
#     logger.info("Community Partner JSON for charts NOT written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
# else:
#     s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json').put(Body=format(jsonstring))
#     print("Community Partner JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
#     logger.info("Community Partner JSON for charts written having total records of " +repr(records)+" in S3 bucket "+settings.AWS_STORAGE_BUCKET_NAME +" at " +str(currentDT))
#
