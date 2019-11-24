var not_set = [undefined, "All", ''];
var missionList = JSON.parse(document.getElementById('missionList').textContent);
var CommunityPartners = JSON.parse(document.getElementById('CommunityPartners').textContent);
var Projects = JSON.parse(document.getElementById('Projects').textContent);
var CampusPartners = JSON.parse(document.getElementById('CampusPartners').textContent);

function getChartData (Projects, CommunityPartners, CampusPartners, missionList, engagement_type, academic_year, comm_type, college_name, campus_partner, weitz_cec_part) {
    if (!not_set.includes(engagement_type)) {
        var Projects = Projects.filter(d => d.engagement_type.engagement_type_id === parseInt(engagement_type));
    }
    if (!not_set.includes(academic_year)) {
        var Projects = Projects.filter(d => d.years.includes(parseInt(academic_year)));
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
    var projectCampus = new Set();
    Projects.forEach(function(feature) {
        if (feature["community_partner_ids"].length != 0) {
            feature["community_partner_ids"].forEach(item => projectCommunities.add(item));
        }
        feature["campus_partner_ids"].forEach(item => projectCampus.add(item));
    })

    if (!not_set.includes(engagement_type) || !not_set.includes(academic_year) || !not_set.includes(college_name) || !not_set.includes(campus_partner) || ['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        var CommunityPartners = CommunityPartners.filter(d => projectCommunities.has(d.community_partner_id));
    }
    if (!not_set.includes(engagement_type) || !not_set.includes(academic_year) || !not_set.includes(comm_type) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        var CampusPartners = CampusPartners.filter(d => projectCampus.has(d.campus_partner_id));
    }
    if (not_set.includes(y_axis)) {
       var y_axis = "campus";
    }

    var projSeries = [];
    var communitySeries = [];
    var missionCategories = [];
    for (m in missionList) {
        var missionID = missionList[m].id;
        missionCategories.push(missionList[m].name);
        var projs = Projects.filter(d => d.primary_mission_area.mission_id === parseInt(missionID));
        var comms = CommunityPartners.filter(d => d.primary_mission_id === parseInt(missionID));
        projSeries.push(projs.length);
        communitySeries.push(comms.length);
    }
    var max = Math.max(...projSeries.concat(communitySeries)) +5;

    return [missionCategories, projSeries, communitySeries, max];
}

var defaultYrID = JSON.parse(document.getElementById('defaultYrID').textContent);

var res = getChartData (Projects, CommunityPartners, CampusPartners, missionList, '', defaultYrID, '', '', '', '');
var missionCategories = res[0];
var projSeries = res[1];
var communitySeries = res[2];
var max = res[3];

var chart = Highcharts.chart('container', {
   "chart":{ "type":"bar" },
   "title":{ "text":"" },
   "xAxis":{
      "title":{
         "text":"Focus Areas",
         "style":{ "fontWeight":"bold", "color":"black", "fontSize":"15px" }},
      "categories": missionCategories,
      "labels":{
         "style":{ "color":"black", "fontSize":"13px" }}},
   "yAxis":{
      "allowDecimals":false,
      "title":{
         "text":"Projects/Community Partners ",
         "style":{ "fontWeight":"bold", "color":"black", "fontSize":"15px" }},
      "min":0,
      "max":max},
   "plotOptions":{
      "bar":{
         "dataLabels":{
            "enabled":"true",
            "style":{ "fontSize":"9px" }}}},
   "legend":{
      "layout":"horizontal",
      "align":"right",
      "verticalAlign":"top",
      "x":-10, "y":50,
      "borderWidth":1,
      "backgroundColor":"#FFFFFF",
      "shadow":"true"},
   "series":[
      {"name":"Projects","data": projSeries,"color":"turquoise"},
      {"name":"Community Partners","data": communitySeries,"color":"teal"}
]});


function updateChart () {
    var academic_year = $('#id_academicyear option:selected').val();
    var engagement_type = $('#id_engagement_type option:selected').val();
    var college_name = $('#id_college_name option:selected').val();
    var campus_partner = $('#id_campus_partner option:selected').val();
    var weitz_cec_part = $('#id_weitz_cec_part option:selected').val();
    var comm_type = $('#id_community_type option:selected').val();
    if (academic_year == '') {
        var academic_year = defaultYrID;
    }
    var res = getChartData (Projects, CommunityPartners, CampusPartners, missionList, engagement_type, academic_year, comm_type, college_name, campus_partner, weitz_cec_part);
    var projSeries = res[1];
    var communitySeries = res[2];
    var max = res[3];
    chart.update({"series":[ {"data": projSeries}, {"data": communitySeries}],
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
