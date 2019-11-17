from UnoCPI import sqlfiles,settings
import psycopg2
import os

sql = sqlfiles
global connection
global cursor
try:
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  host='localhost',
                                  #host=settings.DATABASES['default']['HOST'],
                                  port=settings.DATABASES['default']['PORT'],
                                  database=settings.DATABASES['default']['NAME'])
                                  #sslmode="require")

    if connection:
        print("Postgres SQL Database successful connection")

    cursor = connection.cursor()

    print("Executing Community Partner status inactive")

    #UPDATE Community partner to show status 'Inactive' from newly added Partner Status Table
    update_comm_partner_status_to_inactive_from_table= """Update partners_communitypartner
                                                          Set partner_status_id =(select id from partners_partnerstatus
                                                          where name = 'Inactive')
                                                          Where id in (select id
                                                          from partners_communitypartner
                                                          where not active);"""


    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_status_to_inactive_from_table)
    connection.commit()
    print("Completed Community Partner status inactive")


    print("Executing Community Partner status active")
    #UPDATE Community partner to show status 'Active' from newly added Partner Status Table
    update_comm_partner_status_to_active_from_table= """Update partners_communitypartner
                                                          Set partner_status_id =(select id from partners_partnerstatus
                                                          where name = 'Active')
                                                          Where id in (select id
                                                          from partners_communitypartner
                                                          where active);"""


    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_status_to_active_from_table)
    connection.commit()
    print("Completed Community Partner status active")


    print("Executing Campus Partner status inactive")
    #UPDATE Community partner to show status 'Inactive' from newly added Partner Status Table
    update_campus_partner_status_to_inactive_from_table= """Update partners_campuspartner
                                                          Set partner_status_id =(select id from partners_partnerstatus
                                                          where name = 'Inactive')
                                                          Where id in (select id
                                                          from partners_campuspartner
                                                          where not active);"""


    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_status_to_inactive_from_table)
    connection.commit()
    print("Completed Campus Partner status inactive")


    print("Executing Campus Partner status Active")
    #UPDATE Community partner to show status 'Inactive' from newly added Partner Status Table
    update_campus_partner_status_to_active_from_table= """Update partners_campuspartner
                                                          Set partner_status_id =(select id from partners_partnerstatus
                                                          where name = 'Active')
                                                          Where id in (select id
                                                          from partners_campuspartner
                                                          where active);"""


    # create a temp table with all projects start and end dates
    cursor.execute(update_campus_partner_status_to_active_from_table)
    connection.commit()
    print("completed Campus Partner status Active")


    print("Executing Community Partner CEC status Current")

    # UPDATE Community partner to show status 'Current' from newly added Partner Status Table
    update_comm_partner_cec_status_to_current_from_table = """Update partners_communitypartner
                                                              Set cec_partner_status_id =(select id from partners_cecpartnerstatus
                                                              where name = 'Current')
                                                              Where id in (select id
                                                              from partners_communitypartner
                                                              where weitz_cec_part='Yes');"""

    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_cec_status_to_current_from_table)
    connection.commit()
    print("Completed Community Partner CEC status Current")

    print("Executing Community Partner CEC status Former")
    # UPDATE Community partner to show status 'Active' from newly added Partner Status Table
    update_comm_partner_cec_status_to_former_from_table = """Update partners_communitypartner
                                                              Set cec_partner_status_id =(select id from partners_cecpartnerstatus
                                                              where name = 'Never')
                                                              Where id in (select id
                                                              from partners_communitypartner
                                                              where weitz_cec_part='No');"""

    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_cec_status_to_former_from_table)
    connection.commit()
    print("Completed Community Partner CEC status Former")

    print("Executing Campus Partner CEC status Current")

    # UPDATE Community partner to show status 'Current' from newly added Partner Status Table
    update_comm_partner_cec_status_to_current_from_table = """Update partners_campuspartner
                                                              Set cec_partner_status_id =(select id from partners_cecpartnerstatus
                                                              where name = 'Current')
                                                              Where id in (select id
                                                              from partners_campuspartner
                                                              where weitz_cec_part='Yes');"""

    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_cec_status_to_current_from_table)
    connection.commit()
    print("Completed Campus Partner CEC status Current")

    print("Executing Camous Partner CEC status Former")
    # UPDATE Community partner to show status 'Active' from newly added Partner Status Table
    update_comm_partner_cec_status_to_former_from_table = """Update partners_campuspartner
                                                              Set cec_partner_status_id =(select id from partners_cecpartnerstatus
                                                              where name = 'Never')
                                                              Where id in (select id
                                                              from partners_campuspartner
                                                              where weitz_cec_part='No');"""

    # create a temp table with all projects start and end dates
    cursor.execute(update_comm_partner_cec_status_to_former_from_table)
    connection.commit()
    print("Completed Campus Partner CEC status Former")
    # drop all_projects_start_and_end_date temp table
    # cursor.execute(sql.drop_temp_table_all_projects_start_and_end_dates_sql)

except (psycopg2.Error) as error:
    print("Error while connecting to Postgres SQL", error)
# finally:
#     # closing database connection.
#     if connection:
#         connection.commit()
#         # drop all_projects_start_and_end_date temp table
#         cursor.execute(sql.drop_temp_table_all_projects_start_and_end_dates_sql)
cursor.close()
connection.close()
print("Postgres SQL connection is closed")