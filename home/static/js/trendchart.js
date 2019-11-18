function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

var engagement_type = getUrlVars()["engagement_type"];
var mission = getUrlVars()["mission"];
var comm_type = getUrlVars()["community_type"];
var college_name = getUrlVars()["college_name"];
var campus_partner = getUrlVars()["campus_partner"];
var weitz_cec_part = getUrlVars()["weitz_cec_part"];
var not_set = [undefined, "All", ''];

var yearList = JSON.parse(document.getElementById('yearList').textContent);
var Projects = JSON.parse(document.getElementById('Projects').textContent);
var CommunityPartners = JSON.parse(document.getElementById('CommunityPartners').textContent);
var CampusPartners = JSON.parse(document.getElementById('CampusPartners').textContent);

function get_filter_set (Projects, CommunityPartners, CampusPartners, engagement_type, mission, comm_type, college_name, campus_partner, weitz_cec_part) {
    if (!not_set.includes(engagement_type)) {
        var Projects = Projects.filter(d => d.engagement_type.engagement_type_id === parseInt(engagement_type));
    }
    if (!not_set.includes(mission)) {
        var Projects = Projects.filter(d => d.primary_mission_area.mission_id === parseInt(mission));
        var CommunityPartners = CommunityPartners.filter(d => d.primary_mission_id === parseInt(mission));
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
    if (!not_set.includes(comm_type) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        comms = [];
        CommunityPartners.forEach(function (feature) {
            comms.push(feature["community_partner_id"]);
        })
        var Projects = Projects.filter(d => d.community_partner_ids.some(r => comms.includes(r)));
    }
    var projectCommunities = new Set();
    var projectCampus = new Set();
    Projects.forEach(function (feature) {
        if (feature["community_partner_ids"].length != 0) {
            feature["community_partner_ids"].forEach(item => projectCommunities.add(item));
        }
        feature["campus_partner_ids"].forEach(item => projectCampus.add(item));
    })
    var CommunityPartners = CommunityPartners.filter(d => projectCommunities.has(d.community_partner_id));
    var CampusPartners = CampusPartners.filter(d => projectCampus.has(d.campus_partner_id));
    return [Projects, CommunityPartners, CampusPartners];
}

var proj_data = [];
var comm_data = [];
var camp_data = [];
var yrs = [];
if (not_set.includes(weitz_cec_part)) {
    for (y in yearList) {
        yrs.push(yearList[y].name);
        var YrProjects = Projects.filter(d => d.years.includes(yearList[y].id));
        var filt = get_filter_set (YrProjects, CommunityPartners, CampusPartners, engagement_type, mission, comm_type, college_name, campus_partner, weitz_cec_part);
        var projs = filt[0];
        var community = filt[1];
        var campus = filt[2];
        proj_data.push(projs.length);
        comm_data.push(community.length);
        camp_data.push(campus.length);
    }
} else {
    for (y in yearList) {
        var yrID = yearList[y].id;
        yrs.push(yearList[y].name);
        var index = yearList.map(function(o) { return o.id; }).indexOf(yrID);
        var yrArr = [];
        for (var i = 0; i < index; i++) {
            yrArr.push(yearList[i].id);
        }
        if (['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
            if (weitz_cec_part == 'CURR_COMM') {
                var CECCommunityPartners = CommunityPartners.filter(d => d.cec_partner.cec_years.includes(yrID));
                console.log(CECCommunityPartners.length);
            } else if (weitz_cec_part == 'FORMER_COMM') {
                var CECCommunityPartners = CommunityPartners.filter(d => !d.cec_partner.cec_years.includes(yrID)).filter(d => d.cec_partner.cec_years.some(r=> yrArr.includes(r)));
                console.log(CECCommunityPartners.length);
            }
            var projs = Projects.filter(d => d.years.includes(yearList[y].id));
            var filt = get_filter_set (projs, CECCommunityPartners, CampusPartners, engagement_type, mission, comm_type, college_name, campus_partner, weitz_cec_part);
        }
        if (['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
            if (weitz_cec_part == 'CURR_CAMP') {
                var CECCampusPartners = CampusPartners.filter(d => d.cec_partner.cec_years.includes(yrID));
            } else if (weitz_cec_part == 'FORMER_CAMP') {
                var CECCampusPartners = CampusPartners.filter(d => !d.cec_partner.cec_years.includes(yrID)).filter(d => d.cec_partner.cec_years.some(r => yrArr.includes(r)));
            }
            var projs = Projects.filter(d => d.years.includes(yearList[y].id));
            var filt = get_filter_set (projs, CommunityPartners, CECCampusPartners, engagement_type, mission, comm_type, college_name, campus_partner, weitz_cec_part);
        }
        var projs = filt[0];
        var community = filt[1];
        var campus = filt[2];
        proj_data.push(projs.length);
        comm_data.push(community.length);
        camp_data.push(campus.length);
    }
}

var project_count_series = {
    'name': 'Projects',
    'data': proj_data,
    'color': 'turquoise'};
var community_partner_count_series = {
    'name': 'Community Partners',
    'data': comm_data,
    'color': 'teal'};
var campus_partner_count_series = {
    'name': 'Campus Partners',
    'data': camp_data,
    'color': 'blue'};

Highcharts.chart('container',
    {"title":{"text":""},
   "xAxis":{
      "categories": yrs,
      "title":{
         "text":"Academic Years",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px", "fontFamily": "Arial Narrow"}}},
   "yAxis":{
      "title":{
         "text":"Projects/Partners",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px", "fontFamily": "Arial Narrow"}}},
   "plotOptions":{
      "series":{
         "dataLabels":{
            "style":{"fontSize":"8px"}}}},
   "tooltip": {"split": true, "style": {"fontFamily": "Arial Narrow"}},
   "series":[project_count_series, community_partner_count_series, campus_partner_count_series],
   "legend":{
      "layout":"horizontal",
      "align":"right",
      "verticalAlign":"top",
      "x":-10,
      "y":50,
      "borderWidth":1,
      "backgroundColor":"#FFFFFF",
      "shadow":"true",
      "itemStyle": {"fontFamily": "Arial Narrow"}},
   "responsive":{
      "rules":[{
        "condition":{"maxWidth":500},
        "chartOptions":{
           "legend":{"layout":"horizontal","align":"center","verticalAlign":"bottom"}}}]}
});
