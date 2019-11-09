function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

var engagement_type = getUrlVars()["engagement_type"];
var legislative_value = getUrlVars()["legislative_value"];
var k12_flag = getUrlVars()["k12_flag"];
var mission = getUrlVars()["mission"];
var comm_type = getUrlVars()["community_type"];
var college_name = getUrlVars()["college_name"];
var campus_partner = getUrlVars()["campus_partner"];
// var weitz_cec_part = getUrlVars()["weitz_cec_part"];
var not_set = [undefined, "All", ''];

var yearList = JSON.parse(document.getElementById('yearList').textContent);
var CommunityPartners = JSON.parse(document.getElementById('CommunityPartners').textContent);
var Projects = JSON.parse(document.getElementById('Projects').textContent);
var CampusPartners = JSON.parse(document.getElementById('CampusPartners').textContent);

if (!not_set.includes(engagement_type)) {
    var Projects = Projects.filter(d => d.engagement_type.engagement_type_id === parseInt(engagement_type));
}
if (!not_set.includes(mission)) {
    var Projects = Projects.filter(d => d.primary_mission_area.mission_id === parseInt(mission));
    var CommunityPartners = CommunityPartners.filter(d => d.primary_mission_id === parseInt(mission));
}

if (!not_set.includes(legislative_value)) {
    var Projects = Projects.filter(d => d.legislative_district === parseInt(legislative_value.split("+")[2]));
}
if (k12_flag === 'Yes') {
    var Projects = Projects.filter(d => d.k12_flag === true);
} else if (k12_flag === 'No') {
    var Projects = Projects.filter(d => d.k12_flag === false);
}

if (!not_set.includes(college_name)) {
    var CampusPartners = CampusPartners.filter(d => d.college.college_name_id === parseInt(college_name));
}
if (!not_set.includes(campus_partner)) {
    var CampusPartners = CampusPartners.filter(d => d.campus_partner_id === parseInt(campus_partner));
}
if (!not_set.includes(college_name) || !not_set.includes(campus_partner)) {
   camps = [];
   CampusPartners.forEach(function(feature) {camps.push(feature["campus_partner_id"]);})
   var Projects = Projects.filter(d => d.campus_partner_ids.some(r => camps.includes(r)));
}

if (!not_set.includes(comm_type)) {
    var CommunityPartners = CommunityPartners.filter(d => d.community_type.community_type_id === parseInt(comm_type));
    comms = [];
    CommunityPartners.forEach(function(feature) {comms.push(feature["community_partner_id"]);})
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

if (!not_set.includes(engagement_type) || !not_set.includes(legislative_value) || !not_set.includes(k12_flag) || !not_set.includes(college_name) || !not_set.includes(campus_partner)) {
    var CommunityPartners = CommunityPartners.filter(d => projectCommunities.has(d.community_partner_id));
}
if (!not_set.includes(mission) || !not_set.includes(engagement_type) || !not_set.includes(legislative_value) || !not_set.includes(k12_flag) || !not_set.includes(comm_type)) {
    var CampusPartners = CampusPartners.filter(d => projectCampus.has(d.campus_partner_id));
}

var proj_data = [];
var comm_data = [];
var camp_data = [];
var yrs = [];
for (y in yearList) {
    yrs.push(yearList[y].name);
    var projs = Projects.filter(d => d.years.includes(yearList[y].id));
    proj_data.push(projs.length);
    var comms = new Set();
    var camps = new Set();
    projs.forEach(function(feature) {
        if (feature["community_partner_ids"].length != 0) {
            feature["community_partner_ids"].forEach(item => comms.add(item));
        }
        feature["campus_partner_ids"].forEach(item => camps.add(item));
    })
    comm_data.push(comms.size);
    camp_data.push(camps.size);
}

var project_count_series = {
    'name': 'Project Count',
    'data': proj_data,
    'color': 'turquoise'};
var community_partner_count_series = {
    'name': 'Community Partner Count',
    'data': comm_data,
    'color': 'teal'};
var campus_partner_count_series = {
    'name': 'Campus Partner Count',
    'data': camp_data,
    'color': 'blue'};

Highcharts.chart('container',
    {"title":{"text":""},
   "xAxis":{
      "categories": yrs,
      "title":{
         "text":"Academic Years",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px"}}},
   "yAxis":{
      "title":{
         "text":"Projects/Partners",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px"}}},
   "plotOptions":{
      "series":{
         "dataLabels":{
            "style":{"fontSize":"8px"}}}},
   "series":[project_count_series, community_partner_count_series, campus_partner_count_series],
   "legend":{
      "layout":"horizontal",
      "align":"right",
      "verticalAlign":"top",
      "x":-10,
      "y":50,
      "borderWidth":1,
      "backgroundColor":"#FFFFFF",
      "shadow":"true"},
   "responsive":{
      "rules":[{
        "condition":{"maxWidth":500},
        "chartOptions":{
           "legend":{"layout":"horizontal","align":"center","verticalAlign":"bottom"}}}]}
});
