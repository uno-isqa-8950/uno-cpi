function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

var academic_year = getUrlVars()["academic_year"];
var engagement_type = getUrlVars()["engagement_type"];
var college_name = getUrlVars()["college_name"];
var campus_partner = getUrlVars()["campus_partner"];
var weitz_cec_part = getUrlVars()["weitz_cec_part"];
var comm_type = getUrlVars()["community_type"];
var legislative_value = getUrlVars()["legislative_value"];
var community_partner = getUrlVars()["community_partner"];
var not_set = [undefined, "All", ''];

var missionList = JSON.parse(document.getElementById('missionList').textContent);
var yearList = JSON.parse(document.getElementById('yearList').textContent);
var CommunityPartners = JSON.parse(document.getElementById('CommunityPartners').textContent);
var Projects = JSON.parse(document.getElementById('Projects').textContent);
var CampusPartners = JSON.parse(document.getElementById('CampusPartners').textContent);

if (not_set.includes(academic_year)) {
    var yrID = yearList[yearList.length-1].id;
} else {
    var yrID = parseInt(academic_year);
}
var Projects = Projects.filter(d => d.years.includes(yrID));
var index = yearList.map(function(o) { return o.id; }).indexOf(yrID);
var yrArr = [];
for (var i = 0; i < index; i++) {
    yrArr.push(yearList[i].id);
}
if (!not_set.includes(engagement_type)) {
    var Projects = Projects.filter(d => d.engagement_type.engagement_type_id === parseInt(engagement_type));
}

