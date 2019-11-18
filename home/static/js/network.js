// //*********************************** Get data from HTML Network Chart *****************************************************

var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);

var Collegenames = JSON.parse(document.getElementById('Collegenames').textContent);

// console.log("campus partner chart data ",Collegenames)
// campus_partner_json,community_partner_json,mission_subcategories_json,projects_json
var campus_partner_json = JSON.parse(document.getElementById('campus_partner_json').textContent);
     // console.log("PARTNERS",campus_partner_json);

var community_partner_json = JSON.parse(document.getElementById('community_partner_json').textContent);
var community_partner_json2 = JSON.parse(document.getElementById('community_partner_json').textContent);
var mission_subcategories_json = JSON.parse(document.getElementById('mission_subcategories_json').textContent);
var projects_json = JSON.parse(document.getElementById('projects_json').textContent);

// console.log(" initial load of projects_json",projects_json)
var max_year = JSON.parse(document.getElementById('max_year').textContent);
var max_yr_id = JSON.parse(document.getElementById('max_yr_id').textContent);
// alert(max_yr_id);

const colorCodeObject = {
    [Missionarea[0]]:         "#01B8AA",
    [Missionarea[1]]:         "#374649",
    [Missionarea[2]]:    "#FD625E",
    [Missionarea[3]]:          "#8AD4EB",
    [Missionarea[4]]:        "#FE9666",
    [Missionarea[5]]:       "#A66999",
    [Missionarea[6]]:       "#3599B8",
    [Missionarea[7]]:       "#DFBFBF",
    [Missionarea[8]]:       "#1743f3"
}

// alert(Missionarea0]);

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

var academic_year = getUrlVars()["academic_year"];
var engagement_type = getUrlVars()["engagement_type"];
var mission = getUrlVars()["mission"];
var comm_type = getUrlVars()["community_type"];
var college_name = getUrlVars()["college_name"];
var campus_partner = getUrlVars()["campus_partner"];
var weitz_cec_part = getUrlVars()["weitz_cec_part"];



// var k12_flag = getUrlVars()["k12_flag"];

// console.log(" url values ",college_name)

var not_set = [undefined, "All", ''];
//
// if (k12_flag==="No"){
//     k12_flag="false"
// }
//
// if (k12_flag==="Yes"){
//     k12_flag="true"
// }

if (weitz_cec_part==="Yes"){
    weitz_cec_part="true"
}

if (weitz_cec_part==="No"){
    weitz_cec_part="false"
}

if (not_set.includes(academic_year)) {
    // alert(academic_year)
    academic_year=max_yr_id
    var projects_json = projects_json.filter(d => d.years.includes(max_yr_id));
    // console.log("filtered academic_year", projects_json)
}


if (!not_set.includes(academic_year)) {
    // alert(academic_year)
    var projects_json = projects_json.filter(d => d.years.includes(parseInt(academic_year)));
    // console.log("filtered academic_year"+ projects_json)
}


if (!not_set.includes(engagement_type)) {
    // console.log(" projects"+ engagement_type)
    var projects_json = projects_json.filter(d => d.engagement_type.engagement_type_id==engagement_type);


}
if (not_set.includes(engagement_type) && engagement_type!='All') {
    console.log(" projects"+ engagement_type)
    var projects_json = projects_json.filter(d => d.engagement_type.engagement_type_name=='Knowledge and Resource Sharing');

}


if (!not_set.includes(comm_type)) {
    var community_partner_json = community_partner_json.filter(d => d.community_type.community_type_id == (comm_type));
    // console.log("filtered comm_type", community_partner_json)
}


if (not_set.includes(comm_type) && comm_type!='All') {
    var community_partner_json = community_partner_json.filter(d => d.community_type.community_type_name =='Nonprofit');


}

if (!not_set.includes(college_name)) {
    var Collegenames = Collegenames.filter(d => d.id ==parseInt(college_name));
    // console.log("filtered college_name", Collegenames)
}
if (!not_set.includes(campus_partner)) {
    var campus_partner_json = campus_partner_json.filter(d => d.campus_partner_id == parseInt(campus_partner));
// console.log("filtered campus_partner",campus_partner_json)
}

