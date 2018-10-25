mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var communityDatas="";
var k12Datas="";
var districtData="";
$.get("static/GEOJSON/CommunityPartners.geojson",function(data){ //load JSON file from static/GEOJSON
	communityDatas=jQuery.parseJSON(data);
})
$.get("static/GEOJSON//K-12Partners.geojson",function(data){ //load JSON file from static/GEOJSON
	k12Datas=jQuery.parseJSON(data);
})
$.get("static/GEOJSON/ID2.geojson",function(data){ //load JSON file from static/GEOJSON
	districtData=jQuery.parseJSON(data);
})
var hoveredStateId =  null; //this variable is used for hovering over the districts
var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
var filterInput = document.getElementById('filter-input'); //this is for filtering the Legislative Districts
//Get map
var map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/mapbox/streets-v10',
	center: [-95.957309,41.276479],
	zoom:4
});

var popup = new mapboxgl.Popup({
		closeButton: true,
		closeOnClick: true
});
map.addControl(new mapboxgl.NavigationControl());
//parsing the description
function parseDescription(message) {
    var string = ""


    for (var i in message) {

        if (i == "CommunityPartner") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        }if (i == "K-12 Partner") {
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
	map.addLayer({
		"id":"k12",
		"type":"circle",
		"source":"k12Datas",
		"paint":{
			"circle-radius": 8,
			"circle-opacity": 0.8,
			"circle-color": '#0000AA'
		},
		//Default filter year to 2018 in map
		"filter":['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]
	});
    //add community partner layer
    communityDatas.features.forEach(function(feature){
		var primary=feature.properties["PrimaryMissionFocus"];

		if(primary=="Social Justice"){
			layerID="show1";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityDatas",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#2A0A12'
					},
					"filter": ["all",["==", "PrimaryMissionFocus", "Social Justice"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Educational Support"){
			layerID="show2";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityDatas",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#fbb03b'
					},
					"filter": ["all",["==", "PrimaryMissionFocus", "Educational Support"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Economic Sufficiency"){
			layerID="show3";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityDatas",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#223b53'
					},
					"filter": ["all",["==", "PrimaryMissionFocus", "Economic Sufficiency"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="International Service"){
			layerID="show4";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityDatas",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#e55e5e'
					},
					"filter": ["all",["==", "PrimaryMissionFocus", "International Service"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Environmental Stewardship"){
			layerID="show5";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityDatas",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#3bb2d0'
					},
					"filter": ["all",["==", "PrimaryMissionFocus", "Environmental Stewardship"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}
		else if(primary=="Health & Wellness"){
			layerID="show6";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityDatas",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#ba55d3'
					},
					"filter": ["all",["==", "PrimaryMissionFocus", "Health & Wellness"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
				})
			}
		}

	})

	//******************************Add a clickable legend**********************************

    var comlist=["show1","show2","show3","show4","show5","show6", "k12"];
			var edu=document.getElementById("all");
				edu.addEventListener("click",function(e){
					comlist.forEach(function (com) {
						if (com == "show2") {
							map.setLayoutProperty(com, 'visibility', 'visible');
						} else {
							map.setLayoutProperty(com, 'visibility', 'visible');
						}
					})

				})

			var edu=document.getElementById("educational");
			edu.addEventListener("click",function(e){
				comlist.forEach(function (com) {
					if (com == "show2") {
						map.setLayoutProperty(com, 'visibility', 'visible');
					} else {
						map.setLayoutProperty(com, 'visibility', 'none');
					}
				})

			})

			var edu=document.getElementById("economic");
			edu.addEventListener("click",function(e){
				comlist.forEach(function (com) {
					if (com == "show3") {
						map.setLayoutProperty(com, 'visibility', 'visible');
					} else {
						map.setLayoutProperty(com, 'visibility', 'none');
					}
				})

			})

			var edu=document.getElementById("service");
			edu.addEventListener("click",function(e){
				comlist.forEach(function (com) {
					if (com == "show4") {
						map.setLayoutProperty(com, 'visibility', 'visible');
					} else {
						map.setLayoutProperty(com, 'visibility', 'none');
					}
				})

			})

			var edu=document.getElementById("environmental");
			edu.addEventListener("click",function(e){
				comlist.forEach(function (com) {
					if (com == "show5") {
						map.setLayoutProperty(com, 'visibility', 'visible');
					} else {
						map.setLayoutProperty(com, 'visibility', 'none');
					}
				})

			})

			var edu=document.getElementById("health");
			edu.addEventListener("click",function(e){
				comlist.forEach(function (com) {
					if (com == "show6") {
						map.setLayoutProperty(com, 'visibility', 'visible');
					} else {
						map.setLayoutProperty(com, 'visibility', 'none');
					}
				})

			})
			var edu=document.getElementById("justice");
			edu.addEventListener("click",function(e){
				comlist.forEach(function (com) {
					if (com == "show1") {
						map.setLayoutProperty(com, 'visibility', 'visible');
					} else {
						map.setLayoutProperty(com, 'visibility', 'none');
					}
				})

			})

	//******************************Search Legislative District**********************************
    filterInput.addEventListener('keyup', function(e) {
        // If the input value matches a layerID set
        // it's visibility to 'visible' or else hide it.
        var value = e.target.value.trim().toLowerCase();
        layerIDs.forEach(function(layerID) {
            map.setLayoutProperty(layerID, 'visibility',
                layerID.indexOf(value) > -1 ? 'visible' : 'none');
        });
    });
	//******************************Search Community Part**********************************
	//******************************Show data when the mouse moves on it**********************************

    map.on("mousemove", "district", function(e) {
        if (e.features.length > 0) {
            if (hoveredStateId) {
                map.setFeatureState({source: 'districtData', id: hoveredStateId}, { hover: false});
            }
            hoveredStateId = e.features[0].id;
            map.setFeatureState({source: 'districtData', id: hoveredStateId}, { hover: true});
        }
    });

    map.on("mouseleave", "district", function() {
        if (hoveredStateId) {
            map.setFeatureState({source: 'districtData', id: hoveredStateId}, { hover: false});
        }
        hoveredStateId =  null;
    });


	map.on('click', 'district', function (e) {
        new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML('<span style="font-weight:bold">District Number: </span>' + e.features[0].properties["id"])
            .addTo(map);
    });

	map.on("click","k12",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setHTML(description)
		.addTo(map);
		close();
	});

	map.on("click","show1",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setLngLat(coordinates)
		.setHTML(description)
		.addTo(map);
		close();
	});
	map.on("click","show2",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setLngLat(coordinates)
		.setHTML(description)
		.addTo(map);
		close();
	});
	map.on("click","show3",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setLngLat(coordinates)
		.setHTML(description)
		.addTo(map);
		close();
	});
	map.on("click","show4",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setLngLat(coordinates)
		.setHTML(description)
		.addTo(map);
		close();
	});
	map.on("click","show5",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setLngLat(coordinates)
		.setHTML(description)
		.addTo(map);
		close();
	});
	map.on("click","show6",function(e){
		map.getCanvas().style.cursor = 'pointer';
		var coordinates = e.features[0].geometry.coordinates.slice();
		var description =  e.features[0].properties;
		description=parseDescription(description);

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		popup.setLngLat(coordinates)
		.setHTML(description)
		.addTo(map);
		close();
	});
	//********************************************************************************


	//*****************************filter communityPartner***********************************************************
	var selectType=document.getElementById("selectType");
	selectType.addEventListener("change",function(e){
		
		var value=e.target.value.trim().toLowerCase();

		var comlist=["show1","show2","show3","show4","show5","show6"];//community id

		
		if(value=="all"){
			comlist.forEach(function(com){
				map.setLayoutProperty(com, 'visibility','visible');
			})
			map.setLayoutProperty("k12", 'visibility','visible');
		}else if(value=="community"){
			comlist.forEach(function(com){
				map.setLayoutProperty(com, 'visibility','visible');
			})
			map.setLayoutProperty("k12", 'visibility','none');
		}else if(value=="k12"){
			comlist.forEach(function(com){
				map.setLayoutProperty(com, 'visibility','none');
			})
			map.setLayoutProperty("k12", 'visibility','visible');
		}
	})


	//****************************filter year*******************************************
	var selectYear=document.getElementById("selectYear");
	selectYear.addEventListener("change",function(e){
		var value=e.target.value.trim().toLowerCase();

		if(value==2018){
			map.setFilter("k12",
				['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]
			)
			
			map.setFilter("show1",
				["all",["==", "PrimaryMissionFocus", "Social Justice"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show2",
				["all",["==", "PrimaryMissionFocus", "Educational Support"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show3",
				["all",["==", "PrimaryMissionFocus", "Economic Sufficiency"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show4",
				["all",["==", "PrimaryMissionFocus", "International Service"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show5",
				["all",["==", "PrimaryMissionFocus", "Environmental Stewardship"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
			map.setFilter("show6",
				["all",["==", "PrimaryMissionFocus", "Health & Wellness"],['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]]
			)
		}else if(value==2017){
			map.setFilter("k12",
				[
					'in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"
				]
			)

			map.setFilter("show1",
				["all",["==", "PrimaryMissionFocus", "Social Justice"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show2",
				["all",["==", "PrimaryMissionFocus", "Educational Support"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show3",
				["all",["==", "PrimaryMissionFocus", "Economic Sufficiency"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show4",
				["all",["==", "PrimaryMissionFocus", "International Service"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show5",
				["all",["==", "PrimaryMissionFocus", "Environmental Stewardship"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
			map.setFilter("show6",
				["all",["==", "PrimaryMissionFocus", "Health & Wellness"],['in',"time","Spring 2017","Fall 2017","Summer 2017","winter 2017"]]
			)
		}else{//all
			map.setFilter("k12",null)

			map.setFilter("show1",
				["==", "PrimaryMissionFocus", "Social Justice"]
			)
			map.setFilter("show2",
				["==", "PrimaryMissionFocus", "Educational Support"]
			)
			map.setFilter("show3",
				["==", "PrimaryMissionFocus", "Economic Sufficiency"]
			)
			map.setFilter("show4",
				["==", "PrimaryMissionFocus", "International Service"]
			)
			map.setFilter("show5",
				["==", "PrimaryMissionFocus", "Environmental Stewardship"]
			)
			map.setFilter("show6",
				["==", "PrimaryMissionFocus", "Health & Wellness"]
			)
		}
		
	})

});

