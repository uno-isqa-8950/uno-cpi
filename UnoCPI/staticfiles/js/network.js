// //*********************************** Get data from HTML Network Chart *****************************************************

var not_set = [undefined, "All", ''];

var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);

var Collegenames = JSON.parse(document.getElementById('Collegenames').textContent);
var campus_partner_json = JSON.parse(document.getElementById('campus_partner_json').textContent);

var community_partner_json = JSON.parse(document.getElementById('community_partner_json').textContent);
var community_partner_json2 = JSON.parse(document.getElementById('community_partner_json').textContent);
var mission_subcategories_json = JSON.parse(document.getElementById('mission_subcategories_json').textContent);
var projects_json = JSON.parse(document.getElementById('projects_json').textContent);

var max_year = JSON.parse(document.getElementById('max_year').textContent);
var max_yr_id = JSON.parse(document.getElementById('max_yr_id').textContent);
var allCamps = JSON.parse(document.getElementById("campusfilter").textContent);


function updateCampus() {

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


function  getchartdata(Missionarea,Collegenames,campus_partner_json,community_partner_json,mission_subcategories_json,projects_json,max_yr_id,max_year,
                       academic_year,engagement_type, mission,comm_type, college_name,campus_partner,weitz_cec_part,legislative,community_partner  ) {

    // if ( academic_year =='All' ) {
    //
    //     var projects_json = projects_json;
    //
    // }
     if ( comm_type == 'All') {
        var community_partner_json = community_partner_json ;
    }

    if (!not_set.includes(engagement_type)) {
        var projects_json = projects_json.filter(d => d.engagement_type.engagement_type_id === parseInt(engagement_type));
    }
    // if (not_set.includes(academic_year) && academic_year!='All' ) {
    if (not_set.includes(academic_year) ) {
        var projects_json = projects_json.filter(d => d.years.includes(max_yr_id));

    }

    if (!not_set.includes(academic_year)) {
        var projects_json = projects_json.filter(d => d.years.includes(parseInt(academic_year)));
    }

    if (!not_set.includes(mission)) {
        var projects_json = projects_json.filter(d => d.primary_mission_area.mission_id === (parseInt(mission)));
    }

    if (weitz_cec_part == 'CURR_CAMP') {
        var campus_partner_json = campus_partner_json.filter(d => d.cec_partner.cec_partner_status === "Current");
    }
    if (weitz_cec_part == 'FORMER_CAMP') {
        var campus_partner_json = campus_partner_json.filter(d => d.cec_partner.cec_partner_status === "Former");
    }
    if (!not_set.includes(college_name)) {
        var campus_partner_json = campus_partner_json.filter(d => d.college.college_name_id === parseInt(college_name));
    }
    if (!not_set.includes(campus_partner)) {
        var campus_partner_json = campus_partner_json.filter(d => d.campus_partner_id === parseInt(campus_partner));
    }
    if (!not_set.includes(college_name) || !not_set.includes(campus_partner) || ['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        camps = [];
        campus_partner_json.forEach(function (feature) {
            camps.push(feature["campus_partner_id"]);
        })
        var projects_json = projects_json.filter(d => d.campus_partner_ids.some(r => camps.includes(r)));
    }

    if (!not_set.includes(comm_type)) {
        var community_partner_json = community_partner_json.filter(d => d.community_type.community_type_id === parseInt(comm_type));
    }
      if (not_set.includes(comm_type) && comm_type != 'All') {
        var community_partner_json = community_partner_json.filter(d => d.community_type.community_type_name == 'Nonprofit');
    }
    if (!not_set.includes(legislative)) {
        var community_partner_json = community_partner_json.filter(d => d.legislative_district === parseInt(legislative.split(" ")[2]));
    }
    if (weitz_cec_part == 'CURR_COMM') {
        var community_partner_json = community_partner_json.filter(d => d.cec_partner.cec_partner_status === "Current");
    }
    if (weitz_cec_part == 'FORMER_COMM') {
        var community_partner_json = community_partner_json.filter(d => d.cec_partner.cec_partner_status === "Former");
    }
    if (!not_set.includes(comm_type) || !not_set.includes(legislative) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        comms = [];
        community_partner_json.forEach(function (feature) {
            comms.push(feature["community_partner_id"]);
        })
        var projects_json = projects_json.filter(d => d.community_partner_ids.some(r => comms.includes(r)));
    }

    if (!not_set.includes(community_partner)) {

        var projects_json = projects_json.filter(d => d.community_partner_ids.includes(parseInt(community_partner)));
        var community_partner_json = community_partner_json.filter(d => d.community_partner_id== parseInt(community_partner));

    }


    var projectCommunities = new Set();
    var projectCampus = new Set();
    projects_json.forEach(function(feature) {
        if (feature["community_partner_ids"].length != 0) {
            feature["community_partner_ids"].forEach(item => projectCommunities.add(item));
        }
        feature["campus_partner_ids"].forEach(item => projectCampus.add(item));
    })

    if (!not_set.includes(engagement_type) || !not_set.includes(academic_year) || !not_set.includes(college_name) || !not_set.includes(campus_partner) || !not_set.includes(legislative) || ['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        var community_partner_json = community_partner_json.filter(d => projectCommunities.has(d.community_partner_id));
    }
    if (!not_set.includes(engagement_type) || !not_set.includes(academic_year) || !not_set.includes(comm_type)  || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        var campus_partner_json = campus_partner_json.filter(d => projectCampus.has(d.campus_partner_id));
    }


    var chart_data = []
    var nodedata = []

    for (coll in Collegenames) {

        var college = Collegenames[coll].cname

        var camppartners = campus_partner_json.filter(d => d.college.college_name.includes(college))

        camppartners.forEach(function (feature) {
            var campid = feature["campus_partner_id"]
            if (camppartners !== 0) {
                var camppartnrprojects = projects_json.filter(d => d.campus_partner_ids.includes(parseInt(campid)));


                var commpartnerslist=[]
                var filteredcommlist=[]


                for (var i = 0; i < community_partner_json.length; i++) {
                    if (!filteredcommlist.includes(community_partner_json[i].community_partner_id) ) {
                        filteredcommlist.push(community_partner_json[i].community_partner_id);
                    }
                }


                            camppartnrprojects.forEach(function(feature){
                                   var cc=feature.community_partner_ids

                                   if (cc.length>0){
                                       for (x in cc){
                                           // //console.log(" id of cc",cc[x], " list ",filteredcommlist[x])
                                           if (!commpartnerslist.includes(cc[x])){
                                               commpartnerslist.push(cc[x])
                                                                                 }
                                       }
                                   }
                               })

                var cop=[]
                            for (c in commpartnerslist){
                                if(filteredcommlist.includes(commpartnerslist[c])){
                                    cop.push(commpartnerslist[c])
                                }
                            }

                camppartnrprojects.forEach(function (feature1) {

                                       var commps = new Set()


                    community_partner_json.forEach(function (feature2) {

                        var comm = feature2.community_partner_name

                        if (feature1.community_partner_ids.includes(feature2.community_partner_id)) {
                            commps.add(comm)
                        }
                    })

                    commps = Array.from(commps)
                        if(!commps.length == 0 ){
                            var camp = feature["campus_partner_name"]


                    res2 = {'from': college, 'to': camp}
                    if (!chart_data.find(o => o.from === college && o.to === camp)) {
                        chart_data.push(res2)
                    }
                    node = {'id': college, 'color': 'red', 'marker': {'symbol': 'triangle'}, 'projects': ''}
                    node2 = {
                        'id': camp,
                        'color': 'black',
                        'marker': {'symbol': 'triangle'},
                        'projects': 'Projects: ' + '<b>'+camppartnrprojects.length+'</b>' +'<br></br>'+'Community Partner Engagement: '+'<b>' + cop.length+'</b>'
                    }
                    if (!nodedata.find(o => o.id === college)) {
                        nodedata.push(node)
                    }
                    if (!nodedata.find(o => o.id === camp)) {
                        nodedata.push(node2)
                    }

                        }

                    if (!commps.length == 0) {
                        for (c in commps) {
                            var community = community_partner_json.find(d => d.community_partner_name == commps[c])
                            mission_id = community.primary_mission_id
                            mission_obj = mission_subcategories_json.find(d => d.mission_area_id == mission_id)
                            mission_name = mission_obj.mission_area_name
                            commpprojects=projects_json.filter(d => d.community_partner_ids.includes(community.community_partner_id))
                            var campspartnerslist=[]
                            commpprojects.forEach(function(feature){
                                   var cc=feature.campus_partner_ids
                                   if (cc.length>0){
                                       for (x in cc){
                                           if (!campspartnerslist.includes(cc[x])){
                                               campspartnerslist.push(cc[x])

                                           }
                                       }
                                   }
                               })
                            var campsfinal=[]
                            campus_partner_json.forEach(function (feature4) {
                                var cp=feature4.campus_partner_id
                                if(!campsfinal.includes(cp)){
                                    campsfinal.push(cp)
                                }

                            })
                            var cp=[]

                            for (c in campspartnerslist){
                                if(campsfinal.includes(campspartnerslist[c])){
                                    cp.push(campspartnerslist[c])
                                }
                            }

                            res3 = {'from': camp, 'to': community.community_partner_name, 'p': commps.length}
                            if (!chart_data.find(o => o.from === camp && o.to === community.community_partner_name)) {
                                chart_data.push(res3)
                            }
                            node3 = {
                                'id': community.community_partner_name,
                                'color': Missionarea.find(d => d.name == mission_name).color,

                                'marker': {
                                    'symbol': 'circle',

                                },
                                'projects': 'Projects: '+'<b>' + commpprojects.length +'</b>'+ '<br></br>' + 'Focus Area : '+ mission_name + '<br></br>'+'Campus Partner Engagement: '+'<b>'+ cp.length+'</b>'
                            }
                            if (!nodedata.find(o => o.id === community.community_partner_name)) {
                                nodedata.push(node3)
                            }
                        }
                    }

                })
            }
        })
    }


    if (chart_data.length === 0) {
        alert("There are no projects associated with your selection criteria.");
    }

      return[chart_data,nodedata]
}

    var titletext = "<span style='color:red;font-size:20px;margin-left:6px'>▲</span><span style='margin-right: 12px'>College and Main Units</span><span style='color: black;font-size:20px'>▲ </span><span style='margin-right: 12px'>Campus Partners</span> "
    var i;
    for (i = 0; i < Missionarea.length; i++) {
        var missionname = Missionarea[i].name
        var selectedcolor = Missionarea[i].color
        titletext += "<span style='color:" + selectedcolor + ";font-size:20px'>●" + "</span>" + "<span style='margin-right: 12px'>" + missionname + "</span>"
        ;

    }

    document.getElementById('text').innerHTML = titletext;



var res=getchartdata(Missionarea,Collegenames,campus_partner_json,community_partner_json,mission_subcategories_json,projects_json,max_yr_id,max_year)
var chart_data=res[0]
var nodedata=res[1]


var chart=Highcharts.chart('container', {

    chart: {
        type: 'networkgraph',
        zoomType: 'xy'
    },
     boost: {
                    enabled: true,
                    seriesThreshold: 1,
                    useGPUTranslations: true,
                    usePreallocated: true,
                },
    title: {
        text: "",
        style: {},

    },

    legend: {
        enabled: true,
        title: {
            text: "",
            style: {fontWeight: "bold", color: "black", fontSize: 15, fontFamily: "Arial Narrow"},
        },

        box: {
            visibility: true,
        },

        stroke: 'black',
        strokeWidth: 10,

    },

    plotOptions: {

        networkgraph: {
            allowPointSelect: true,
            cursor: 'pointer',
            turboThreshold: 0,
            initialPositions: 'bottom',
            cropThreshold: 500,
            layoutAlgorithm: {
                enableSimulation: false,
                integration: 'verlet',
                linkLength: 100,
                linkWidth: 1
            },
             marker:{
            		states:{
           						 hover:{
            								radius:7,
              								},

           						 }
            },

            states: {
                inactive: {
                    linkColor:'black',
                    linkWidth:10,
                    linkOpacity:0
                					},
                hover:{
                 linkColor:'black',
                 linkWidth:100,
                }
            }

        },

    },



tooltip: {
        nullFormat:'N/A',
        style: {fontFamily: "Arial Narrow"},
        formatter: function (point) {
             tooltext= '<b>'+this.point.id +'</b>'+'<br></br>'+ this.point.projects
            return  tooltext

        }
    },
    series: [{
        name:'Network Graph',
        linkLength: 100,
        type:'networkgraph',
        dataLabels: {
            enabled: false,
            linkFormat: ''
        },
        data: chart_data,
        nodes:nodedata,
        legendIndex:1,
        opacity:0
            },
    ]
})




function updatechart(){
       var x = document.getElementById("loading");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
setTimeout(function(){
    var academic_year =  $('#id_academicyear option:selected').val();
    var engagement_type = $('#id_engagement_type option:selected').val();
    var mission =  $('#id_mission option:selected').val();
    var comm_type = $('#id_community_type option:selected').val();
    var college_name = $('#id_college_name option:selected').val();
    var campus_partner =  $('#id_campus_partner option:selected').val();
    var weitz_cec_part =  $('#id_weitz_cec_part option:selected').val();
    var community_partner=$('#id_community_partner option:selected').val();
    var legislative=$('#id_legislative_value option:selected').val();
    var not_set = [undefined, "All", ''];

    var res=getchartdata(Missionarea,Collegenames,campus_partner_json,community_partner_json,mission_subcategories_json,projects_json,max_yr_id,max_year,
        academic_year,engagement_type,mission,comm_type, college_name, campus_partner,weitz_cec_part,legislative,community_partner)
    var chartdata_updated=res[0]
    var nodedata_updated=res[1]
    console.log(" i got the chart updated data")
    chart.update({
        series: [{

            data: chartdata_updated,
            nodes:nodedata_updated,

        }
        ]
})
console.log("i updated the chart")
$('#loading').hide();
}, 0.0001)
}