if (['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
    if (weitz_cec_part == 'CURR_CAMP') {
        var CampusPartners = CampusPartners.filter(d => d.cec_partner.cec_years.includes(yrID));
    } else if (weitz_cec_part == 'FORMER_CAMP') {
        var CampusPartners = CampusPartners.filter(d => !d.cec_partner.cec_years.includes(yrID)).filter(d => d.cec_partner.cec_years.some(r => yrArr.includes(r)));
    }
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

if (['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
    if (weitz_cec_part == 'CURR_COMM') {
        var CommunityPartners = CommunityPartners.filter(d => d.cec_partner.cec_years.includes(yrID));
    } else if (weitz_cec_part == 'FORMER_COMM') {
        var CommunityPartners = CommunityPartners.filter(d => !d.cec_partner.cec_years.includes(yrID)).filter(d => d.cec_partner.cec_years.some(r=> yrArr.includes(r)));
    }
}
if (!not_set.includes(comm_type)) {
    var CommunityPartners = CommunityPartners.filter(d => d.community_type.community_type_id === parseInt(comm_type));
}
if (!not_set.includes(legislative_value)) {
    var CommunityPartners = CommunityPartners.filter(d => d.legislative_district === parseInt(legislative_value.split("+")[2]));
}
if (!not_set.includes(comm_type) || !not_set.includes(legislative_value) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
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
var CommunityPartners = CommunityPartners.filter(d => projectCommunities.has(d.community_partner_id));
var CampusPartners = CampusPartners.filter(d => projectCampus.has(d.campus_partner_id));


var y_axis = getUrlVars()["y_axis"];
if (not_set.includes(y_axis)) {
   var y_axis = "campus";
}

var x_vars = [];
var y_vars = [];
var chart_data = [];
var y_label = "";
for (m in missionList) {
   var color = missionList[m].color;
   var communities = CommunityPartners.filter(d => d.primary_mission_id === missionList[m].id);
   var data = [];
   communities.forEach(function(feature) {
      comm_mission_count = new Set();
      comm_mission_count.add(feature["primary_mission_id"]);
      feature["secondary_mission_ids"].forEach(item => comm_mission_count.add(item));

      var projs = Projects.filter(d => d.community_partner_ids.includes(feature["community_partner_id"]));
      var x = projs.length;
      x_vars.push(x);
      var y_items = new Set();
      projs.forEach(function(feature) {
         if (y_axis === "years") {
            y_label = "Years of Engagement";
            feature["years"].forEach(item => y_items.add(item));
         } else if (y_axis === "engagement") {
            y_label = "Number of Engagement Types";
            y_items.add(feature["engagement_type"].engagement_type_id);
         } else if (y_axis === "score") {
            y_label = "Interdisciplinary Score";
            feature["subcategories"].forEach(item => y_items.add(item));
         } else if (y_axis === "campus") {
            y_label = "Number of Campus Partners";
            feature["campus_partner_ids"].forEach(item => y_items.add(item));
         }
      })
      var y = y_items.size;
      if (y_axis === "score") {
         var y = y + comm_mission_count.size;
      }
      y_vars.push(y);
      var comm = {"name": feature["community_partner_name"], "x": x, "y":y};
      data.push(comm);
   })
   var mission_comms = {"name":missionList[m].name, "color":color, "data":data};
   chart_data.push(mission_comms);
}

var xLine = (Math.min(...x_vars)+Math.max(...x_vars))/2;
var yLine = (Math.min(...y_vars)+Math.max(...y_vars))/2;

var chart = Highcharts.chart('container', {
   "chart":{ "type":"scatter","zoomType":"xy"},
   "title":{ "text":""},
   "xAxis":{
      "allowDecimals":false,
      "title":{"text":"Projects",
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px", "fontFamily": "Arial Narrow"}},
      "plotLines":[
         {  "value":xLine,    "dashStyle":"dash",
            "width":2,        "color":"#d33" }]},
   "yAxis":{
      "allowDecimals":false,
      "title":{
         "text":y_label,
         "style":{"fontWeight":"bold","color":"black","fontSize":"15px", "fontFamily": "Arial Narrow"}},
      "plotLines":[
         {  "value":yLine,    "dashStyle":"dash",
            "width":2,        "color":"#d33"}]},
   "legend":{
      "layout":"horizontal",    "align":"right",    "verticalAlign":"top",
      "x":10,   "y":20,         "borderWidth":1, "itemStyle": {"fontFamily": "Arial Narrow"},
      "backgroundColor":"#FFFFFF",  "shadow":"true"
   },
   "plotOptions":{
      "scatter":{
         "marker":{
            "radius":5,
            "symbol": "circle",
            "states":{"hover":{"enabled":true,"lineColor":"rgb(100,100,100)"}}},
         "states":{"hover":{"marker":{"enabled":false}}},
         "jitter": {"x": 0.24, "y": 0.24},
         "tooltip":{
            "style": {"fontFamily": "Arial Narrow"},
            "headerFormat": "",
            "pointFormat":"<b>{point.name}</b><br>Projects: {point.x} <br>Community Partner Engagement: {point.y}"
         }
      }
   },
   "responsive":{"rules":[{"condition":{"maxWidth":500},
            "chartOptions":{"legend":{"layout":"horizontal","align":"center","verticalAlign":"bottom"}}}]},
   "series":chart_data
});

if (!not_set.includes(community_partner)) {
    var selectCom = CommunityPartners.filter(d => d.community_partner_id == community_partner);
    if (selectCom.length) {
        var selected = selectCom[0].community_partner_name;
        for (c in chart_data) {
            if (chart_data[c].data.length) {
                for (d in chart_data[c].data) {
                    if (chart_data[c].data[d].name === selected) {
                        chart.update({
                           "xAxis":{
                              "plotLines":[
                                 {  "value":chart_data[c].data[d].x,    "dashStyle":"dash",
                                    "width":2,        "color":"#d33" }]},
                           "yAxis":{
                              "plotLines":[
                                 {  "value":chart_data[c].data[d].y,    "dashStyle":"dash",
                                    "width":2,        "color":"#d33" }]},
                        });

                    }
                }
            }
        }
    } else {
        alert("The selected community partner does not exist for the filters selected");
    }
}
