import sys
import psycopg2
import json
import csv

conn = psycopg2.connect("dbname = 'CPI_DEV' user = 'postgres' host = 'localhost' password = 'horcrux'")
cursor = conn.cursor()

q = "select cp.id, count(distinct pcp.project_name_id) as project_count, count(distinct pps.sub_category_id) as score " \
    "from partners_communitypartner cp " \
    "left join projects_projectcommunitypartner pcp " \
    "on cp.id = pcp.community_partner_id " \
    "left join projects_projectsubcategory pps " \
    "on pcp.project_name_id = pps.project_name_id " \
    "group by cp.id"
cursor.execute(q)
projects = cursor.fetchall()
# print(projects)
# ruhi_partners = []
# for p in projects:
#     ruhi_partners.append(p[0])
# print(ruhi_partners)

x = [505, 508, 504, 503, 507]
partner_data = []

json_data = []
for p in projects:
    if (p[0] in x):
        res = {'name': 'woop', 'x': p[1], 'y': p[2]}
        json_data.append(res)
# json_data = json.dumps(json_data)
d1 = {'name': 'm1', 'data': json_data}

json_data1 = []
for p in projects:
    if (p[0] in x):
        res = {'name': 'boop', 'x': p[1], 'y': p[2]}
        json_data1.append(res)
d2 = {'name': 'm2', 'data': json_data1}


partner_data.append(d1)
partner_data.append(d2)
print(partner_data)
#
# for p in partner_data:
#     x = [mission for mission, data in p.items()]
#     y = [data for mission, data in p.items()]
#     print (x,y)

