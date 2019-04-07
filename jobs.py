from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

import psycopg2
from UnoCPI import sqlfiles,settings
import os

import Project_GEOJSON,Partner_GEOJSON
from UnoCPI.jobs import generateGEOJSON

sched = BlockingScheduler()
sched1 = BackgroundScheduler()
# Initializing the sql files
sql = sqlfiles

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
# sched.add_job(YOURRUNCTIONNAME, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=23)
# @sched.scheduled_job('cron', month='1,6,8', day='1', hour='0')
# @sched.scheduled_job('interval', minutes=5)
@sched1.add_job(generateGEOJSON,'interval', hours=1)


def generateGEOJSON():
    os.system(Partner_GEOJSON)
    os.system(Project_GEOJSON)
    
def scheduled_job():
    print('This job is ran every day at 11pm.')
    # print('This job is ran every 1st day of the month of January, June and August at 12 AM.')
    # print('This job is ran every minute.')

    global connection
    global cursor

    try:
        # CAT STAGING
        connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                              password=settings.DATABASES['default']['PASSWORD'],
                              host=settings.DATABASES['default']['HOST'],
                              port=settings.DATABASES['default']['PORT'],
                              database=settings.DATABASES['default']['NAME'],
                              sslmode="require")



        if connection:
            print("Postgres SQL Database successful connection")

        cursor = connection.cursor()

        # create a temp table with all projects start and end dates
        cursor.execute(sql.start_and_end_dates_temp_table_sql)

        # fetch all community partners to be set to inactive
        cursor.execute(sql.comm_partners_to_be_set_to_inactive)

        inactive_comm_partners = cursor.fetchall()
        print("Here is the list of all projects to be set to inactive", "\n")
        # loop to print all the data
        for i in inactive_comm_partners:
            print(i)

        # fetch all community partners to be set to active
        cursor.execute(sql.comm_partners_to_be_set_to_active)

        active_comm_partners = cursor.fetchall()
        print("Here is the list of all projects to be set to active", "\n")
        # loop to print all the data
        for i in active_comm_partners:
            print(i)

        # UPDATE PROJECT STATUS TO ACTIVE
        cursor.execute(sql.update_project_to_active_sql)

        # UPDATE PROJECT STATUS TO COMPLETED
        cursor.execute(sql.update_project_to_inactive_sql)

        # UPDATE COMMUNITY PARTNER WHEN TIED TO A INACTIVE PROJECTS ONLY TO FALSE(INACTIVE)
        cursor.execute(sql.update_comm_partner_to_inactive_sql)

        # UPDATE  COMMUNITY PARTNER WHEN TIED TO A BOTH ACTIVE
        # and / or INACTIVE or JUST ACTIVE PROJECTS ONLY TO TRUE(ACTIVE)
        cursor.execute(sql.update_comm_partner_to_active_sql)

        # drop all_projects_start_and_end_date temp table
        cursor.execute(sql.drop_temp_table_all_projects_start_and_end_dates_sql)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to Postgres SQL", error)
    finally:
        # closing database connection.
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("Postgres SQL connection is closed")
            

sched.start()
sched1.start()
