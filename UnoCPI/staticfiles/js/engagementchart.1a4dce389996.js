var not_set = [undefined, "All", ''];
var engagementList = JSON.parse(document.getElementById('engagementList').textContent);
var Projects = JSON.parse(document.getElementById('Projects').textContent);
var CommunityPartners = JSON.parse(document.getElementById('CommunityPartners').textContent);
var CampusPartners = JSON.parse(document.getElementById('CampusPartners').textContent);

function get_filter_set (Projects, CommunityPartners, CampusPartners, academic_year, mission, comm_type, college_name, campus_partner, weitz_cec_part) {
    if (!not_set.includes(academic_year)) {
        var Projects = Projects.filter(d => d.years.includes(parseInt(academic_year)));
    }
    if (!not_set.includes(mission)) {
        var Projects = Projects.filter(d => d.primary_mission_area.mission_id === parseInt(mission));
        var CommunityPartners = CommunityPartners.filter(d => d.primary_mission_id === parseInt(mission));
    }
    if (weitz_cec_part == 'CURR_CAMP') {
        var CampusPartners = CampusPartners.filter(d => d.cec_partner.cec_partner_status === "Current");
    }
    if (weitz_cec_part == 'FORMER_CAMP') {
        var CampusPartners = CampusPartners.filter(d => d.cec_partner.cec_partner_status === "Former");
    }
    if (!not_set.includes(college_name)) {
        var CampusPartners = CampusPartners.filter(d => d.college.college_name_id === parseInt(college_name));
    }
    if (!not_set.includes(campus_partner)) {
        var CampusPartners = CampusPartners.filter(d => d.campus_partner_id === parseInt(campus_partner));
    }
    if (!not_set.includes(college_name) || !not_set.includes(campus_partner) || ['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        camps = [];
        CampusPartners.forEach(function (feature) {
            camps.push(feature["campus_partner_id"]);
        })
        var Projects = Projects.filter(d => d.campus_partner_ids.some(r => camps.includes(r)));
    }
    if (!not_set.includes(comm_type)) {
        var CommunityPartners = CommunityPartners.filter(d => d.community_type.community_type_id === parseInt(comm_type));
    }
    if (weitz_cec_part == 'CURR_COMM') {
        var CommunityPartners = CommunityPartners.filter(d => d.cec_partner.cec_partner_status === "Current");
    }
    if (weitz_cec_part == 'FORMER_COMM') {
        var CommunityPartners = CommunityPartners.filter(d => d.cec_partner.cec_partner_status === "Former");
    }
    if (!not_set.includes(comm_type) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        comms = [];
        CommunityPartners.forEach(function (feature) {
            comms.push(feature["community_partner_id"]);
        })
        var Projects = Projects.filter(d => d.community_partner_ids.some(r => comms.includes(r)));
    }

    var projectCommunities = new Set();
    Projects.forEach(function (feature) {
        if (feature["community_partner_ids"].length != 0) {
            feature["community_partner_ids"].forEach(item => projectCommunities.add(item));
        }
    })
    var CommunityPartners = CommunityPartners.filter(d => projectCommunities.has(d.community_partner_id));

    if (!not_set.includes(mission)) {
        var Projects = Projects.filter(d => d.primary_mission_area.mission_id === parseInt(mission));
        var CommunityPartners = CommunityPartners.filter(d => d.primary_mission_id === parseInt(mission));
    }

    var projectCampus = new Set();
    Projects.forEach(function (feature) {
        feature["campus_partner_ids"].forEach(item => projectCampus.add(item));
    })
    var CampusPartners = CampusPartners.filter(d => projectCampus.has(d.campus_partner_id));

    return [Projects, CommunityPartners, CampusPartners];
}

function getChartData(engagementList, Projects, CommunityPartners, CampusPartners, academic_year, mission, comm_type, college_name, campus_partner, weitz_cec_part) {
    var proj_data = [];
    var comm_data = [];
    var camp_data = [];
    var engagements = [];
    for (e in engagementList) {
        var engLabel = '';
        var engLabel = engLabel.concat('<span tabindex="-1" data-toggle="tooltip" data-placement="right" title="',engagementList[e].description,'" class="float" > <i class="fa fa-info-circle fa-align-top" aria-hidden="true"></i></span> ',engagementList[e].name);
        engagements.push(engLabel);
        var EngProjects = Projects.filter(d => d.engagement_type.engagement_type_id === parseInt(engagementList[e].id));

        var filt = get_filter_set(EngProjects, CommunityPartners, CampusPartners, academic_year, mission, comm_type, college_name, campus_partner, weitz_cec_part);
        var projs = filt[0];
        var community = filt[1];
        var campus = filt[2];
        proj_data.push(projs.length);
        comm_data.push(community.length);
        camp_data.push(campus.length);
    }
    var max = Math.max(...proj_data.concat(comm_data.concat(camp_data))) +5;

    return [engagements, proj_data, comm_data, camp_data, max];
}

var defaultYrID = JSON.parse(document.getElementById('defaultYrID').textContent);

var res = getChartData(engagementList, Projects, CommunityPartners, CampusPartners, defaultYrID, '', '', '', '', '');
var engagements = res[0];
var proj_data = res[1];
var comm_data = res[2];
var camp_data = res[3];
var max = res[4];

var chart = Highcharts.chart('container',{
   "chart":{"type":"bar"},
   "title":{"text":""},
   "xAxis":{
      "title":{"text":"Engagement Types",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px", "fontFamily": "Arial Narrow"}},
      "categories": engagements,
      "labels":{"useHTML": true, "style":{"color":"black","fontSize":"13px", "fontFamily": "Arial Narrow"}}},
   "yAxis":{
      "allowDecimals":false,
      "title":{
         "text":"Projects/Partners",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px", "fontFamily": "Arial Narrow"}},
      "min":0,
      "max":max},
   "plotOptions":{
      "bar":{"dataLabels":{"enabled":"true","style":{"fontSize":"10px", "fontFamily": "Arial Narrow"}}}},
   "legend":{
      "layout":"horizontal",
      "align":"right",
      "verticalAlign":"top",
      "x":-40, "y":-5,
      "borderWidth":1,
      "backgroundColor":"#FFFFFF",
      "shadow":"true",
      "itemStyle": {"fontFamily": "Arial Narrow"}},
   "series":[
      {"name":"Projects","data": proj_data,"color":"teal"},
      {"name":"Community Partners","data": comm_data,"color":"turquoise"},
      {"name":"Campus Partners","data": camp_data,"color":"blue"}]
});

function updateChart () {
    var academic_year = $('#id_academic_year option:selected').val();
    var mission = $('#id_mission option:selected').val();
    var comm_type = $('#id_community_type option:selected').val();
    var college_name = $('#id_college_name option:selected').val();
    var campus_partner = $('#id_campus_partner option:selected').val();
    var weitz_cec_part = $('#id_weitz_cec_part option:selected').val();
    if (academic_year == '') {
        var academic_year = defaultYrID;
    }
    var res = getChartData(engagementList, Projects, CommunityPartners, CampusPartners, academic_year, mission, comm_type, college_name, campus_partner, weitz_cec_part);
    var proj_data = res[1];
    var comm_data = res[2];
    var camp_data = res[3];
    var max = res[4];

    chart.update({"series":[ {"data": proj_data}, {"data": comm_data}, {"data": camp_data}],
                    "yAxis":{"max":max}});
}

function updateCampus() {
    var allCamps = JSON.parse(document.getElementById('campus_filter').textContent);
    var college_name = $('#id_college_name option:selected').val();
    if (!not_set.includes(college_name)) {
        var campus_filter = allCamps.filter(d => d.college === parseInt(college_name));
    } else {
        var campus_filter = allCamps;
    }
    var select = document.getElementById("id_campus_partner");
    select.options.length = 0;
    select.options[select.options.length] = new Option('All', 'All');
    for(campus in campus_filter) {
        select.options[select.options.length] = new Option(campus_filter[campus].name, campus_filter[campus].id);
    }
}