from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import psycopg2
from UnoCPI import sqlfiles,settings
import os

import Update_Partner, Update_Project

sched = BlockingScheduler()
sched1 = BackgroundScheduler()
# Initializing the sql files
sql = sqlfiles
logger=logging.getLogger("UNO CPI Application update database Batch job")

#
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=3)

def scheduled_job():
    print('This job is ran every Sunday at 4 AM GMT/ 11 PM CDT.')
    updateProject = 'python Update_Project.py'

    updatePartner = 'python Update_Partner.py'

    logger.info("Start update project script") 
    print("Start update project script") 
    os.system(updateProject)
    print("End update project script")

    print("Start update partner script") 
    os.system(updatePartner)
    print("End update partner script") 

    global connection
    global cursor

    try:
        connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                      password=settings.DATABASES['default']['PASSWORD'],
                                      host=settings.DATABASES['default']['HOST'],
                                      port=settings.DATABASES['default']['PORT'],
                                      database=settings.DATABASES['default']['NAME'],
                                      sslmode="require")

        if connection:
            print("Postgres SQL Database successful connection")

        cursor = connection.cursor()
        cursor.close()
        connection.close()

        # create a temp table with all projects start and end dates
        #cursor.execute(sql.start_and_end_dates_temp_table_sql)

        # UPDATE PROJECT STATUS TO ACTIVE
        #cursor.execute(sql.update_project_to_active_sql)
        #connection.commit()

        # UPDATE PROJECT STATUS TO COMPLETED
        #cursor.execute(sql.update_project_to_inactive_sql)
        #connection.commit()

        # UPDATE PROJECT STATUS TO PENDING
        #cursor.execute(sql.update_project_to_pending_sql)
        #connection.commit()

        # UPDATE COMMUNITY PARTNER WHEN TIED TO A INACTIVE PROJECTS ONLY TO FALSE(INACTIVE)
        #cursor.execute(sql.update_comm_partner_to_inactive_sql)
        #connection.commit()

        # UPDATE  COMMUNITY PARTNER WHEN TIED TO A BOTH ACTIVE
        # and / or INACTIVE or JUST ACTIVE PROJECTS ONLY TO TRUE(ACTIVE)
        #cursor.execute(sql.update_comm_partner_to_active_sql)
        #connection.commit()

        # drop all_projects_start_and_end_date temp table
        # cursor.execute(sql.drop_temp_table_all_projects_start_and_end_dates_sql)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to Postgres SQL", error)
    finally:
        # closing database connection.
        if connection:
            #connection.commit()
            # drop all_projects_start_and_end_date temp table
            #cursor.execute(sql.drop_temp_table_all_projects_start_and_end_dates_sql)
            cursor.close()
            connection.close()
            print("Postgres SQL connection is closed")


sched.start()
