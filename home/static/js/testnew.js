mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
// This adds the map to your page
if (!('remove' in Element.prototype)) {
    Element.prototype.remove = function() {
        if (this.parentNode) {
            this.parentNode.removeChild(this);
        }
    };
}

var filterInput = document.getElementById('filter-input');
var layerIDs = [];
var hoveredStateId = null;
var map = new mapboxgl.Map({
    // container id specified in the HTML
    container: 'map',
    // style URL
    style: 'mapbox://styles/mapbox/light-v9',
    // initial position in [lon, lat] format
    center: [-95.957309, 41.276479],
    // initial zoom
    zoom: 12
});

var popup = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: true
});
//******************************Create content for the popups**********************************

function parseDescription(message) {
    var string = ""


    for (var i in message) {

        if (i == "PhoneNumber") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        } else if (i == "Website") {
            var website = message[i];
            var base = "http://";
            if (website === null || website == "null" || website == "") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (!website.includes("http")) {
                website = base.concat(website);
                string += `<span style="font-weight:bold">${i}</span>:<a target="_blank" href="${website}" class="popup">${website}</a><br>`;
            } else {
                string += `<span style="font-weight:bold">${i}</span>:<a target="_blank" href="${website}" class="popup">${website}</a><br>`;
            }
        } else if (i == "PrimaryMissionFocus") {
            string += '<span style="font-weight:bold">' + "Primary Mission" + '</span>' + ": " + message[i] + "<br>"
        }else if(i=="time"){
            string += '<span style="font-weight:bold">' + "date" + '</span>' + ": " + message[i] + "<br>"
        }
    }
    return string;
}

//******************************Load data and put it on the map**********************************

