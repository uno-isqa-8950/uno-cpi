mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var communityDatas="";
var k12Datas=""
var districtData=""
var projectData=""
$.get("static/GEOJSON/CommunityPartners.geojson",function(data){ //load JSON file from static/GEOJSON
	communityDatas=jQuery.parseJSON(data);
})
$.get("static/GEOJSON//K-12Partners.geojson",function(data){ //load JSON file from static/GEOJSON
	k12Datas=jQuery.parseJSON(data);
})
$.get("static/GEOJSON/ID2.geojson",function(data){ //load JSON file from static/GEOJSON
	districtData=jQuery.parseJSON(data);
})
$.get("static/GEOJSON/Projects.geojson",function(data){ //load JSON file from static/GEOJSON
	projectData=jQuery.parseJSON(data);
})

var hoveredStateId =  null; //this variable is used for hovering over the districts
var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
var names = [];
var filterInput = document.getElementById('filter-input'); //this is for filtering the Legislative Districts
//var CommunityPartnerInput = document.getElementById('filter-input2');//this is for searching community partner
var ProjectInput;
//Get map
var map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/mapbox/streets-v10',
	center: [-95.957309,41.276479],
	zoom:3
});
map.addControl(new mapboxgl.NavigationControl());
map.addControl(new mapboxgl.FullscreenControl());
//parsing the description
function parseDescription(message) {
    var string = ""


    for (var i in message) {

        if (i == "ProjectName") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        }if (i == "ProjectMission") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        } else if (i == "PhoneNumber") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        } else if (i == "Website"){
            var website = message[i]
            var base = "http://"
            if (!website.includes("http")){
                website = base.concat(website)
            }
			//string += '<span style="font-weight:bold">' + i + '</span>: <a target="_blank" href="' + message[i] + '">' + message[i] + '</a><br>';
			string += `<span style="font-weight:bold">${i}</span>:<a target="_blank" href="${website}" class="popup">${website}</a><br>`;
        }
    }
    return string;
}