if (!not_set.includes(mission)) {
    var projects_json = projects_json.filter(d => d.primary_mission_area.mission_id == parseInt(mission));
    // console.log("filtered mission areas", projects_json)
}
// need to add weitzpart status in json
if (!not_set.includes(weitz_cec_part)) {
    if (['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        if (weitz_cec_part == 'CURR_COMM') {
            var community_partner_json = community_partner_json.filter(d => d.cec_partner.cec_years.includes(academic_year));
            // console.log(CECCommunityPartners.length);
        } else if (weitz_cec_part == 'FORMER_COMM') {
            var community_partner_json = community_partner_json.filter(d => !d.cec_partner.cec_years.includes(academic_year)).filter(d => d.cec_partner.isEmptyObject=false);
            // console.log(CECCommunityPartners.length);
        }

    }
    if (['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        if (weitz_cec_part == 'CURR_CAMP') {
            var campus_partner_json = campus_partner_json.filter(d => d.cec_partner.cec_years.includes(academic_year));
        } else if (weitz_cec_part == 'FORMER_CAMP') {
            var campus_partner_json = campus_partner_json.filter(d => !d.cec_partner.cec_years.includes(academic_year)).filter(d => d.cec_partner.cec_years.isEmptyObject=false);
        }
        var campus_partner_json = campus_partner_json;
        var community_partner_json = community_partner_json;
        // console.log("filtered weitz_cec_part"+ community_partner_json)
    }
}
// if (!not_set.includes(k12_flag)) {
//     // alert("k12 falg"+k12_flag)
//     var projects_json = projects_json.filter(d => d.k12_flag == "false");
//     // console.log("filtered k12 flag option", projects_json)
// }
//
// var test = community_partner_json.filter(d => !d.cec_partner.cec_years.includes(7)).filter(d => d.cec_partner.cec_years.isEmptyObject=false);
//
// console.log("naresh trsting ####################################### ",test)
var chart_data = []
var nodedata=[]
 //
 // var camppartnrprojects=projects_json.filter(d => d.campus_partner_ids.includes(29));
 //             var x=camppartnrprojects.length
 //          // console.log("campus naresh",camppartnrprojects,x);

