mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var communityDatas="";
var k12Datas=""
$.get("CommunityPartners.geojson",function(data){
	communityDatas=jQuery.parseJSON(data);
})
$.get("K-12Partners.geojson",function(data){
	k12Datas=jQuery.parseJSON(data);
})

//Get map
var map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/mapbox/streets-v10',
	center: [-95.957309,41.276479],
	zoom:12
});

function parseDescription(message){
	var string=""

	for(var i in message){
		string+='<span>'+i+":"+message[i]+"</span><br>"
	}

	return string;
}

//Get style
map.on("load",function(){
	//GetcommunityPartner data
	map.addSource('communityDatas', {
		type: 'geojson',
		data: communityDatas,
	});
	//Get k12Partner data
	map.addSource("k12Datas",{
		type:"geojson",
		data:k12Datas,
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
						"circle-color": '#e55e5e'
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

	

	//******************************Show data when the mouse moves on it**********************************
	var popup = new mapboxgl.Popup({
		closeButton: false,
		closeOnClick: false
	});

	map.on("mouseenter","k12",function(e){
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
	});

	map.on("mouseenter","show1",function(e){
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
	});
	map.on("mouseenter","show2",function(e){
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
	});
	map.on("mouseenter","show3",function(e){
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
	});
	map.on("mouseenter","show4",function(e){
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
	});
	map.on("mouseenter","show5",function(e){
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
	});
	map.on("mouseenter","show6",function(e){
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
	});
	//********************************************************************************

	//*************************stop showing data when mouse leaves it**********************************
	map.on('mouseleave', 'k12', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	map.on('mouseleave', 'show1', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	map.on('mouseleave', 'show2', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	map.on('mouseleave', 'show3', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	map.on('mouseleave', 'show4', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	map.on('mouseleave', 'show5', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	map.on('mouseleave', 'show6', function() {
		map.getCanvas().style.cursor = '';
		popup.remove();
	});
	//********************************************************************************************

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
		}else if(value==2016){
			map.setFilter("k12",
				[
					'in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"
				]
			)

			map.setFilter("show1",
				["all",["==", "PrimaryMissionFocus", "Social Justice"],['in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"]]
			)
			map.setFilter("show2",
				["all",["==", "PrimaryMissionFocus", "Educational Support"],['in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"]]
			)
			map.setFilter("show3",
				["all",["==", "PrimaryMissionFocus", "Economic Sufficiency"],['in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"]]
			)
			map.setFilter("show4",
				["all",["==", "PrimaryMissionFocus", "International Service"],['in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"]]
			)
			map.setFilter("show5",
				["all",["==", "PrimaryMissionFocus", "Environmental Stewardship"],['in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"]]
			)
			map.setFilter("show6",
				["all",["==", "PrimaryMissionFocus", "Health & Wellness"],['in',"time","Spring 2016","Fall 2016","Summer 2016","winter 2016"]]
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

