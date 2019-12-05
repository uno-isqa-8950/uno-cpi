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
var min_year = JSON.parse(document.getElementById('min_year').textContent);
var min_yr_id = JSON.parse(document.getElementById('min_yr_id').textContent);

function  getchartdata(Missionarea,Collegenames,campus_partner_json,community_partner_json,mission_subcategories_json,projects_json,max_yr_id,max_year,min_yr_id,min_year,
                       academic_year,endacademic_year,engagement_type, college_name, campus_partner,weitz_cec_part,comm_type,legislative) {

    console.log(academic_year," ---",endacademic_year)


        if (not_set.includes(academic_year)) {
        // alert(academic_year)
            console.log(academic_year," ----------->",min_yr_id)
        var startprojects = projects_json.filter(d => d.years.includes(parseInt(min_yr_id)));
        console.log("filtered academic_year default ",startprojects)
       }


        if (!not_set.includes(academic_year)) {
        // alert(academic_year)
        var startprojects = projects_json.filter(d => d.years.includes(parseInt(academic_year)));
        console.log("filtered academic_year selected year ",startprojects)
       }


    // console.log(" end aca year ",endacademic_year)
    if (not_set.includes(endacademic_year)) {
        console.log(endacademic_year," ----------->",max_yr_id)
        var endprojects = projects_json.filter(d => d.years.includes(parseInt(max_yr_id)));
        console.log("filtered end academic_year default", endprojects)
    }


    console.log(" end aca year ",endacademic_year)
    if (!not_set.includes(endacademic_year)) {
        // alert(academic_year)
        var endprojects = projects_json.filter(d => d.years.includes(parseInt(endacademic_year)));
        console.log("filtered end academic_year for selected ", endprojects)
    }


    if (!not_set.includes(engagement_type)) {
        // console.log(" projects"+ engagement_type)
        var startprojects = startprojects.filter(d => d.engagement_type.engagement_type_id == engagement_type);
         var endprojects = endprojects.filter(d => d.engagement_type.engagement_type_id == engagement_type);
    }

    if (!not_set.includes(legislative)) {
        var startprojects = startprojects.filter(d => d.legislative_district == parseInt(legislative));
        var endprojects = endprojects.filter(d => d.legislative_district == parseInt(legislative));
        // console.log("filtered mission areas", projects_json)
    }

        if (weitz_cec_part == 'CURR_CAMP') {
            var campus_partner_json = campus_partner_json.filter(d => d.cec_partner.cec_partner_status === "Current");
        }
        if (weitz_cec_part == 'FORMER_CAMP') {
            var campus_partner_json = campus_partner_json.filter(d => d.cec_partner.cec_partner_status === "Former");
        }

        if (!not_set.includes(college_name)) {
        var campus_partner_json = campus_partner_json.filter(d => d.college.college_name_id=== parseInt(college_name));
        // console.log("filtered college_name", Collegenames)
    }
    if (!not_set.includes(campus_partner)) {
        var campus_partner_json = campus_partner_json.filter(d => d.campus_partner_id == parseInt(campus_partner));
// console.log("filtered campus_partner",campus_partner_json)
    }
     if (!not_set.includes(college_name) || !not_set.includes(campus_partner) || ['CURR_CAMP', 'FORMER_CAMP'].includes(weitz_cec_part)) {
        camps = [];
        campus_partner_json.forEach(function (feature) {
            camps.push(feature["campus_partner_id"]);
        })
        var startprojects = startprojects.filter(d => d.campus_partner_ids.some(r => camps.includes(r)));
        var endprojects = endprojects.filter(d => d.campus_partner_ids.some(r => camps.includes(r)));
    }

        if (weitz_cec_part == 'CURR_COMM') {
            var community_partner_json = community_partner_json.filter(d => d.cec_partner.cec_partner_status === "Current");
        }
        if (weitz_cec_part == 'FORMER_COMM') {
            var community_partner_json = community_partner_json.filter(d => d.cec_partner.cec_partner_status === "Former");
        }

    if (!not_set.includes(comm_type)) {
        var community_partner_json = community_partner_json.filter(d => d.community_type.community_type_id == (comm_type));
        // console.log("filtered comm_type", community_partner_json)
    }
    if (!not_set.includes(comm_type) || ['CURR_COMM', 'FORMER_COMM'].includes(weitz_cec_part)) {
        comms = [];
        community_partner_json.forEach(function (feature) {
            comms.push(feature["community_partner_id"]);
        })
        var startprojects = startprojects.filter(d => d.community_partner_ids.some(r => comms.includes(r)));
         var endprojects = endprojects.filter(d => d.community_partner_ids.some(r => comms.includes(r)));
    }





    // console.log("projects_json_count chart data ", projects_json_count)

    if (startprojects.length == 0 && endprojects.length == 0) {
        alert("Sorry, there are no projects matching your filter criteria");
    }


console.log("startprojects after filtwrs ",startprojects)
console.log("endprojects after filters",endprojects)

var secondary_y_axis=[]
var Yaxis=[]
var json_data=[]
var from_json_data=[]
var to_json_data=[]
var missionarealist=[]
var subdrill=[]
    for (m in Missionarea) {
        var mission_id = Missionarea[m].id;
        var missionLabel = '';
        var missionLabel = missionLabel.concat('<span tabindex="-1" data-toggle="tooltip" data-placement="right" title="',Missionarea[m].mission_descr,'" class="float" > <i class="fa fa-info-circle fa-align-top" aria-hidden="true"></i></span> ',Missionarea[m].name);
        missionarealist.push(missionLabel);
        // console.log(" mission id and name",mission_id)
        var startyearprojects = startprojects.filter(d => d.primary_mission_area.mission_id === parseInt(mission_id));
        var from_project_count = startyearprojects.length
        var endyearprojects = endprojects.filter(d => d.primary_mission_area.mission_id === parseInt(mission_id));
        var to_project_count = endyearprojects.length
        var mid = Missionarea.indexOf(Missionarea[m])
        // console.log(" from_project_count,to_project_count ", from_project_count,to_project_count )
        if (from_project_count < to_project_count) {
            if(from_project_count ==0){
                var per = Math.round(( to_project_count/to_project_count) * 100)
            }else{
            var per = Math.round(((to_project_count-from_project_count ) / from_project_count) * 100)}
            // console.log("red")
            res = {
                "name": Missionarea[m].name,
                "x": from_project_count,
                "x2": to_project_count,
                "y": mid,
                "drilldown": Missionarea[m].name,
                "color": "turquoise",
                "per": per
            }
        }
        else {
            // console.log("non red")
            if(to_project_count == 0){
                var per = Math.round(-(from_project_count/from_project_count ) * 100)
            } else{
            var per = Math.round(((to_project_count-from_project_count) / from_project_count) * 100)}
            // console.log(" per ",per)
            res = {
                "name": Missionarea[m].name,
                "x": from_project_count,
                "x2": to_project_count,
                "y": mid,
                "drilldown": Missionarea[m].name,
                "color": "red",
                "per": per
            }
        }

        resfrom = {"name": Missionarea[m].name,"x": from_project_count, "y": mid, "drilldown": Missionarea[m].name}
        resto = {"name": Missionarea[m].name,"x": to_project_count, "y": mid, "drilldown": Missionarea[m].name}

        json_data.push(res)
        from_json_data.push(resfrom)
        to_json_data.push(resto)
        subcategory = []
        var mission_sub = mission_subcategories_json.find(d => d.mission_area_name == Missionarea[m].name).subcategories
        if (mission_sub.length != 0) {
            mission_sub.forEach(function (feature) {
                var res = {'id': feature.subcategory_id, 'name': feature.subcategory_name}
                subcategory.push(res)
                subcategory = subcategory.sort((a, b) => (a.name < b.name ? 1 : -1))
                // console.log("sorted subcategory",subcategory)
            })
        }
        // console.log("Missionarea[m].name ",Missionarea[m].name,"-------------",subcategory)
        subcategorylist = []
        drilldata = []
        if ($('#user').val() === 'True') {
            for (sc in subcategory) {
                var subcatid = subcategory[sc].id
                subcategorylist.push(subcategory[sc].name)
                sid = subcategory.indexOf(subcategory[sc])
                var from_project_mission_sub_ids = startyearprojects.filter(d => d.subcategories.includes(parseInt(subcatid)));
                var from_subcat_counts = from_project_mission_sub_ids.length
                var to_project_mission_sub_ids = endyearprojects.filter(d => d.subcategories.includes(parseInt(subcatid)));
                var to_subcat_counts = to_project_mission_sub_ids.length
                // var mid = Missionarea.indexOf(m)
                if (from_subcat_counts < to_subcat_counts) {
                    if(from_subcat_counts==0){
                        var per = Math.round((( to_subcat_counts/to_subcat_counts) ) * 100)
                    } else{
                    var per = Math.round(((to_subcat_counts-from_subcat_counts) / from_subcat_counts) * 100)}
                    var drill = {
                        "name": subcategory[sc].name, "x": from_subcat_counts,
                        "x2": to_subcat_counts, "y": sid, "color": "turquoise", "per": per
                    }
                }

                else {
                    if(to_subcat_counts==0){
                        var per = Math.round(((- from_subcat_counts/from_subcat_counts) ) * 100)
                    }
                    else{
                    var per = Math.round(((to_subcat_counts-from_subcat_counts ) / from_subcat_counts) * 100)}
                    var drill = {
                        "name": subcategory[sc].name, "x": from_subcat_counts,
                        "x2": to_subcat_counts, "y": sid, "color": "red", "per": per
                    }
                }

                drilldata.push(drill)
            }

            // console.log("drilldata",drilldata)
            drilled = {
                "type": "xrange",
                "name": Missionarea[m].name,
                "id": Missionarea[m].name,
                "yAxis": mid + 1,
                "data": drilldata
            }
            subdrill.push(drilled)
            // console.log("drilldata",drilldata)
            // console.log("subdrill",subdrill)

            // console.log("Missionarea.length",Missionarea.length)
            if (mid == (Missionarea.length - 1)) {
                // console.log(" last one")
                yaxis = {
                    'id': mid + 1,
                    'type': 'category',
                    // # 'min':1,
                    // # 'max':len(subcategorylist)-1,
                    // # 'tickInterval':1.0,
                    'title': {
                        'text': 'Focus Area',
                        'style': {
                            'fontFamily': 'Arial Narrow',
                            'fontWeight': 'bold',
                            'color': 'black',
                            'fontSize': '15px'
                        }
                    },
                    'labels': {'style': {'color': 'black', 'fontSize': '13px'}},
                    'categories': subcategorylist
                }
            }
            else {
                yaxis = {
                    'id': mid + 1,
                    'type': 'category',
                    // # 'min':1,
                    // # 'max':len(subcategorylist)-1,
                    // # 'tickInterval':1.0,
                    'title': {
                        'text': '',
                        'style': {
                            'fontFamily': 'Arial Narrow',
                            'fontWeight': 'bold',
                            'color': 'black',
                            'fontSize': '15px'
                        }
                    },
                    'labels': {'style': {'color': 'black', 'fontSize': '13px'}},
                    'categories': subcategorylist
                }
            }
            // console.log(" ya xis ",yaxis)

            secondary_y_axis.push(yaxis)


        }
        // console.log("secondary_y_axis",secondary_y_axis)
    }

  var   primary_axis={
                'id':0,
                'type': 'category',
                'title': {'text': '',
                          'style': {'fontWeight': 'bold', 'color': 'black', 'fontSize': '15px', "fontFamily": "Arial Narrow"}},
                'labels': {"useHTML": true, 'style': {'color': 'black', 'fontSize': '13px'}},
                'categories': missionarealist,
            }
    Yaxis.push(primary_axis)

    for (axis in secondary_y_axis) {
        // if (!Yaxis.includes(axis)){
        Yaxis.push(secondary_y_axis[axis])}
    // }
    // # print(" yxis value in category ",Yaxis)
  var   Academic_Year = {
        'name': 'Analysis Start Year',
        'data': from_json_data,
        'color': 'teal',
        'type': 'scatter'}
   var  End_Academic_Year = {
        'name': 'Analysis Comparison (End) Year',
        'data': to_json_data,
        'color': 'blue',
        'type': 'scatter'}
  var   project_over_academic_years = {
      'name': 'Analysis Start - End Years',
      'data': json_data,
      'type': 'xrange',
      'showInLegend': false,
      'marker': {
          'enabled': true
      }
  }
  var   Growth = {
          'name': 'Increase In Projects ',
         'data': '',
        'type':'line',
        'showInLegend':true,
        'color':'turquoise',
        'marker':{
        'color':'turquoise',
        'enabled':false
                }

                }
  var   Decrease = {
        'name': 'Decrease In Projects ',
        'data': '',
        'type':'line',
        'showInLegend':true,
        'color': 'red',
        'marker':{
            'color': 'red',
            'enabled':false
        }

                }
                return[project_over_academic_years, Academic_Year, End_Academic_Year,subdrill,Yaxis,Growth,Decrease]

}


