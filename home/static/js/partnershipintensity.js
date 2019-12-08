var not_set = [undefined, "All", ''];
var missionList = JSON.parse(document.getElementById('missionList').textContent);
var CommunityPartners = JSON.parse(document.getElementById('CommunityPartners').textContent);
var Projects = JSON.parse(document.getElementById('Projects').textContent);
var CampusPartners = JSON.parse(document.getElementById('CampusPartners').textContent);

function getChartData (Projects, CommunityPartners, CampusPartners, missionList, engagement_type, academic_year, comm_type, college_name, campus_partner, weitz_cec_part, legislative_value, y_axis) {
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

    if (!not_set.includes(legislative_value)) {
        var CommunityPartners = CommunityPartners.filter(d => d.legislative_district === parseInt(legislative_value.split(" ")[2]));
    }
    if (weitz_cec_part == 'CURR_COMM') {
        var CommunityPartners = CommunityPartners.filter(d => d.cec_partner.cec_partner_status === "Current");
    }
    if (weitz_cec_part == 'FORMER_COMM') {
        var CommunityPartners = CommunityPartners.filter(d => d.cec_partner.cec_partner_status === "Former");
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

    if (!not_set.includes(engagement_type) || !not_set.includes(academic_year) || !not_set.includes(college_name) || !not_set.includes(campus_partner) || ['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        var CommunityPartners = CommunityPartners.filter(d => projectCommunities.has(d.community_partner_id));
    }
    if (!not_set.includes(engagement_type) || !not_set.includes(academic_year) || !not_set.includes(comm_type) || !not_set.includes(legislative_value) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        var CampusPartners = CampusPartners.filter(d => projectCampus.has(d.campus_partner_id));
    }
    var campers = [];
    CampusPartners.forEach(function(feature) {
        campers.push(feature["campus_partner_id"]);
    });
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
                var thisCamp = [];
                feature["campus_partner_ids"].forEach(item => thisCamp.push(item));
                let intersection = thisCamp.filter(x => campers.includes(x));
                intersection.forEach(item => y_items.add(item));
             }
          });
          var y = y_items.size;
          if (y_axis === "score") {
             var y = y + comm_mission_count.size;
          }
          y_vars.push(y);
          var comm = {"name": feature["community_partner_name"], "x": x, "y":y};
          data.push(comm);
       });
       var mission_comms = {"name":missionList[m].name, "color":color, "data":data};
       chart_data.push(mission_comms);
    }
    var xLine = (Math.min(...x_vars)+Math.max(...x_vars))/2;
    var yLine = (Math.min(...y_vars)+Math.max(...y_vars))/2;
    // const median = arr => {
    //   const mid = Math.floor(arr.length / 2),
    //     nums = [...arr].sort((a, b) => a - b);
    //   return arr.length % 2 !== 0 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
    // };
    // var xLine = median(x_vars);
    // var yLine = median(y_vars);

    var select = document.getElementById("id_community_partner");
    select.options.length = 2;
    for (c in CommunityPartners) {
        select.options[select.options.length] = new Option(CommunityPartners[c].community_partner_name, CommunityPartners[c].community_partner_id);
    }

    return [xLine, yLine, y_label, chart_data, CommunityPartners];
}

var defaultYrID = JSON.parse(document.getElementById('defaultYrID').textContent);

var res = getChartData (Projects, CommunityPartners, CampusPartners, missionList, '', defaultYrID, '', '', '', '', '', '');
var xLine = res[0];
var yLine = res[1];
var y_label = res[2];
var chart_data = res[3];