var communityData = ""
var districtData = "";
var k12Datas = "";
$.get("static/GEOJSON/CommunityPartners.geojson", function(data) { //load JSON file from static/GEOJSON
    communityData = jQuery.parseJSON(data);
    var features=communityData["features"];
	var count=0;
	features.forEach(function(feature){
		feature.properties["id"]=count;
		count++;
	});
	communityData["features"]=features;
})
$.get("static/GEOJSON//K-12Partners.geojson", function(data) { //load JSON file from static/GEOJSON
    k12Datas = jQuery.parseJSON(data);
})
$.get("static/GEOJSON/ID2.geojson", function(data) { //load JSON file from static/GEOJSON
    districtData = jQuery.parseJSON(data);
})
map.addControl(new mapboxgl.NavigationControl());
map.on('load', function(e) {

    map.addSource('communityDatas', {
        type: 'geojson',
        data: communityData,
    });
    map.addSource("k12Datas", {
        type: "geojson",
        data: k12Datas,
    });
    map.addSource('districtData', {
        type: 'geojson',
        data: districtData,
    });
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
                        0.4
                    ],
                    "fill-outline-color": "#0000AA"
                },
                "filter": ["==", "id", symbol]
            });

            layerIDs.push(layerID);
        }
    })

    map.addLayer({
        "id": "district",
        "type": "fill",
        "source": "districtData",
        'layout': {},
        'paint': {
            "fill-color": "#888",
            "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                1,
                0.08
            ],
            "fill-outline-color": "#0000AA"
        }
    });

    // Add the data to your map as a layer
    communityData.features.forEach(function(feature) {
        var primary = feature.properties["PrimaryMissionFocus"];

        if (primary == "Social Justice") {
            layerID = "show1";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "communityDatas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#2A0A12'
                    },
                    "filter": ["all", ["==", "PrimaryMissionFocus", "Social Justice"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                })
            }
        } else if (primary == "Educational Support") {
            layerID = "show2";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "communityDatas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#fbb03b'
                    },
                    "filter": ["all", ["==", "PrimaryMissionFocus", "Educational Support"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                })
            }
        } else if (primary == "Economic Sufficiency") {
            layerID = "show3";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "communityDatas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#223b53'
                    },
                    "filter": ["all", ["==", "PrimaryMissionFocus", "Economic Sufficiency"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                })
            }
        } else if (primary == "International Service") {
            layerID = "show4";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "communityDatas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#e55e5e'
                    },
                    "filter": ["all", ["==", "PrimaryMissionFocus", "International Service"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                })
            }
        } else if (primary == "Environmental Stewardship") {
            layerID = "show5";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "communityDatas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#3bb2d0'
                    },
                    "filter": ["all", ["==", "PrimaryMissionFocus", "Environmental Stewardship"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                })
            }
        } else if (primary == "Health & Wellness") {
            layerID = "show6";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "communityDatas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#ba55d3'
                    },
                    "filter": ["all", ["==", "PrimaryMissionFocus", "Health & Wellness"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "winter 2018"]
                    ]
                })
            }
        }

    });
    // buildLocationList(communityData); //add partners to the left hand sidebar
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


    map.on('click', 'district', function(e) {
        popup.setLngLat(e.lngLat)
            .setHTML('<span style="font-weight:bold">District Number: </span>' + e.features[0].properties["id"])
            .addTo(map);
    });


    //****************************filter year*******************************************
    var selectYear = document.getElementById("selectYear");
    selectYear.addEventListener("change", function(e) {
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

    //******************************search community***********************************************
    var valueFilter=document.getElementById("valueFilter");
	var listings=document.getElementById('listings');

	//Press the listening button
	valueFilter.addEventListener("keydown",function(e){
		if(e.keyCode==8){
			map.setFilter("show1",["==", "PrimaryMissionFocus", "Social Justice"]);
			map.setFilter("show2",["==", "PrimaryMissionFocus", "Educational Support"]);
			map.setFilter("show3",["==", "PrimaryMissionFocus", "Economic Sufficiency"]);
			map.setFilter("show4",["==", "PrimaryMissionFocus", "International Service"]);
			map.setFilter("show5",["==", "PrimaryMissionFocus", "Environmental Stewardship"]);
			map.setFilter("show6",["==", "PrimaryMissionFocus", "Health & Wellness"]);
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
		}
	});



});
//******************************Show a marker when clicking on the list on the left hand side**********************************
function buildLocationList(data) {
    // Iterate through the list of stores
    for (i = 0; i < data.features.length; i++) {
        var currentFeature = data.features[i];
        // Shorten data.feature.properties to just `prop` so we're not
        // writing this long form over and over again.
        var prop = currentFeature.properties;
        var description = parseDescription(prop);
        // Select the listing container in the HTML and append a div
        // with the class 'item' for each store
        var listings = document.getElementById('listings');
        var listing = listings.appendChild(document.createElement('div'));
        listing.className = 'item';
        listing.id = 'listing-' + i;

        // Create a new link with the class 'title' for each store
        // and fill it with the store address
        var link = listing.appendChild(document.createElement('a'));
        link.href = '#';
        link.className = 'title';
        link.dataPosition = i;
        link.innerHTML = prop['CommunityPartner'];
        var details = listing.appendChild(document.createElement('div'));
        details.innerHTML = description;

        link.addEventListener('click', function(e) {
            // Update the currentFeature to the store associated with the clicked link
            var clickedListing = data.features[this.dataPosition];
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

    }
}
//******************************Create a flying effect and popup**********************************

function flyToStore(currentFeature) {
    map.flyTo({
        center: currentFeature.geometry.coordinates,
        zoom: 15
    });
}

function createPopUp(currentFeature) {

    var popUps = document.getElementsByClassName('mapboxgl-popup');
    // Check if there is already a popup on the map and if so, remove it
    if (popUps[0]) popUps[0].remove();

    new mapboxgl.Popup().setLngLat(currentFeature.geometry.coordinates)
        .setHTML('<h3>' + currentFeature.properties['CommunityPartner'] + '</h3>' +
            '<h4>' + currentFeature.properties['Address'] + '</h4>')
        .addTo(map);
    close();
}

//***********************************search function*****************************************************
function normalize(string) {
	return string.trim().toLowerCase();
}

function renderListings(features){
	listings.innerHTML = '';

	if (features.length) {
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


			var details = listing.appendChild(document.createElement('div'));
			details.innerHTML = description;
			i++;
		});

    } else {
    	var empty = document.createElement('p');
    	empty.textContent = 'Drag the map to populate results';
    	listings.appendChild(empty);

        listings.style.display = 'none';


    }
}

//******************************Add a clickable legend**********************************

var comlist = ["show1", "show2", "show3", "show4", "show5", "show6", "k12"];
var edu = document.getElementById("all");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show2") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'visible');
        }
    })

})

var edu = document.getElementById("educational");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show2") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("economic");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show3") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("service");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show4") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("environmental");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show5") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("health");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show6") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})
var edu = document.getElementById("justice");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show1") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})



