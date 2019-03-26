tables_sql = "SELECT table_schema || '.' || table_name "\
           "FROM information_schema.tables "\
           "WHERE table_type = 'BASE TABLE' "\
           "AND table_schema NOT IN ('pg_catalog', 'information_schema');"


all_projects_sql = "SELECT project_name FROM projects_project;"

drop_temp_table_all_projects_start_and_end_dates_sql = "DROP TABLE all_projects_start_and_end_dates"

start_and_end_dates_temp_table_sql = """CREATE TEMP TABLE all_projects_start_and_end_dates AS (
	select p3.id
		,start_date
		,end_date
		,case 
			when EXTRACT(YEAR FROM start_date) <> EXTRACT(YEAR FROM current_date) then 'Inactive'
			when EXTRACT(YEAR FROM start_date) =  EXTRACT(YEAR FROM current_date) 
			and EXTRACT(MONTH FROM start_date) >  EXTRACT(MONTH FROM current_date) then 'Inactive'	 
			when 
			(EXTRACT(YEAR FROM start_date) =  EXTRACT(YEAR FROM current_date) and EXTRACT(MONTH FROM start_date) <=  EXTRACT(MONTH FROM current_date))
				AND
			(EXTRACT(YEAR FROM   end_date) =  EXTRACT(YEAR FROM current_date) and EXTRACT(MONTH FROM   end_date)  >  EXTRACT(MONTH FROM current_date)) 
			then 'Active'
		end proj_status
	from 
			(select p2.id
				,cast ((cast(end_year as varchar(4))||'-'||cast(start_month as varchar(4))||'-'||'1') as date) start_date
				,cast ((cast(end_year as varchar(4))||'-'||cast(end_month as varchar(4))||'-'||'31') as date) end_date
			from
				(select p1.*
					,case
						when start_month = 1 then cast((substring(academic_year,1,4)) as integer)+1 
						when start_month = 6 then cast((substring(academic_year,1,4)) as integer)+1 
						when start_month = 8 then cast((substring(academic_year,1,4)) as integer) 
					end end_year
				from
					(select p.id
						,p.semester
						,ay.academic_year
						,case 
							when semester like 'Fall%' then 8
							when semester like 'Spring%' then 1
							when semester like 'Summer%' then 6 
						end start_month
						,case 
							when semester like 'Fall%' then 12
							when semester like 'Spring%' then 5
							when semester like 'Summer%' then 7 
						end end_month
					FROM public.projects_project p
						inner join projects_academicyear ay on p.academic_year_id = ay.id
					)p1
				)p2
			)p3
);"""



comm_partners_to_be_set_to_active ="""select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = 'Active'
order by p.community_partner_id"""

comm_partners_to_be_set_to_inactive ="""select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = ''
order by p.community_partner_id"""

update_comm_partner_to_inactive_sql = """
--UPDATE COMMUNITY PARTNER WHEN TIED TO A INACTIVE PROJECTS ONLY TO FALSE (INACTIVE)
UPDATE public.partners_communitypartner SET active = FALSE WHERE id in
(select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = ''
order by p.community_partner_id
)
;"""

update_comm_partner_to_active_sql = """
--UPDATE COMMUNITY PARTNER WHEN TIED TO A BOTH ACTIVE and/or INACTIVE or JUST ACTIVE PROJECTS ONLY TO TRUE (ACTIVE)
UPDATE public.partners_communitypartner SET active = TRUE WHERE id in
(select community_partner_id
from
	(-- ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT
	select distinct community_partner_id
		,max(case when proj_status = 'Active' then proj_status end) active_prj
		,max(case when proj_status = 'Inactive' then proj_status end) inactive_prj
	from    
		--ALL COMMUNITY PARTNERS ATTACHED TO A PROJECT ACTIVE AND/OR INACTIVE
		(select distinct cp.community_partner_id
			,p.project_name
			,cp1.name as comm_partner_name
			,p4.id as project_id
			,p4.start_date
			,p4.end_date
			,cp1.active
			,p4.proj_status
		from all_projects_start_and_end_dates p4
			INNER JOIN public.projects_project p on p.id = p4.id
			INNER JOIN public.projects_projectcommunitypartner cp on p4.id = cp.project_name_id
			INNER JOIN public.partners_communitypartner cp1 on cp1.id = cp.community_partner_id
		)p
	group by p.community_partner_id
)p
where coalesce(active_prj,'') = 'Active'
order by p.community_partner_id)
;"""

update_project_to_inactive_sql = """
--UPDATE PROJECT STATUS TO COMPLETED
UPDATE public.projects_project SET status_id = 2 WHERE id in
(select p.id 
from all_projects_start_and_end_dates p
where proj_status = 'Inactive'
)
; """

update_project_to_active_sql = """
--UPDATE PROJECT STATUS TO ACTIVE
UPDATE public.projects_project SET status_id = 1 WHERE id in
(select p.id 
from all_projects_start_and_end_dates p
where proj_status = 'Active'
)
; """