var res=getchartdata(Missionarea,Collegenames,campus_partner_json,community_partner_json,mission_subcategories_json,projects_json,max_yr_id,max_year,min_yr_id,min_year)

var project_over_academic_years=res[0]
var Academic_Year =res[1]
var  End_Academic_Year=res[2]
var subdrill=res[3]
var Yaxis=res[4]
var Growth=res[5]
var Decrease=res[6]

// console.log(project_over_academic_years)
// console.log("Academic_Year ",Academic_Year)
// console.log("End_Academic_Year",End_Academic_Year)
// console.log(" subdrill ",subdrill)
// console.log(" y axs " ,Yaxis)

                Highcharts.Tick.prototype.drillable = function () {};

    var chart=Highcharts.chart('container',  {

       'title': '',
        'xAxis': {'allowDecimals': false, 'title': {'text': 'Projects ',
                                                    'style': {'fontFamily':'Arial Narrow','fontWeight': 'bold', 'color': 'black',
                                                              'fontSize': '15px'}}},
        'yAxis':Yaxis,
        'plotOptions': {
            'xrange': {
                'pointWidth': 4,
                'dataLabels': {
                    'enabled': true,
                    'inside':false,
                    'style': {
                        'fontSize': '6px'
                    },
                    'marker':{
                    'linewidth':'4px',
                    }

                },'colorByPoint': false,
                'tooltip': {
                    'style': {'fontFamily': 'Arial Narrow'},
                    // 'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                    "headerFormat": "",
                    'pointFormat': '<span>{point.name}</span><br> Analysis Start Year Projects: <b>{point.x}</b><br>Analysis End Year Projects: <b>{point.x2}</b><br> Growth/Decrease: <b>{point.per}%</b>'
                }
            },

            'scatter': {
                'marker': {
                    'radius': 6,
                    'symbol': 'circle'
                }
            }
        },
        'tooltip': {
            'style': {'fontFamily': 'Arial Narrow'},
        // 'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
            "headerFormat": "",
        'pointFormat': '<span>{point.name}</span><br> Projects: <b>{point.x}</b><span></span>'
                 },
        'legend': {
            'layout': 'horizontal',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -10,
            'y': 10,
            'borderWidth': 1,
            'backgroundColor': '#FFFFFF',
            'shadow': 'true',
            'itemStyle': {'fontFamily': 'Arial Narrow'},
            'backgroundColor': '#FFFFFF', "shadow": 'true'
        },


        'series': [project_over_academic_years, Academic_Year, End_Academic_Year,Growth,Decrease],
        'drilldown':{
            'series': subdrill,
        }

    })




