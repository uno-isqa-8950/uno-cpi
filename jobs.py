from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

import psycopg2
from UnoCPI import sqlfiles,settings
import os

import Project_GEOJSON,Partner_GEOJSON

sched = BlockingScheduler()
sched1 = BackgroundScheduler()
# Initializing the sql files
sql = sqlfiles


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=22)

def scheduled_job():
    print('This job runs every day at 10 PM.')
    os.system(Project_GEOJSON)
    os.system(Partner_GEOJSON)
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

        # create a temp table with all projects start and end dates
        cursor.execute(sql.start_and_end_dates_temp_table_sql)

        # fetch all community partners to be set to inactive
        # cursor.execute(sql.comm_partners_to_be_set_to_inactive)
        #
        # inactive_comm_partners = cursor.fetchall()
        # print("Here is the list of all projects to be set to inactive", "\n")
        # loop to print all the data
        # for i in inactive_comm_partners:
        #     print(i)

        # fetch all community partners to be set to active
        # cursor.execute(sql.comm_partners_to_be_set_to_active)
        #
        # active_comm_partners = cursor.fetchall()
        # print("Here is the list of all projects to be set to active", "\n")
        # loop to print all the data
        # for i in active_comm_partners:
        #     print(i)

        # UPDATE PROJECT STATUS TO ACTIVE
        cursor.execute(sql.update_project_to_active_sql)

        # UPDATE PROJECT STATUS TO COMPLETED
        cursor.execute(sql.update_project_to_inactive_sql)

        # UPDATE PROJECT STATUS TO COMPLETED
        cursor.execute(sql.update_project_to_pending_sql)

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