from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import psycopg2
from UnoCPI import sqlfiles,settings
import os

# import charts_campuspartner_json,charts_communitypartner_json,charts_missionsubcat_json,charts_project_json

sched = BlockingScheduler()
sched1 = BackgroundScheduler()

logger=logging.getLogger("UNO CPI Application Charts Batch job")

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=6)

def scheduled_job():
    print('This job is run every Sunday at 4 AM GMT/ 11 PM CDT.')
    projectScript = 'python charts_project_json.py'
    communityScript = 'python charts_communitypartner_json.py'
    campusScript = 'python charts_campuspartner_json.py'
    missionScript = 'python charts_missionsubcat_json.py'

    print("Start project script")
    os.system(projectScript)
    print("End project script")
    print("Start community script")
    os.system(communityScript)
    print("End community script")
    print("Start campus script")
    os.system(campusScript)
    print("End campus script")
    print("Start mission script")
    os.system(missionScript)
    print("End mission script")
sched.start()
