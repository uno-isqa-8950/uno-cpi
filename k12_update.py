from UnoCPI import sqlfiles,settings
import psycopg2
import os

sql = sqlfiles
global connection
global cursor
try:
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  host=settings.DATABASES['default']['HOST'],
                                  port=settings.DATABASES['default']['PORT'],
                                  database=settings.DATABASES['default']['NAME'])
                                  #sslmode="require")

    if connection:
        print("Postgres SQL Database successful connection")

    cursor = connection.cursor()

    print("Executing Community Partner status inactive")


    update_k12_flag_for_existing_projects= """Update projects_project
                                                          Set k12_flag = 't' 
                                                          Where total_k12_students > 0 or total_k12_hours > 0;"""



    cursor.execute(update_k12_flag_for_existing_projects)
    connection.commit()

except (psycopg2.Error) as error:
    print("Error while connecting to Postgres SQL", error)

cursor.close()
connection.close()
print("Postgres SQL connection is closed")