for (coll in Collegenames) {
    // console.log("college",Collegenames[coll].cname);
    var college = Collegenames[coll].cname

    var camppartners = campus_partner_json.filter(d => d.college.college_name.includes(college))
    // console.log("campus partners",camppartners)
    camppartners.forEach(function (feature) {
        var campid = feature["campus_partner_id"]
        if (camppartners !== 0) {
            // var camp = feature["campus_partner_name"]
            // // var cp={"from":Collegenames[coll].cname,"to":feature["campus_partner_name"]}
            // res2 = {'from': college, 'to': camp}
            // chart_data.push(res2)
            // node = {'id': college, 'color': 'red', 'marker': {'symbol': 'triangle'}}
            // node2 = {'id': camp, 'color': 'black', 'marker': {'symbol': 'triangle'}}
            // nodedata.push(node)
            // nodedata.push(node2)
            // console.log("campuspartnerid ",campid)
            // console.log("projects_json",projects_json)
            var camppartnrprojects = projects_json.filter(d => d.campus_partner_ids.includes(parseInt(campid)));
            // var x = Object.keys(camppartnrprojects)

            camppartnrprojects.forEach(function (feature1) {

                // if (camppartnrprojects != 0) {
                    var camp = feature["campus_partner_name"]
                    // var cp={"from":Collegenames[coll].cname,"to":feature["campus_partner_name"]}
                    res2 = {'from': college, 'to': camp}
                    if (!chart_data.find(o => o.from === college && o.to === camp)){
                    chart_data.push(res2)}
                    node = {'id': college, 'color': 'red', 'marker': {'symbol': 'triangle'},'projects':''}
                    node2 = {'id': camp, 'color': 'black', 'marker': {'symbol': 'triangle'},'projects':'Projects:'+camppartnrprojects.length}
                    if (!nodedata.find(o => o.id === college)){
                    nodedata.push(node)}
                    if (!nodedata.find(o => o.id === camp)){
                    nodedata.push(node2)}
                    var commps = new Set()


                    community_partner_json.forEach(function (feature2) {
                        // console.log(" input",feature2.community_partner_id)
                        var comm = feature2.community_partner_name

                        if (feature1.community_partner_ids.includes(feature2.community_partner_id)) {
                             // console.log("community partner ids",feature1.community_partner_ids,"  includes ",feature2.community_partner_id)
                            commps.add(comm)
                        }
                    })

                    commps=Array.from(commps)

                    // console.log("community partners filtered for a campus partner", commps, "camp", camp)
                    if(!commps.length==0){
                    for (c in commps) {
                        // console.log(" community ",commps[c])
                        var community = community_partner_json.find(d => d.community_partner_name == commps[c])
                        mission_id = community.primary_mission_id
                        mission_obj = mission_subcategories_json.find(d => d.mission_area_id == mission_id)
                        mission_name = mission_obj.mission_area_name
                        // alert("mission_obj"+mission_name)

                        res3 = {'from': camp, 'to': community.community_partner_name,'p':commps.length}
                        // console.log("final",res3)
                        if (!chart_data.find(o => o.from === camp && o.to === community.community_partner_name)){
                        chart_data.push(res3)}
                        node3 = {
                            'id': community.community_partner_name,
                            'color': colorCodeObject[mission_name],
                            'marker': {'symbol': 'circle',

                            // 'radius': commps.length
                            },
                            'projects':'Projects:'+commps.length+ '<br></br>'+'Focus Area: <b></b>'+mission_name
                            // tooltip: {useHTML: true,
                            // format:'<b>Name: {%id%} ${this.Node.name}</b><br><b> projects[${this.point.projects}]</b>'}
                        }
                        if (!nodedata.find(o => o.id === community.community_partner_name)){
                        nodedata.push(node3)}
                    }}

            })
        }
    })
}

console.log("campus partner chart data ",chart_data.length)

if(chart_data.length===0){
    alert("Sorry, There are no Projects matching your selection criteria");
}

 var titletext = "<span style='color:red'>▲College and Main Units</span>"+"<span style='color:white'> ---</span>"+
               "<span style='color: black'>▲Campus Partners</span> <br>"
        var i;
        for (i = 0; i < Missionarea.length; i++) {
            var missionname = Missionarea[i]
            var selectedcolor = colorCodeObject[Missionarea[i]]
            titletext +=""+"<span style='color:" + selectedcolor + "'>●" + missionname +"<span style='color:white'> ---</span>"+"</span>"
            ;

        }

    document.getElementById('text').innerHTML = titletext;


// document.getElementById("text").innerHTML = titletext;

Highcharts.chart('container', {

    chart: {
        type: 'networkgraph',
        zoomType: 'xy'
    },
// renderTo: 'container',
    title:{
        text:'.',
        style:{},
        // align:right
    },

        legend: {
        enabled:true,
                    title:{
                        text: "",
                    },

                    box:{
                        visibility: true,
                    },
            // border: 'black',
            stroke: 'black',
            strokeWidth: 10,

        },

    plotOptions: {
        networkgraph: {
            turboThreshold: 0,
            initialPositions: 'bottom',
            cropThreshold:500,
            layoutAlgorithm: {
                enableSimulation: false,
                integration: 'verlet',
                linkLength: 100,
                linkWidth:10
            }
        },
    },
tooltip: {
        nullFormat:'N/A',
        formatter: function (point) {
             tooltext='Name: <b>' + this.point.id +'<br></br>'+ this.point.projects
            return  tooltext

        }
    },
    series: [{
        name:'Network Graph',
        linkLength: 100,
        type:'networkgraph',
        dataLabels: {
            enabled: false,
            // textPath:'<span style="color:{point.color}">{point.name}</span><br> FromYearProjectCount:{point.x}<br>ToYearProjectCount:{point.x2}<br>',
            linkFormat: ''
        },
        data: chart_data,
        nodes:nodedata,
        legendIndex:1,
        opacity:0
        // showInLegend:false,
        // visibility:true,
    },
    ]
})