//Get style
map.on("load",function(){

	//Get Legislative District Data
	map.addSource('districtData', {
		type: 'geojson',
		data: districtData,
	});
	map.addSource('communityDatas', {
		type: 'geojson',
		data: communityDatas,
	});
	//Get k12Partner data
	map.addSource("k12Datas",{
		type:"geojson",
		data:k12Datas,
	});

	//Get Project data
		map.addSource("projectData",{
		type:"geojson",
		data:projectData,
	});
	//This function is to create multiple layers, each of which corresponds to the number of the district
    districtData.features.forEach(function(feature) {
        var symbol = feature.properties['id'];
        var layerID = 'poi-' + symbol;

        if (!map.getLayer(layerID)) {
            map.addLayer({
                "id": layerID,
                "type": "fill",
                "source": "districtData",
                'layout': {},
                'paint': {
                    "fill-color": "#888",
                    "fill-opacity": ["case",
                        ["boolean", ["feature-state", "hover"], false],
                        1,
                        0.5],
                    "fill-outline-color": "#0000AA"
                },
                "filter": ["==", "id", symbol]
            });

            layerIDs.push(layerID);
        }
    })


    //add the "normal" legislative districts
	map.addLayer({
            "id":"district",
            "type":"fill",
            "source":"districtData",
            'layout': {},
            'paint': {
                "fill-color": "#B233FF",
                "fill-opacity": ["case",
                    ["boolean", ["feature-state", "hover"], false],
                    1,
                    0.08],
                "fill-outline-color": "#0000AA"
            }
        });

	//Add k12 style
//	map.addLayer({
//		"id":"k12",
//		"type":"circle",
//		"source":"k12Datas",
//		"paint":{
//			"circle-radius": 8,
//			"circle-opacity": 0.8,
//			"circle-color": '#0000AA'
//		},
//		//Default filter year to 2018 in map
//		"filter":['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]
//	});

	//Add Project style
//	map.addLayer({
//		"id":"project",
//		"type":"circle",
//		"source":"projectData",
//		"paint":{
//			"circle-radius": 8,
//			"circle-opacity": 0.8,
//			"circle-color": '#0000AA'
//		},
//		//Default filter year to 2018 in map
//		"filter":['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]
//	});
	//add project layer
    projectData.features.forEach(function(feature){
		var primary=feature.properties["ProjectMission"];
		var projectname=feature.properties["ProjectName"];

		if(primary=="Social Justice"){
			layerID="show1";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"projectData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#2A0A12'
					},
					"filter": ["all",["==", "ProjectMission", "Social Justice"],['in' ,"ProjectName" ,projectname],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Educational Support"){
			layerID="show2";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"projectData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#fbb03b'
					},
					"filter": ["all",["==", "ProjectMission", "Educational Support"],['in' ,"ProjectName" ,projectname],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Economic Sufficiency"){
			layerID="show3";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"projectData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#223b53'
					},
					"filter": ["all",["==", "ProjectMission", "Economic Sufficiency"],['in',"ProjectName" ,projectname],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="International Service" ){
			layerID="show4";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"projectData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#e55e5e'
					},
					"filter": ["all",["==", "ProjectMission", "International Service"],['in' ,"ProjectName" ,projectname],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Environmental Stewardship"){
			layerID="show5";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"projectData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#3bb2d0'
					},
					"filter": ["all",["==", "ProjectMission", "Environmental Stewardship"],['in' ,"ProjectName" ,projectname],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Health & Wellness"){
			layerID="show6";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"projectData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#ba55d3'
					},
					"filter": ["all",["==", "ProjectMission", "Health & Wellness"],['in' ,"ProjectName" ,projectname],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
            names.push(layerID);
	})

	//****************************filter year*******************************************
	var selectYear=document.getElementById("selectYear");
	selectYear.addEventListener("change",function(e){
		var value=e.target.value.trim().toLowerCase();
        if(value==2018){
			map.setFilter("show1",
				["all",["==", "ProjectMission", "Social Justice"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show2",
				["all",["==", "ProjectMission", "Educational Support"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show3",
				["all",["==", "ProjectMission", "Economic Sufficiency"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show4",
				["all",["==", "ProjectMission", "International Service"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show5",
				["all",["==", "ProjectMission", "Environmental Stewardship"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show6",
				["all",["==", "ProjectMission", "Health & Wellness"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
		}else if(value==2017){
//			map.setFilter("k12",
//				[
//					'in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"
//				]
//			)

			map.setFilter("show1",
				[["==", "ProjectMission", "Social Justice"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show2",
				[["==", "ProjectMission", "Educational Support"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show3",
				[["==", "ProjectMission", "Economic Sufficiency"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show4",
				[["==", "ProjectMission", "International Service"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show5",
				[["==", "ProjectMission", "Environmental Stewardship"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show6",
				[["==", "ProjectMission", "Health & Wellness"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
	      }else{//all
//			map.setFilter("k12",null)

			map.setFilter("show1",
				["==", "ProjectMission", "Social Justice"]
			)
			map.setFilter("show2",
				["==", "ProjectMission", "Educational Support"]
			)
			map.setFilter("show3",
				["==", "ProjectMission", "Economic Sufficiency"]
			)
			map.setFilter("show4",
				["==", "ProjectMission", "International Service"]
			)
			map.setFilter("show5",
				["==", "ProjectMission", "Environmental Stewardship"]
			)
			map.setFilter("show6",
				["==", "ProjectMission", "Health & Wellness"]
			)
		}

	})

	var selectMission=document.getElementById("selectMission");
	selectMission.addEventListener("change",function(e){

		var value=e.target.value.trim().toLowerCase();

		var comlist=["show1","show2","show3","show4","show5","show6"];

		if(value==0){
			comlist.forEach(function(com){
				map.setLayoutProperty(com, 'visibility','visible');
			})
		}else if(value==1){
			comlist.forEach(function(com){
				if(com=="show1"){
					map.setLayoutProperty(com, 'visibility','visible');
				}else{
					map.setLayoutProperty(com, 'visibility','none');
				}
			})
		}else if(value==2){
			comlist.forEach(function(com){
				if(com=="show2"){
					map.setLayoutProperty(com, 'visibility','visible');
				}else{
					map.setLayoutProperty(com, 'visibility','none');
				}
			})
		}else if(value==3){
			comlist.forEach(function(com){
				if(com=="show2"){
					map.setLayoutProperty(com, 'visibility','visible');
				}else{
					map.setLayoutProperty(com, 'visibility','none');
				}
			})
		}else if(value==4){
			comlist.forEach(function(com){
				if(com=="show3"){
					map.setLayoutProperty(com, 'visibility','visible');
				}else{
					map.setLayoutProperty(com, 'visibility','none');
				}
			})
		}else if(value==5){
			comlist.forEach(function(com){
				if(com=="show4"){
					map.setLayoutProperty(com, 'visibility','visible');
				}else{
					map.setLayoutProperty(com, 'visibility','none');
				}
			})
		}else if(value==6){
			comlist.forEach(function(com){
				if(com=="show1"){
					map.setLayoutProperty(com, 'visibility','visible');
				}else{
					map.setLayoutProperty(com, 'visibility','none');
				}
			})
		}
	})

});