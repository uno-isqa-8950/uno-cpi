from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import psycopg2
from UnoCPI import settings
import os

import Project_GEOJSON,Partner_GEOJSON

sched = BlockingScheduler()
sched1 = BackgroundScheduler()
# Initializing the sql files

logger=logging.getLogger("UNO CPI Application Create MAPS json Batch job")

#
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=1)

def scheduled_job():
    print('This job is ran every day at 1:30 AM CST/ 12:30 AM CDT.')
    project = 'python Project_GEOJSON.py'
    partner = 'python Partner_GEOJSON.py'

    logger.info("Start create project json") 
    print("Start create project geo json script") 
    os.system(project)
    print("End create project geo json script") 
    logger.info("Start create partner json") 
    print("Start create partner geo json script") 
    os.system(partner)
    print("End create partner geo json script")     

sched.start()
