mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var countyData = JSON.parse(document.getElementById('county-data').textContent); //load the variable from views.py. See the line from html first

var k12Data = "";
var communityData = "";
var referencedincome = 0;
$.get("static/GEOJSON/CommunityPartners_new.geojson", function(data) { //load JSON file from static/GEOJSON
    communityData = jQuery.parseJSON(data);
    var features=communityData["features"];
	var count=0;
	features.forEach(function(feature){
		feature.properties["id"]=count;
		count++;
	});
	communityData["features"]=features;
});
$.get("static/GEOJSON//K12Partners_new.geojson", function(data) { //load JSON file from static/GEOJSON
    k12Data = jQuery.parseJSON(data);
    var features=k12Data["features"];
    var count=0;
	features.forEach(function(feature){
		feature.properties["id"]=count;
		count++;
	});
	k12Data["features"]=features;
});


var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-95.957309, 41.276479],
    // initial zoom
    zoom: 6
});
map.addControl(new mapboxgl.NavigationControl());

var popup = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: true,
});


function parseDescription(message) {
    var string = "";


    for (var i in message) {


        if (i == "CommunityPartner") {
            string += '<span style="font-weight:bold">' + 'Community Partner' + '</span>' + ": " + message[i] + "<br>";
        }if (i == "K-12 Partner") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i =="Address"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "City"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "  ";
        } else if (i == "State"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "Website"){
            var website = message[i];
            var base = "http://";
            if (!website.includes("http")){
                website = base.concat(website);
            }
            string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${i}</a><br>`;
        } else if (i == "STATE"){
            string += '<span style="font-weight:bold">' + 'State' + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "NAME"){
            string += '<span style="font-weight:bold">' + 'County' + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "Income"){
            string += '<span style="font-weight:bold">' + 'Household Income' + '</span>' + ": " + message[i] + "<br>";
        } else if (i=="income"){
            string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + message[i] + "<br>"
        } else if (i=="County"){
            string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + message[i] + "<br>"
        } else if (i=="district"){
            string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + message[i] + "<br>"
        }
    }
    return string;
};

map.on("load",function() {

    //Get Legislative District Data
    map.addSource('countyData', {
        type: 'geojson',
        data: countyData,
    });
    map.addSource('communityData', {
        type: 'geojson',
        data: communityData,
    });
    //Get k12Partner data
    map.addSource("k12Data", {
        type: "geojson",
        data: k12Data,
    });
 	//Add k12 style
	map.addLayer({
		"id":"county",
		"type":"fill",
		"source":"countyData",
        'paint': {
            "fill-color": "#888",
            "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                1,
                0.0
            ],
            "fill-outline-color": "#0000AA"
        }
	});

    communityData.features.forEach(function(feature){
		var primary=feature.properties["PrimaryMissionFocus"];

		if(primary=="Social Justice"){
			layerID="show1";
			if(!map.getLayer(layerID)){
				map.addLayer({
					"id":layerID,
					"type":"circle",
					"source":"communityData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#FFFF00'
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
					"source":"communityData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#65dc1e'
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
					"source":"communityData",
					"paint":{
						"circle-radius": 8,
						"circle-opacity": 0.8,
						"circle-color": '#17f3d1'
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
					"source":"communityData",
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
					"source":"communityData",
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
					"source":"communityData",
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

    map.addLayer({
		"id":"k12",
		"type":"circle",
		"source":"k12Data",
		"paint":{
			"circle-radius": 8,
			"circle-opacity": 1,
			"circle-color": '#2F4F4F'
		},
		//Default filter year to 2018 in map
		"filter":['in',"time","Spring 2018","Fall 2018","Summer 2018","winter 2018"]
	});
	//******************************Add a county map **********************************
    countyData.features.forEach(function(feature) {
        var income = feature.properties["Income"];
        if (30000 <= income && income < 45000) {
            layerID = "income1";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "fill",
                    "source": "countyData",
                    'layout': {},
                    'paint': {
                        "fill-color": "#A4A4A4",
                        "fill-opacity": ["case",
                            ["boolean", ["feature-state", "hover"], false],
                            1,
                            0.5],
                        "fill-outline-color": "#0000AA"
                    },
                    "filter": ["all",
                        [">=", "Income", 30000],
                        ["<", "Income", 45000]
                    ]
                })
            }
        } else if (45000 <= income && income < 60000) {
            layerID = "income2";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "fill",
                    "source": "countyData",
                    'layout': {},
                    'paint': {
                        "fill-color": "#6E6E6E",
                        "fill-opacity": ["case",
                            ["boolean", ["feature-state", "hover"], false],
                            1,
                            0.5],
                        "fill-outline-color": "#0000AA"
                    },
                    "filter": ["all",
                        [">=", "Income", 45000],
                        ["<", "Income", 60000]
                    ]
                })
            }
        } else {
            layerID = "income3";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "fill",
                    "source": "countyData",
                    'layout': {},
                    'paint': {
                        "fill-color": "#424242",
                        "fill-opacity": ["case",
                            ["boolean", ["feature-state", "hover"], false],
                            1,
                            0.8],
                        "fill-outline-color": "#0000AA"
                    },
                    "filter": [">=", "Income", 60000]
                })
            }
        }
    })

        //******************************Add a clickable legend**********************************

        var comlist = ["show1", "show2", "show3", "show4", "show5", "show6", "k12"];
        var edu = document.getElementById("k12partner");
        edu.addEventListener("click", function(e) {
            comlist.forEach(function(com) {
                if (com == "k12") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })
        })

        var edu = document.getElementById("all");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show2") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                }
            })

        })

        var edu = document.getElementById("educational");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show2") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })

        })

        var edu = document.getElementById("economic");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show3") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })

        })

        var edu = document.getElementById("service");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show4") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })

        })

        var edu = document.getElementById("environmental");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show5") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })

        })

        var edu = document.getElementById("health");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show6") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })

        })
        var edu = document.getElementById("justice");
        edu.addEventListener("click", function (e) {
            comlist.forEach(function (com) {
                if (com == "show1") {
                    map.setLayoutProperty(com, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(com, 'visibility', 'none');
                }
            })

        })


        //****************************filter year*******************************************
        var selectYear = document.getElementById("selectYear");
        selectYear.addEventListener("change", function (e) {
            var value = e.target.value.trim().toLowerCase();

            if (value == 2018) {
                map.setFilter("show1",
                    ["all", ["==", "PrimaryMissionFocus", "Social Justice"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                )
                map.setFilter("show2",
                    ["all", ["==", "PrimaryMissionFocus", "Educational Support"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                )
                map.setFilter("show3",
                    ["all", ["==", "PrimaryMissionFocus", "Economic Sufficiency"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                )
                map.setFilter("show4",
                    ["all", ["==", "PrimaryMissionFocus", "International Service"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                )
                map.setFilter("show5",
                    ["all", ["==", "PrimaryMissionFocus", "Environmental Stewardship"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                )
                map.setFilter("show6",
                    ["all", ["==", "PrimaryMissionFocus", "Health & Wellness"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                )
            } else if (value == 2017) {

                map.setFilter("show1",
                    ["all", ["==", "PrimaryMissionFocus", "Social Justice"],
                        ['in', "time", "Spring 2017", "Fall 2017", "Summer 2017", "winter 2017"]
                    ]
                )
                map.setFilter("show2",
                    ["all", ["==", "PrimaryMissionFocus", "Educational Support"],
                        ['in', "time", "Spring 2017", "Fall 2017", "Summer 2017", "winter 2017"]
                    ]
                )
                map.setFilter("show3",
                    ["all", ["==", "PrimaryMissionFocus", "Economic Sufficiency"],
                        ['in', "time", "Spring 2017", "Fall 2017", "Summer 2017", "winter 2017"]
                    ]
                )
                map.setFilter("show4",
                    ["all", ["==", "PrimaryMissionFocus", "International Service"],
                        ['in', "time", "Spring 2017", "Fall 2017", "Summer 2017", "winter 2017"]
                    ]
                )
                map.setFilter("show5",
                    ["all", ["==", "PrimaryMissionFocus", "Environmental Stewardship"],
                        ['in', "time", "Spring 2017", "Fall 2017", "Summer 2017", "winter 2017"]
                    ]
                )
                map.setFilter("show6",
                    ["all", ["==", "PrimaryMissionFocus", "Health & Wellness"],
                        ['in', "time", "Spring 2017", "Fall 2017", "Summer 2017", "winter 2017"]
                    ]
                )
            } else { //all

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
    // //******************************Add an event when clicking on each item on the left-hand sidebar**********************************
    map.on('click', function(e) {
        // Query all the rendered points in the view
        map.getCanvas().style.cursor = 'pointer';
        var features = map.queryRenderedFeatures(e.point, {
            layers: ['show1', 'show2', 'show3',
                'show4', 'show5', 'show6'
            ]
        });
        if (features.length) {
            var clickedPoint = features[0];
            // 1. Fly to the point
            flyToStore(clickedPoint);
            // 2. Close all other popups and display popup for clicked store
            createPopUp(clickedPoint);
            // 3. Highlight listing in sidebar (and remove highlight for all other listings)
            var activeItem = document.getElementsByClassName('active');
            if (activeItem[0]) {
                activeItem[0].classList.remove('active');
            }
            // Find the index of the store.features that corresponds to the clickedPoint that fired the event listener
            var selectedFeature = clickedPoint.properties['Address'];

            for (var i = 0; i < communityData.features.length; i++) {
                if (communityData.features[i].properties['Address'] === selectedFeature) {
                    selectedFeatureIndex = i;
                }
            }
            // Select the correct list item using the found index and add the active class
            var listing = document.getElementById('listing-' + selectedFeatureIndex);
            listing.classList.add('active');
        }
    });

    map.on('click', function(e) {
        // Query all the rendered points in the view
        map.getCanvas().style.cursor = 'pointer';
        var features = map.queryRenderedFeatures(e.point, {
            layers: ['k12']
        });
        if (features.length) {
            var clickedPoint = features[0];
            // 1. Fly to the point
            flyToStore(clickedPoint);
            // 2. Close all other popups and display popup for clicked store
            createPopUp(clickedPoint);
            // 3. Highlight listing in sidebar (and remove highlight for all other listings)
            var activeItem = document.getElementsByClassName('active');
            if (activeItem[0]) {
                activeItem[0].classList.remove('active');
            }
            // Find the index of the store.features that corresponds to the clickedPoint that fired the event listener
            var selectedFeature = clickedPoint.properties['Address'];

            for (var i = 0; i < k12Data.features.length; i++) {
                if (k12Data.features[i].properties['Address'] === selectedFeature) {
                    selectedFeatureIndex = i;
                }
            }
            // Select the correct list item using the found index and add the active class
            var listing = document.getElementById('listing-' + selectedFeatureIndex);
            listing.classList.add('active');
        }
    });
        //********************************************************************************
        map.on("click", "k12", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });

        map.on("click", "show1", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });
        map.on("click", "show2", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });
        map.on("click", "show3", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });
        map.on("click", "show4", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });
        map.on("click", "show5", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });
        map.on("click", "show6", function (e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);

            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });

    //******************************click county***********************************************

    map.on('click', 'county', function(e) {
        popup.setLngLat(e.lngLat)
            .setHTML('<span style="font-weight:bold">County: </span>' + e.features[0].properties["NAME"])
            .addTo(map);
    });

    //******************************search community***********************************************
    var valueFilter=document.getElementById("valueFilter");


	//Press the listening button
	valueFilter.addEventListener("keydown",function(e){
		if(e.keyCode==8){
			map.setFilter("show1",["==", "PrimaryMissionFocus", "Social Justice"]);
			map.setFilter("show2",["==", "PrimaryMissionFocus", "Educational Support"]);
			map.setFilter("show3",["==", "PrimaryMissionFocus", "Economic Sufficiency"]);
			map.setFilter("show4",["==", "PrimaryMissionFocus", "International Service"]);
			map.setFilter("show5",["==", "PrimaryMissionFocus", "Environmental Stewardship"]);
			map.setFilter("show6",["==", "PrimaryMissionFocus", "Health & Wellness"]);
			map.setFilter("k12",null);
		}
	});

    // the listening button off
	valueFilter.addEventListener("keyup",function(e){
		//get the input value
		var value=e.target.value.trim().toLowerCase();

		if(value==""){
			renderListings([]);
		}else{
			//get geojosn data from the map
			var cmValues1=map.queryRenderedFeatures({layers:['show1']});
			var cmValues2=map.queryRenderedFeatures({layers:['show2']});
			var cmValues3=map.queryRenderedFeatures({layers:['show3']});
			var cmValues4=map.queryRenderedFeatures({layers:['show4']});
			var cmValues5=map.queryRenderedFeatures({layers:['show5']});
			var cmValues6=map.queryRenderedFeatures({layers:['show6']});
			var cmValues7=map.queryRenderedFeatures({layers:['k12']});
			//filter the name(s) that include the input value
			var filtered1=cmValues1.filter(function(feature){
				var name=normalize(feature.properties.CommunityPartner);
				return name.indexOf(value)==0;
			});
			var filtered2=cmValues2.filter(function(feature){
				var name=normalize(feature.properties.CommunityPartner);
				return name.indexOf(value)==0;
			});
			var filtered3=cmValues3.filter(function(feature){
				var name=normalize(feature.properties.CommunityPartner);
				return name.indexOf(value)==0;
			});
			var filtered4=cmValues4.filter(function(feature){
				var name=normalize(feature.properties.CommunityPartner);
				return name.indexOf(value)==0;
			});
			var filtered5=cmValues5.filter(function(feature){
				var name=normalize(feature.properties.CommunityPartner);
				return name.indexOf(value)==0;
			});
			var filtered6=cmValues6.filter(function(feature){
				var name=normalize(feature.properties.CommunityPartner);
				return name.indexOf(value)==0;
			});
			var filtered7=cmValues7.filter(function(feature){
				var name=normalize(feature.properties["K-12 Partner"]);
				return name.indexOf(value)==0;
			});
			filtereds=filtered1.concat(filtered2,filtered3,filtered4,filtered5,filtered6);

			renderListings(filtereds);


			if(filtered1.length>0){
				map.setFilter("show1",['match',['get','id'],filtered1.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("show1",['match',['get','id'],-1,true,false]);
			}
			if(filtered2.length>0){
				map.setFilter("show2",['match',['get','id'],filtered2.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("show2",['match',['get','id'],-1,true,false]);
			}

			if(filtered3.length>0){
				map.setFilter("show3",['match',['get','id'],filtered3.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("show3",['match',['get','id'],-1,true,false]);
			}

			if(filtered4.length>0){
				map.setFilter("show4",['match',['get','id'],filtered4.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("show4",['match',['get','id'],-1,true,false]);
			}

			if(filtered5.length>0){
				map.setFilter("show5",['match',['get','id'],filtered5.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("show5",['match',['get','id'],-1,true,false]);
			}

			if(filtered6.length>0){
				map.setFilter("show6",['match',['get','id'],filtered6.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("show6",['match',['get','id'],-1,true,false]);
			}
			if(filtered7.length>0){
				map.setFilter("k12",['match',['get','id'],filtered7.map(function(feature){

					return feature.properties.id;
				}),true,false]);
			}else{
				map.setFilter("k12",['match',['get','id'],-1,true,false]);
			}
		}
	});

        /*
          map.on('mousemove', 'income1', function (e) {
           map.getCanvas().style.cursor = 'pointer';
           var description =  e.features[0].properties;
           description=parseDescription(description);
           popup.setLngLat(e.lngLat)
                .setHTML(description)
                .addTo(map)
       });
          map.on('mouseleave', 'income1', function() {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
          map.on('mousemove', 'income2', function (e) {
           map.getCanvas().style.cursor = 'pointer';
           var description =  e.features[0].properties;
           description=parseDescription(description);
           popup.setLngLat(e.lngLat)
                .setHTML(description)
                .addTo(map)
       });
          map.on('mouseleave', 'income2', function() {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
          map.on('mousemove', 'income3', function (e) {
           map.getCanvas().style.cursor = 'pointer';
           var description =  e.features[0].properties;
           description=parseDescription(description);
           popup.setLngLat(e.lngLat)
                .setHTML(description)
                .addTo(map)
       });
          map.on('mouseleave', 'income3', function() {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
          map.on('mousemove', 'income4', function (e) {
           map.getCanvas().style.cursor = 'pointer';
           var description =  e.features[0].properties;
           description=parseDescription(description);
           popup.setLngLat(e.lngLat)
                .setHTML(description)
                .addTo(map)
       });
          map.on('mouseleave', 'income4', function() {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
          map.on('mousemove', 'income5', function (e) {
           map.getCanvas().style.cursor = 'pointer';
           var description =  e.features[0].properties;
           description=parseDescription(description);
           popup.setLngLat(e.lngLat)
                .setHTML(description)
                .addTo(map)
       });
          map.on('mouseleave', 'income5', function() {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
    */
        //******************************** Filter by income levels ************************************************

        var countyList = ["income1", "income2", "income3"];
        var comlist = ["show1", "show2", "show3", "show4", "show5", "show6", "k12"];
        var edu = document.getElementById("allincome");
        edu.addEventListener("click", function (e) {
            countyList.forEach(function (county) {
                if (county == "income1") {
                    map.setLayoutProperty(county, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(county, 'visibility', 'visible');
                }
            })
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
            map.setFilter("k12", null)
        })


        var edu = document.getElementById("lowincome");
        edu.addEventListener("click", function (e) {
            countyList.forEach(function (county) {
                if (county == "income1") {
                    map.setLayoutProperty(county, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(county, 'visibility', 'none');
                }
            })
            map.setFilter("show1",
                ["all", ["==", "PrimaryMissionFocus", "Social Justice"],
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )
            map.setFilter("show2",
                ["all", ["==", "PrimaryMissionFocus", "Educational Support"],
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )
            map.setFilter("show3",
                ["all", ["==", "PrimaryMissionFocus", "Economic Sufficiency"],
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )
            map.setFilter("show4",
                ["all", ["==", "PrimaryMissionFocus", "International Service"],
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )
            map.setFilter("show5",
                ["all", ["==", "PrimaryMissionFocus", "Environmental Stewardship"],
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )
            map.setFilter("show6",
                ["all", ["==", "PrimaryMissionFocus", "Health & Wellness"],
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )
            map.setFilter("k12",
                ["all",
                    [">=", "income", 30000], ["<", "income", 45000]
                ]
            )

        })

        var edu = document.getElementById("midincome");
        edu.addEventListener("click", function (e) {
            countyList.forEach(function (county) {
                if (county == "income2") {
                    map.setLayoutProperty(county, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(county, 'visibility', 'none');
                }
            })
            map.setFilter("show1",
                ["all", ["==", "PrimaryMissionFocus", "Social Justice"],
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )
            map.setFilter("show2",
                ["all", ["==", "PrimaryMissionFocus", "Educational Support"],
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )
            map.setFilter("show3",
                ["all", ["==", "PrimaryMissionFocus", "Economic Sufficiency"],
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )
            map.setFilter("show4",
                ["all", ["==", "PrimaryMissionFocus", "International Service"],
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )
            map.setFilter("show5",
                ["all", ["==", "PrimaryMissionFocus", "Environmental Stewardship"],
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )
            map.setFilter("show6",
                ["all", ["==", "PrimaryMissionFocus", "Health & Wellness"],
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )
            map.setFilter("k12",
                ["all",
                    [">=", "income", 45000], ["<", "income", 60000]
                ]
            )

        })
        var edu = document.getElementById("topincome");
        edu.addEventListener("click", function (e) {
            countyList.forEach(function (county) {
                if (county == "income3") {
                    map.setLayoutProperty(county, 'visibility', 'visible');
                } else {
                    map.setLayoutProperty(county, 'visibility', 'none');
                }
            })
            map.setFilter("show1",
                ["all", ["==", "PrimaryMissionFocus", "Social Justice"],
                    [">", "income", 60000]
                ]
            )
            map.setFilter("show2",
                ["all", ["==", "PrimaryMissionFocus", "Educational Support"],
                    [">", "income", 60000]
                ]
            )
            map.setFilter("show3",
                ["all", ["==", "PrimaryMissionFocus", "Economic Sufficiency"],
                    [">", "income", 60000]
                ]
            )
            map.setFilter("show4",
                ["all", ["==", "PrimaryMissionFocus", "International Service"],
                    [">", "income", 60000]
                ]
            )
            map.setFilter("show5",
                ["all", ["==", "PrimaryMissionFocus", "Environmental Stewardship"],
                    [">", "income", 60000]
                ]
            )
            map.setFilter("show6",
                ["all", ["==", "PrimaryMissionFocus", "Health & Wellness"],
                    [">", "income", 60000]
                ]
            )
            map.setFilter("k12",
                ["all",
                    [">", "income", 60000]
                ]
            )
        })
    })
//***********************************search function*****************************************************
function normalize(string) {
	return string.trim().toLowerCase();
}


function renderListings(features){
    var parent = document.getElementById("sidebar");
    console.log(parent);
    var listings = document.getElementById("listings");
    console.log(listings);
    if(listings!=null){
        parent.removeChild(listings);
    }


	if (features.length) {

        listings = document.createElement("div");
        console.log(listings);
        listings.setAttribute("id", "listings");
        listings.setAttribute("class", "listings");

        parent.appendChild(listings);
        listings.innerHTML = '';

		var i=0;

		features.forEach(function(feature) {
			listings.style.display = 'block';

			var prop = feature.properties;
			var description = parseDescription(prop);

			var listing = listings.appendChild(document.createElement('div'));
			listing.className = 'item';
			listing.id = 'listing-' + i;

			var link = listing.appendChild(document.createElement('a'));
			link.href = '#';
			link.className = 'title';
			link.dataPosition = i;
            link.innerHTML = prop.CommunityPartner;
            link.addEventListener('click', function(e) {
                // Update the currentFeature to the store associated with the clicked link
                var clickedListing = features[this.dataPosition];
                // 1. Fly to the point associated with the clicked link
                flyToStore(clickedListing);
                // 2. Close all other popups and display popup for clicked store
                createPopUp(clickedListing);
                // 3. Highlight listing in sidebar (and remove highlight for all other listings)
                var activeItem = document.getElementsByClassName('active');
                if (activeItem[0]) {
                    activeItem[0].classList.remove('active');
                }
                this.parentNode.classList.add('active');
            });


//			var details = listing.appendChild(document.createElement('div'));
//			details.innerHTML = description;
			i++;
		});

    } else {
    	var empty = document.createElement('p');
    	empty.textContent = 'Drag the map to populate results';
    	listings.appendChild(empty);

        listings.style.display = 'none';


    }
}
//******************************Create a flying effect and popup**********************************

function flyToStore(currentFeature) {
    map.flyTo({
        center: currentFeature.geometry.coordinates,
        zoom: 8
    });
}

function createPopUp(currentFeature) {

    var popUps = document.getElementsByClassName('mapboxgl-popup');
    // Check if there is already a popup on the map and if so, remove it
    if (popUps[0]) popUps[0].remove();
    var description = parseDescription(currentFeature.properties)
    new mapboxgl.Popup().setLngLat(currentFeature.geometry.coordinates)
        .setHTML(description)
        .addTo(map);
    close();
}