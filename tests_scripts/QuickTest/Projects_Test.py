import unittest
import psycopg2
from UnoCPI import sqlfiles, settings

# Initializing the sql files
sql = sqlfiles


class TestReports(unittest.TestCase):

    def test_reports(self):

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

            # MISSION AREAS REPORT
            cursor.execute(sql.mission_areas_report_sql)

            # ENGAGEMENT TYPES REPORT
            cursor.execute(sql.engagement_types_report_sql)

            # COMMUNITY PARTNERS REPORT
            cursor.execute(sql.comm_part_report_sql)

            # ALL PROJECTS REPORT
            projects = cursor.execute(sql.all_projects_report_sql)
            # loop to print all the data
            for i in projects:
                print(i)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to Postgres SQL", error)
        finally:
            # closing database connection.
            if connection:
                # connection.commit()
                cursor.close()
                connection.close()
                print("Postgres SQL connection is closed")