var clickdouble = {clickedOnce : false, timer : null, timeBetweenClicks : 400};

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
      "backgroundColor":"#FFFFFF",  "shadow":"true"},
   "plotOptions":{
      "scatter":{
         "marker":{
            "radius":5,
            "symbol": "circle",
            "states":{"hover":{"enabled":true,"lineColor":"rgb(100,100,100)"}}},
         "states":{"hover":{"marker":{"enabled":false}}},
         // "jitter": {"x": 0.24, "y": 0.24},
         "point": {"events": {
            "click": function () {
                chart.update({
                   "xAxis":{
                      "plotLines":[
                         { "value":xLine, "dashStyle":"dash", "width":2, "color":"#d33" },
                         { "value":this.x, "width":2, "color":"#d33" }]},
                   "yAxis":{
                      "plotLines":[
                         { "value":yLine, "dashStyle":"dash", "width":2, "color":"#d33" },
                         { "value":this.y, "width":2, "color":"#d33" }]},
                });
                if (clickdouble == ('Category: ' + this.category + ', value: ' + this.y)) {
                    this.remove();
                    clickdouble = '';
                }else{
                    clickdouble = 'Category: ' + this.category + ', value: ' + this.y;
                }}}},
         "tooltip":{
            "style": {"fontFamily": "Arial Narrow", "pointerEvents": "auto"},
            "headerFormat": "",
            "pointFormat":"<b>{point.name}</b><br>Projects: <b>{point.x}</b> <br>"+y_label+": <b>{point.y}</b><br><i>Double click on point to exclude it from the dataset</i>"}
      }},
   "responsive":{"rules":[{"condition":{"maxWidth":500},
            "chartOptions":{"legend":{"layout":"horizontal","align":"center","verticalAlign":"bottom"}}}]},
   "series":chart_data
});

function updateChart () {
    var y_axis = $('#id_y_axis option:selected').val();
    var academic_year = $('#id_academic_year option:selected').val();
    var engagement_type = $('#id_engagement_type option:selected').val();
    var college_name = $('#id_college_name option:selected').val();
    var campus_partner = $('#id_campus_partner option:selected').val();
    var weitz_cec_part = $('#id_weitz_cec_part option:selected').val();
    var legislative_value = $('#id_legislative_value option:selected').val();
    var comm_type = $('#id_community_type option:selected').val();
    if (academic_year == '') {
        var academic_year = defaultYrID;
    }
    var res = getChartData (Projects, CommunityPartners, CampusPartners, missionList, engagement_type, academic_year, comm_type, college_name, campus_partner, weitz_cec_part, legislative_value, y_axis);
    xLine = res[0];
    yLine = res[1];
    y_label = res[2];
    chart_data = res[3];
    comms = res[4];

    chart.update({
       "xAxis":{
          "plotLines":[
             { "value":xLine, "dashStyle":"dash", "width":2, "color":"#d33" }]},
       "yAxis":{
          "title":{"text":y_label},
          "plotLines":[
             { "value":yLine, "dashStyle":"dash", "width":2, "color":"#d33" }]},
       "plotOptions":{
          "scatter":{
             "tooltip":{"pointFormat":"<b>{point.name}</b><br>Projects: <b>{point.x}</b> <br>"+y_label+": <b>{point.y}</b><br><i>Double click on point to exclude it from the dataset</i>"}}},
       "series":chart_data
    });
}

function getCommunityCroasshairs () {
    var selectedComm = $('#id_community_partner option:selected').val();
    if (!not_set.includes(selectedComm)) {
        var selectCom = CommunityPartners.filter(d => d.community_partner_id == selectedComm);
        var selected = selectCom[0].community_partner_name;
        for (c in chart_data) {
            if (chart_data[c].data.length) {
                for (d in chart_data[c].data) {
                    if (chart_data[c].data[d].name === selected) {
                        chart.update({
                            "xAxis": {
                                "plotLines": [
                                    {"value": xLine, "dashStyle": "dash", "width": 2, "color": "#d33"},
                                    {"value": chart_data[c].data[d].x, "width": 2, "color": "#d33"}]
                            },
                            "yAxis": {
                                "plotLines": [
                                    {"value": yLine, "dashStyle": "dash", "width": 2, "color": "#d33"},
                                    {"value": chart_data[c].data[d].y, "width": 2, "color": "#d33"}]
                            },
                        });
                    }
                }
            }
        }
    } else {
        chart.update({
           "xAxis":{
              "plotLines":[
                 { "value":xLine, "dashStyle":"dash", "width":2, "color":"#d33" }]},
           "yAxis":{
              "plotLines":[
                 { "value":yLine, "dashStyle":"dash", "width":2, "color":"#d33" }]},
        });
    }
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
    select.options.length = 2;
    for(campus in campus_filter) {
        select.options[select.options.length] = new Option(campus_filter[campus].name, campus_filter[campus].id);
    }
}

function jitterFunc(checkboxElem) {
  if (checkboxElem.checked) {
    chart.update({ "plotOptions":{ "scatter":{"jitter": {"x": 0.24, "y": 0.24}} }});
  } else {
    chart.update({ "plotOptions":{ "scatter":{"jitter": {"x": 0, "y": 0}} }});
  }
}