function updatechart(){

    var academic_year =  $('#id_academicyear option:selected').val();
    var endacademic_year =  $('#id_endacademicyear option:selected').val();
    var engagement_type = $('#id_engagement_type option:selected').val();
    var college_name = $('#id_college_name option:selected').val();
    var campus_partner =  $('#id_campus_partner option:selected').val();
    var weitz_cec_part =  $('#id_weitz_cec_part option:selected').val();
    var comm_type = $('#id_community_type option:selected').val();
    var legislative=$('#id_legislative_value option:selected').val();
    var not_set = [undefined, "All", ''];

    var res=getchartdata(Missionarea,Collegenames,campus_partner_json,community_partner_json,mission_subcategories_json,projects_json,max_yr_id,max_year,min_yr_id,min_year,
        academic_year,endacademic_year,engagement_type, college_name, campus_partner,weitz_cec_part,comm_type,legislative);
    var project_over_academic_years=res[0]
    var Academic_Year=res[1]
    var End_Academic_Year=res[2]
    var subdrill=res[3]
    var Yaxis=res[4]


        chart.update({
        'yAxis':Yaxis,
       'series': [project_over_academic_years, Academic_Year, End_Academic_Year],
        'drilldown':{
            'series': subdrill,
        }

});


}


function updateCampus() {
    var allCamps = JSON.parse(document.getElementById('campus_filter').textContent);
    console.log(" all camps ",allCamps)
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
