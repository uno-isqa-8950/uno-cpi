//*********************************** Get mapbox API and get data from HTML *****************************************************

mapboxgl.accessToken = 'pk.eyJ1IjoibWluaGR1b25nMjQzIiwiYSI6ImNqbHNvM3l0cTAxaXMzcHBiYnpvNjBsaXAifQ.NO598_UKYbyOIok45baiWA';
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00'];
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var showlist = [] //the array of layerIDs, used to categorize layers
var base = "show"
for (var i = 0; i < Missionarea.length; i++) { //populate showlist array
    var text = base + i
    showlist.push(text)
}
var projectData = JSON.parse(document.getElementById('project-data').textContent); //load the variable from views.py. See the line from html first

//*********************************** Add id variable to Project Data GEOJSON for search function later *****************************************************
var count = 0;
projectData.features.forEach(function(feature) {
    feature.properties["id"] = count;
    count++;
});
//*********************************** Load the map *****************************************************

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


// //*********************************** Dynamically add the legends *****************************************************
var select = '';
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allmissions"><span style="background-color: black"></span><b>All Mission Areas</b></a>' + "<br>";
for (var i = 0; i < Missionarea.length; i++) {
    var color = colorcode[i]
    var mission = Missionarea[i]
    select += `<a href="#"  id="${mission.valueOf()}" value="${mission.valueOf()}"><span style="background-color: ${color}"></span><b>${mission.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);

//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option val=' + "all" + '>' + "All District" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);
//*********************************** Load the county data here. Should be down here. Otherwise it won't load *****************************************************

var countyData = JSON.parse(document.getElementById('county-data').textContent);
//*********************************** Format the popup *****************************************************


var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});

function parseDescription(message) {
    var string = "";


    for (var i in message) {

        if (i == "Project Name") {
            string += '<span style="font-weight:bold">' + 'Project Name' + '</span>' + " : " + message[i] + "<br>"
        }
        if (i == "Mission Area") {
            string += '<span style="font-weight:bold">' + ' Mission Area' + '</span>' + " : " + message[i] + "<br>"

        } else if (i == "Address") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "City") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "  ";
        } else if (i == "Legislative District Number") {
            string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "Income") {
            string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + formatter.format(message[i]) + "<br>"
        } else if (i == "County") {
            string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + message[i] + "<br>"
        }
    }
    return string;
};
// //*********************************** Load the map *****************************************************

map.on("load", function() {

    map.addSource('projectData', {
        type: 'geojson',
        data: projectData,
    });
    // map.addSource('countyData', {
    //     type: 'geojson',
    //     data: countyData,
    // });

    //*********************************** Load project data *****************************************************
    projectData.features.forEach(function(feature) {
        var primary = feature.properties["Mission Area"];
        var base = "show";
        for (var i = 0; i < Missionarea.length; i++) {
            if (primary == Missionarea[i]) {
                layerID = showlist[i];
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "circle",
                        "source": "projectData",
                        "paint": {
                            "circle-radius": 8,
                            "circle-opacity": 1,
                            "circle-color": colorcode[i],
                        },
                        "filter": ["all", ["==", "Mission Area", primary]]
                    })
                }
            }
        }
    });


    //*********************************** function to show pop-up when clicking on the partner *****************************************************

    for (var i = 0; i < showlist.length; i++) {
        map.on("click", showlist[i], function(e) { //go through every layer. Refer to showlist
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties;
            description = parseDescription(description);
            map.flyTo({
                center: e.features[0].geometry.coordinates
            });
            popup.setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            close();
        });
    }
    //*********************************** District filter *****************************************************

    var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function(e) {
        var value = e.target.value.trim().toLowerCase();
        value = parseInt(value)
        if (isNaN(value)) {
            for (var i = 0; i < showlist.length; i++) {
                map.setFilter(showlist[i], ["all", ["==", "Mission Area", Missionarea[i]]])
            }
            // get the number of markers that fit the requirement and show on the HTML
            var totalnumber = '';
            totalnumber = totalnumber + projectData.features.length;
            $('#totalnumber').html(totalnumber);

        } else {
            for (var j = 0; j < showlist.length; j++) {
                map.setFilter(showlist[j], ["all", ["==", "Mission Area", Missionarea[j]],
                    ["==", "Legislative District Number", value]
                ])
            }
            // get the number of markers that fit the requirement and show on the HTML
            var totalnumber = '';
            var number = 0;
            projectData.features.forEach(function(e) {
                if (e.properties['Legislative District Number'] == value) {
                    number += 1;
                }
            })
            totalnumber += number;
            $('#totalnumber').html(totalnumber);

        }

    })
});



//***********************************clickable legends*****************************************************

var edu = document.getElementById("all"); //get the total number of dots
edu.addEventListener("click", function(e) {
    showlist.forEach(function(com) {
        map.setLayoutProperty(com, 'visibility', 'visible');
    })
    var totalnumber = ''

    totalnumber += projectData.features.length;
    $('#totalnumber').html(totalnumber);
})

$('#legend a').click(function(e) { //filter dots by mission areas and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    console.log(clickedValue)
    var i = Missionarea.indexOf(clickedValue);
    if (i > -1) {
        var show = showlist[i];
        showlist.forEach(function(com) {
            if (com == show) {
                map.setLayoutProperty(com, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(com, 'visibility', 'none');
            }
        })
        var totalnumber = ''
        var number = 0
        projectData.features.forEach(function(e) {
            console.log(Missionarea[i])
            if (e.properties['Mission Area'] == clickedValue) {
                number += 1
            }
        })
        totalnumber += number
        $('#totalnumber').html(totalnumber);
    }
});


// mapboxgl.accessToken = 'pk.eyJ1IjoibWluaGR1b25nMjQzIiwiYSI6ImNqbHNvM3l0cTAxaXMzcHBiYnpvNjBsaXAifQ.NO598_UKYbyOIok45baiWA'
//
// var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
// var names = [];
// var filterInput = document.getElementById('filter-input'); //this is for filtering the Legislative Districts
// //Get map
// var map = new mapboxgl.Map({
//     container: 'map',
//     style: 'mapbox://styles/mapbox/light-v9',
//     center: [-95.957309, 41.276479],
//     // initial zoom
//     zoom: 6
// });
// map.addControl(new mapboxgl.NavigationControl());
// var formatter = new Intl.NumberFormat('en-US', {
//   style: 'currency',
//   currency: 'USD',
//   minimumFractionDigits: 2,
// });
// var popup;
// popup = new mapboxgl.Popup({
//     closeButton: true,
//     closeOnClick: true
// });
//
// function parseDescription(message) {
//     var string = ""
//
//
//     for (var i in message) {
//
//         if (i == "ProjectName") {
//             string += '<span style="font-weight:bold">' + 'Project Name' + '</span>' + " : " + message[i] + "<br>"
//         }
//         if (i == "ProjectMission") {
//             string += '<span style="font-weight:bold">' + 'Project Mission Area' + '</span>' + " : " + message[i] + "<br>"
//         } else if (i == "Website") {
//             var website = message[i];
//             var base = "http://";
//             if (website === null || website == "null" || website == "") {
//                 website.hide();
//             } else
//             if (!website.includes("http")) {
//                 website = base.concat(website);
//                 string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${i}</a><br>`;
//             } else {
//                 string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${i}</a><br>`;
//             }
//         } else if (i == "Address") {
//             string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
//         } else if (i == "City") {
//             string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "  ";
//         } else if (i == "district") {
//             string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + message[i] + "<br>";
//         } else if (i=="income"){
//             string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + formatter.format(message[i]) + "<br>"
//         } else if (i=="County"){
//             string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + message[i] + "<br>"
//         }
//     }
//     return string;
// };
//
// ///****************Load data*************************//
//
// var districtData = "";
// var projectData = "";
// $.get("static/GEOJSON/ID2.geojson", function(data) { //load JSON file from static/GEOJSON
//     districtData = jQuery.parseJSON(data);
// });
// $.get("static/GEOJSON/Projects_new.geojson", function(data) { //load JSON file from static/GEOJSON
//     projectData = jQuery.parseJSON(data);
//     var features = projectData["features"];
//     var count = 0;
//     features.forEach(function(feature) {
//         feature.properties["id"] = count;
//         count++;
//     });
//     projectData["features"] = features;
// });
//
// //Get style
// map.on("load", function() {
// /*
//     //Get Legislative District Data
//     map.addSource('districtData', {
//         type: 'geojson',
//         data: districtData,
//     });
// */
//     //Get Project data
//     map.addSource("projectData", {
//         type: "geojson",
//         data: projectData,
//     });
// /*
//     //This function is to create multiple layers, each of which corresponds to the number of the district
//     districtData.features.forEach(function(feature) {
//         var symbol = feature.properties['id'];
//         var layerID = 'poi-' + symbol;
//
//         if (!map.getLayer(layerID)) {
//             map.addLayer({
//                 "id": layerID,
//                 "type": "fill",
//                 "source": "districtData",
//                 'layout': {},
//                 'paint': {
//                     "fill-color": "#888",
//                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
//                         1,
//                         0.5
//                     ],
//                     "fill-outline-color": "#0000AA"
//                 },
//                 "filter": ["==", "id", symbol]
//             });
//
//             layerIDs.push(layerID);
//         }
//     })
//
//
//     //add the "normal" legislative districts
//     map.addLayer({
//         "id": "district",
//         "type": "fill",
//         "source": "districtData",
//         'layout': {},
//         'paint': {
//             "fill-color": "#B233FF",
//             "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
//                 1,
//                 0.08
//             ],
//             "fill-outline-color": "#0000AA"
//         }
//     });
// */
//     //add project layer
//     projectData.features.forEach(function(feature) {
//             var primary = feature.properties["ProjectMission"];
//             var projectname = feature.properties["ProjectName"];
//
//             if (primary == "Social Justice") {
//                 layerID = "show1";
//                 if (!map.getLayer(layerID)) {
//                     map.addLayer({
//                         "id": layerID,
//                         "type": "circle",
//                         "source": "projectData",
//                         "paint": {
//                             "circle-radius": 8,
//                             "circle-opacity": 0.8,
//                             "circle-color": '#FFFF00'
//                         },
//                         "filter": ["all", ["==", "ProjectMission", "Social Justice"],
//                             ['in', "Semester", "Fall 2016", "Spring 2017", "Summer 2017", "Fall 2017",
//                                 "Spring 2018", "Fall 2018", "Summer 2018"
//                             ]
//                         ]
//                     })
//                 }
//             } else if (primary == "Educational Support") {
//                 layerID = "show2";
//                 if (!map.getLayer(layerID)) {
//                     map.addLayer({
//                         "id": layerID,
//                         "type": "circle",
//                         "source": "projectData",
//                         "paint": {
//                             "circle-radius": 8,
//                             "circle-opacity": 0.8,
//                             "circle-color": '#65dc1e'
//                         },
//                         "filter": ["all", ["==", "ProjectMission", "Educational Support"],
//                             ['in', "Semester", "Fall 2016", "Spring 2017", "Summer 2017", "Fall 2017",
//                                 "Spring 2018", "Fall 2018", "Summer 2018"
//                             ]
//                         ]
//                     })
//                 }
//             } else if (primary == "Economic Sufficiency") {
//                 layerID = "show3";
//                 if (!map.getLayer(layerID)) {
//                     map.addLayer({
//                         "id": layerID,
//                         "type": "circle",
//                         "source": "projectData",
//                         "paint": {
//                             "circle-radius": 8,
//                             "circle-opacity": 0.8,
//                             "circle-color": '#17f3d1'
//                         },
//                         "filter": ["all", ["==", "ProjectMission", "Economic Sufficiency"],
//                             ['in', "Semester", "Fall 2016", "Spring 2017", "Summer 2017", "Fall 2017",
//                                 "Spring 2018", "Fall 2018", "Summer 2018"
//                             ]
//                         ]
//                     })
//                 }
//             } else if (primary == "International Service") {
//                 layerID = "show4";
//                 if (!map.getLayer(layerID)) {
//                     map.addLayer({
//                         "id": layerID,
//                         "type": "circle",
//                         "source": "projectData",
//                         "paint": {
//                             "circle-radius": 8,
//                             "circle-opacity": 0.8,
//                             "circle-color": '#e55e5e'
//                         },
//                         "filter": ["all", ["==", "ProjectMission", "International Service"],
//                             ['in', "Semester", "Fall 2016", "Spring 2017", "Summer 2017", "Fall 2017",
//                                 "Spring 2018", "Fall 2018", "Summer 2018"
//                             ]
//                         ]
//                     })
//                 }
//             } else if (primary == "Environmental Stewardship") {
//                 layerID = "show5";
//                 if (!map.getLayer(layerID)) {
//                     map.addLayer({
//                         "id": layerID,
//                         "type": "circle",
//                         "source": "projectData",
//                         "paint": {
//                             "circle-radius": 8,
//                             "circle-opacity": 0.8,
//                             "circle-color": '#3bb2d0'
//                         },
//                         "filter": ["all", ["==", "ProjectMission", "Environmental Stewardship"],
//                             ['in', "Semester", "Fall 2016", "Spring 2017", "Summer 2017", "Fall 2017",
//                                 "Spring 2018", "Fall 2018", "Summer 2018"
//                             ]
//                         ]
//                     })
//                 }
//             } else if (primary == "Health & Wellness") {
//                 layerID = "show6";
//                 if (!map.getLayer(layerID)) {
//                     map.addLayer({
//                         "id": layerID,
//                         "type": "circle",
//                         "source": "projectData",
//                         "paint": {
//                             "circle-radius": 8,
//                             "circle-opacity": 0.8,
//                             "circle-color": '#ba55d3'
//                         },
//                         "filter": ["all", ["==", "ProjectMission", "Health & Wellness"],
//                             ['in', "Semester", "Fall 2016", "Spring 2017", "Summer 2017", "Fall 2017",
//                                 "Spring 2018", "Fall 2018", "Summer 2018"
//                             ]
//                         ]
//                     })
//                 }
//             }
//             names.push(layerID);
//         })
//         //******************************Add a clickable legend**********************************
//
//     var comlist = ["show1", "show2", "show3", "show4", "show5", "show6"];
//     var edu = document.getElementById("all");
//     edu.addEventListener("click", function(e) {
//         comlist.forEach(function(com) {
//             if (com == "show2") {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             }
//         })
//
//     })
//
//     var edu = document.getElementById("educational");
//     edu.addEventListener("click", function(e) {
//         comlist.forEach(function(com) {
//             if (com == "show2") {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'none');
//             }
//         })
//
//     })
//
//     var edu = document.getElementById("economic");
//     edu.addEventListener("click", function(e) {
//         comlist.forEach(function(com) {
//             if (com == "show3") {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'none');
//             }
//         })
//
//     })
//
//     var edu = document.getElementById("service");
//     edu.addEventListener("click", function(e) {
//         comlist.forEach(function(com) {
//             if (com == "show4") {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'none');
//             }
//         })
//
//     })
//
//     var edu = document.getElementById("environmental");
//     edu.addEventListener("click", function(e) {
//         comlist.forEach(function(com) {
//             if (com == "show5") {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'none');
//             }
//         })
//
//     })
//
//     var edu = document.getElementById("health");
//     edu.addEventListener("click", function(e) {
//         comlist.forEach(function(com) {
//             if (com == "show6") {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'none');
//             }
//         })
//
//     })
//     var edu = document.getElementById("justice");
//     edu.addEventListener("click", function(e) {
//             comlist.forEach(function(com) {
//                 if (com == "show1") {
//                     map.setLayoutProperty(com, 'visibility', 'visible');
//                 } else {
//                     map.setLayoutProperty(com, 'visibility', 'none');
//                 }
//             })
//
//         })
//         //************************************Search Project ******************************
//
//     var valueFilter = document.getElementById("valueFilter");
//     var listings = document.getElementById('listings');
//
//
//     valueFilter.addEventListener("keydown", function(e) {
//         if (e.keyCode == 8) {
//             map.setFilter("show1", ["==", "ProjectMission", "Social Justice"]);
//             map.setFilter("show2", ["==", "ProjectMission", "Educational Support"]);
//             map.setFilter("show3", ["==", "ProjectMission", "Economic Sufficiency"]);
//             map.setFilter("show4", ["==", "ProjectMission", "International Service"]);
//             map.setFilter("show5", ["==", "ProjectMission", "Environmental Stewardship"]);
//             map.setFilter("show6", ["==", "ProjectMission", "Health & Wellness"]);
//         }
//     });
//
//
//     valueFilter.addEventListener("keyup", function(e) {
//
//         var value = e.target.value.trim().toLowerCase();
//
//         if (value == "") {
//             renderListings([]);
//
//         } else {
//
//             var cmValues1 = map.queryRenderedFeatures({
//                 layers: ['show1']
//             });
//             var cmValues2 = map.queryRenderedFeatures({
//                 layers: ['show2']
//             });
//             var cmValues3 = map.queryRenderedFeatures({
//                 layers: ['show3']
//             });
//             var cmValues4 = map.queryRenderedFeatures({
//                 layers: ['show4']
//             });
//             var cmValues5 = map.queryRenderedFeatures({
//                 layers: ['show5']
//             });
//             var cmValues6 = map.queryRenderedFeatures({
//                 layers: ['show6']
//             });
//
//
//             var filtered1 = cmValues1.filter(function(feature) {
//                 var name = normalize(feature.properties.ProjectName);
//                 return name.indexOf(value) == 0;
//             });
//             var filtered2 = cmValues2.filter(function(feature) {
//                 var name = normalize(feature.properties.ProjectName);
//                 return name.indexOf(value) == 0;
//             });
//             var filtered3 = cmValues3.filter(function(feature) {
//                 var name = normalize(feature.properties.ProjectName);
//                 return name.indexOf(value) == 0;
//             });
//             var filtered4 = cmValues4.filter(function(feature) {
//                 var name = normalize(feature.properties.ProjectName);
//                 return name.indexOf(value) == 0;
//             });
//             var filtered5 = cmValues5.filter(function(feature) {
//                 var name = normalize(feature.properties.ProjectName);
//                 return name.indexOf(value) == 0;
//             });
//             var filtered6 = cmValues6.filter(function(feature) {
//                 var name = normalize(feature.properties.ProjectName);
//                 return name.indexOf(value) == 0;
//             });
//
//             filtereds = filtered1.concat(filtered2, filtered3, filtered4, filtered5, filtered6);
//
//             renderListings(filtereds);
//
//
//             if (filtered1.length > 0) {
//                 map.setFilter("show1", ['match', ['get', 'id'], filtered1.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show1", ['match', ['get', 'id'], -1, true, false]);
//             }
//             if (filtered2.length > 0) {
//                 map.setFilter("show2", ['match', ['get', 'id'], filtered2.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show2", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered3.length > 0) {
//                 map.setFilter("show3", ['match', ['get', 'id'], filtered3.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show3", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered4.length > 0) {
//                 map.setFilter("show4", ['match', ['get', 'id'], filtered4.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show4", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered5.length > 0) {
//                 map.setFilter("show5", ['match', ['get', 'id'], filtered5.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show5", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered6.length > 0) {
//                 map.setFilter("show6", ['match', ['get', 'id'], filtered6.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show6", ['match', ['get', 'id'], -1, true, false]);
//             }
//         }
//     });
//
//     //*******************************Search by legislative district*************************///
//
//     //******************************Show a marker when clicking on the list on the left hand side**********************************
//     function buildLocationList(data) {
//         // Iterate through the list of stores
//         for (i = 0; i < data.features.length; i++) {
//             var currentFeature = data.features[i];
//             // Shorten data.feature.properties to just `prop` so we're not
//             // writing this long form over and over again.
//             var prop = currentFeature.properties;
//             var description = parseDescription(prop);
//             // Select the listing container in the HTML and append a div
//             // with the class 'item' for each store
//             var listings = document.getElementById('listings');
//             var listing = listings.appendChild(document.createElement('div'));
//             listing.className = 'item';
//             listing.id = 'listing-' + i;
//
//             // Create a new link with the class 'title' for each store
//             // and fill it with the store address
//             var link = listing.appendChild(document.createElement('a'));
//             link.href = '#';
//             link.className = 'title';
//             link.dataPosition = i;
//             link.innerHTML = prop['ProjectName'];
//             var details = listing.appendChild(document.createElement('div'));
//             details.innerHTML = description;
//
//             link.addEventListener('click', function(e) {
//                 // Update the currentFeature to the store associated with the clicked link
//                 var clickedListing = data.features[this.dataPosition];
//                 // 1. Fly to the point associated with the clicked link
//                 flyToStore(clickedListing);
//                 // 2. Close all other popups and display popup for clicked store
//                 createPopUp(clickedListing);
//                 // 3. Highlight listing in sidebar (and remove highlight for all other listings)
//                 var activeItem = document.getElementsByClassName('active');
//                 if (activeItem[0]) {
//                     activeItem[0].classList.remove('active');
//                 }
//                 this.parentNode.classList.add('active');
//             });
//
//         }
//     }
//     //******************************Create a flying effect and popup**********************************
//
//     function flyToStore(currentFeature) {
//         map.flyTo({
//             center: currentFeature.geometry.coordinates,
//             zoom: 6
//         });
//     }
//
//     function createPopUp(currentFeature) {
//
//         var popUps = document.getElementsByClassName('mapboxgl-popup');
//         // Check if there is already a popup on the map and if so, remove it
//         if (popUps[0]) popUps[0].remove();
//         var description = parseDescription(currentFeature.properties)
//         new mapboxgl.Popup().setLngLat(currentFeature.geometry.coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     }
//
//     //***********************************search function*****************************************************
//     function normalize(string) {
//         return string.trim().toLowerCase();
//     }
//
//     function renderListings(features) {
//         listings.innerHTML = '';
//
//         if (features.length) {
//             var i = 0;
//             features.forEach(function(feature) {
//                 listings.style.display = 'block';
//
//                 var prop = feature.properties;
//                 var description = parseDescription(prop);
//
//                 var listing = listings.appendChild(document.createElement('div'));
//                 listing.className = 'item';
//                 listing.id = 'listing-' + i;
//
//                 var link = listing.appendChild(document.createElement('a'));
//                 link.href = '#';
//                 link.className = 'title';
//                 link.dataPosition = i;
//                 link.innerHTML = prop.ProjectName;
//                 link.addEventListener('click', function(e) {
//                     // Update the currentFeature to the store associated with the clicked link
//                     var clickedListing = features[this.dataPosition];
//                     // 1. Fly to the point associated with the clicked link
//                     flyToStore(clickedListing);
//                     // 2. Close all other popups and display popup for clicked store
//                     createPopUp(clickedListing);
//                     // 3. Highlight listing in sidebar (and remove highlight for all other listings)
//                     var activeItem = document.getElementsByClassName('active');
//                     if (activeItem[0]) {
//                         activeItem[0].classList.remove('active');
//                     }
//                     this.parentNode.classList.add('active');
//                 });
//
//
//                 //			var details = listing.appendChild(document.createElement('div'));
//                 //			details.innerHTML = description;
//                 i++;
//             });
//
//         } else {
//             var empty = document.createElement('p');
//             empty.textContent = 'Drag the map to populate results';
//             listings.appendChild(empty);
//
//             listings.style.display = 'none';
//
//
//         }
//     }
//     //**********************************Dropdown Legislative District********************************
//     //   var selectDistrict = document.getElementById("districtid");
//     //    selectDistrict.addEventListener("change", function(e) {
//     //        var value = e.target.value.trim();
//     //        var comlist=["show1","show2","show3","show4","show5","show6"];//community id
//     //            map.setFilter("show1", ['in', "districtnumber", value])
//     //            map.setFilter("show2", ['in', "districtnumber", value])
//     //            map.setFilter("show3", ['in', "districtnumber", value])
//     //            map.setFilter("show4", ['in', "districtnumber", value])
//     //            map.setFilter("show5", ['in', "districtnumber", value])
//     //            map.setFilter("show6", ['in', "districtnumber", value])
//     //            })
//     //******************************Search Legislative District**********************************
// /*
//     filterInput.addEventListener("keydown", function(e) {
//
//         map.setFilter("show1", ["==", "ProjectMission", "Social Justice"]);
//         map.setFilter("show2", ["==", "ProjectMission", "Educational Support"]);
//         map.setFilter("show3", ["==", "ProjectMission", "Economic Sufficiency"]);
//         map.setFilter("show4", ["==", "ProjectMission", "International Service"]);
//         map.setFilter("show5", ["==", "ProjectMission", "Environmental Stewardship"]);
//         map.setFilter("show6", ["==", "ProjectMission", "Health & Wellness"]);
//
//     });
//
//     filterInput.addEventListener('keyup', function(e) {
//         // If the input value matches a layerID set
//         // it's visibility to 'visible' or else hide it.
//         var value = e.target.value.trim().toLowerCase();
//         if (value == "") {
//             map.setFilter("show1", ["==", "ProjectMission", "Social Justice"]);
//             map.setFilter("show2", ["==", "ProjectMission", "Educational Support"]);
//             map.setFilter("show3", ["==", "ProjectMission", "Economic Sufficiency"]);
//             map.setFilter("show4", ["==", "ProjectMission", "International Service"]);
//             map.setFilter("show5", ["==", "ProjectMission", "Environmental Stewardship"]);
//             map.setFilter("show6", ["==", "ProjectMission", "Health & Wellness"]);
//
//         } else if (value != "") {
//             console.log(value);
//             layerIDs.forEach(function(layerID) {
//                 console.log("dis:" + layerID.length);
//
//                 map.setLayoutProperty(layerID, 'visibility',
//                     (layerID.indexOf(value) == 4) && (layerID.length == (value.length + 4)) ? 'visible' : 'none');
//             });
//             //get geojosn data from the map
//             var cmValues1 = map.queryRenderedFeatures({
//                 layers: ['show1']
//             });
//             var cmValues2 = map.queryRenderedFeatures({
//                 layers: ['show2']
//             });
//             var cmValues3 = map.queryRenderedFeatures({
//                 layers: ['show3']
//             });
//             var cmValues4 = map.queryRenderedFeatures({
//                 layers: ['show4']
//             });
//             var cmValues5 = map.queryRenderedFeatures({
//                 layers: ['show5']
//             });
//             var cmValues6 = map.queryRenderedFeatures({
//                 layers: ['show6']
//             });
//
//             //filter the name(s) that include the input value
//             var filtered1 = cmValues1.filter(function(feature) {
//                 var districtnumber = normalize(feature.properties.district.toString());
//                 console.log("1:" + districtnumber);
//                 console.log(districtnumber == value);
//                 return districtnumber == value;
//             });
//             var filtered2 = cmValues2.filter(function(feature) {
//                 var districtnumber = normalize(feature.properties.district.toString());
//                 console.log(districtnumber == value);
//                 return districtnumber == value;
//             });
//             var filtered3 = cmValues3.filter(function(feature) {
//                 var districtnumber = normalize(feature.properties.district.toString());
//                 console.log(districtnumber == value);
//                 return districtnumber == value;
//             });
//             var filtered4 = cmValues4.filter(function(feature) {
//                 var districtnumber = normalize(feature.properties.district.toString());
//                 console.log(districtnumber == value);
//                 return districtnumber == value;
//             });
//             var filtered5 = cmValues5.filter(function(feature) {
//                 var districtnumber = normalize(feature.properties.district.toString());
//                 console.log(districtnumber == value);
//                 return districtnumber == value;
//             });
//             var filtered6 = cmValues6.filter(function(feature) {
//                 var districtnumber = normalize(feature.properties.district.toString());
//                 console.log(districtnumber == value);
//                 return districtnumber == value;
//             });
//
//             filtereds = filtered1.concat(filtered2, filtered3, filtered4, filtered5, filtered6);
//
//
//             if (filtered1.length > 0) {
//                 map.setFilter("show1", ['match', ['get', 'id'], filtered1.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show1", ['match', ['get', 'id'], -1, true, false]);
//             }
//             if (filtered2.length > 0) {
//                 map.setFilter("show2", ['match', ['get', 'id'], filtered2.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show2", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered3.length > 0) {
//                 map.setFilter("show3", ['match', ['get', 'id'], filtered3.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show3", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered4.length > 0) {
//                 map.setFilter("show4", ['match', ['get', 'id'], filtered4.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show4", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered5.length > 0) {
//                 map.setFilter("show5", ['match', ['get', 'id'], filtered5.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show5", ['match', ['get', 'id'], -1, true, false]);
//             }
//
//             if (filtered6.length > 0) {
//                 map.setFilter("show6", ['match', ['get', 'id'], filtered6.map(function(feature) {
//
//                     return feature.properties.id;
//                 }), true, false]);
//             } else {
//                 map.setFilter("show6", ['match', ['get', 'id'], -1, true, false]);
//             }
//         }
//
//     });
// */
//     //******************************Search Community Part**********************************
//     //******************************Show data when the mouse moves on it**********************************
// /*
//     map.on('click', 'district', function(e) {
//         popup.setLngLat(e.lngLat)
//             .setHTML('<span style="font-weight:bold">District Number: </span>' + e.features[0].properties["id"])
//             .addTo(map);
//     });
//     */
//     //****************************Event when clicking on partners*******************************************
//     map.on("click", "show1", function(e) {
//         map.getCanvas().style.cursor = 'pointer';
//         var coordinates = e.features[0].geometry.coordinates.slice();
//         var description = e.features[0].properties;
//         description = parseDescription(description);
//
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }
//
//         popup.setLngLat(coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     });
//     map.on("click", "show2", function(e) {
//         map.getCanvas().style.cursor = 'pointer';
//         var coordinates = e.features[0].geometry.coordinates.slice();
//         var description = e.features[0].properties;
//         description = parseDescription(description);
//
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }
//
//         popup.setLngLat(coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     });
//     map.on("click", "show3", function(e) {
//         map.getCanvas().style.cursor = 'pointer';
//         var coordinates = e.features[0].geometry.coordinates.slice();
//         var description = e.features[0].properties;
//         description = parseDescription(description);
//
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }
//
//         popup.setLngLat(coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     });
//     map.on("click", "show4", function(e) {
//         map.getCanvas().style.cursor = 'pointer';
//         var coordinates = e.features[0].geometry.coordinates.slice();
//         var description = e.features[0].properties;
//         description = parseDescription(description);
//
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }
//
//         popup.setLngLat(coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     });
//     map.on("click", "show5", function(e) {
//         map.getCanvas().style.cursor = 'pointer';
//         var coordinates = e.features[0].geometry.coordinates.slice();
//         var description = e.features[0].properties;
//         description = parseDescription(description);
//
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }
//
//         popup.setLngLat(coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     });
//     map.on("click", "show6", function(e) {
//         map.getCanvas().style.cursor = 'pointer';
//         var coordinates = e.features[0].geometry.coordinates.slice();
//         var description = e.features[0].properties;
//         description = parseDescription(description);
//
//         while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//             coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//         }
//
//         popup.setLngLat(coordinates)
//             .setHTML(description)
//             .addTo(map);
//         close();
//     });
//     //****************************filter year*******************************************
//     var selectYear = document.getElementById("selectYear");
//     selectYear.addEventListener("change", function(e) {
//         var value = e.target.value.trim().toLowerCase();
//         if (value == 2018) {
//             map.setFilter("show1", ["all", ["==", "ProjectMission", "Social Justice"],
//                 ['in', "Semester", "Spring 2018", "Fall 2018", "Summer 2018"]
//             ])
//             map.setFilter("show2", ["all", ["==", "ProjectMission", "Educational Support"],
//                 ['in', "Semester", "Spring 2018", "Fall 2018", "Summer 2018"]
//             ])
//             map.setFilter("show3", ["all", ["==", "ProjectMission", "Economic Sufficiency"],
//                 ['in', "Semester", "Spring 2018", "Fall 2018", "Summer 2018"]
//             ])
//             map.setFilter("show4", ["all", ["==", "ProjectMission", "International Service"],
//                 ['in', "Semester", "Spring 2018", "Fall 2018", "Summer 2018"]
//             ])
//             map.setFilter("show5", ["all", ["==", "ProjectMission", "Environmental Stewardship"],
//                 ['in', "Semester", "Spring 2018", "Fall 2018", "Summer 2018"]
//             ])
//             map.setFilter("show6", ["all", ["==", "ProjectMission", "Health & Wellness"],
//                 ['in', "Semester", "Spring 2018", "Fall 2018", "Summer 2018"]
//             ])
//         } else if (value == 2017) {
//
//             map.setFilter("show1", ["all", ["==", "PrimaryMission", "Social Justice"],
//                 ['in', "Semester", "Spring 2017", "Fall 2017", "Summer 2017"]
//             ])
//             map.setFilter("show2", ["all", ["==", "PrimaryMission", "Educational Support"],
//                 ['in', "Semester", "Spring 2017", "Fall 2017", "Summer 2017"]
//             ])
//             map.setFilter("show3", ["all", ["==", "PrimaryMission", "Economic Sufficiency"],
//                 ['in', "Semester", "Spring 2017", "Fall 2017", "Summer 2017"]
//             ])
//             map.setFilter("show4", ["all", ["==", "PrimaryMission", "International Service"],
//                 ['in', "Semester", "Spring 2017", "Fall 2017", "Summer 2017"]
//             ])
//             map.setFilter("show5", ["all", ["==", "PrimaryMission", "Environmental Stewardship"],
//                 ['in', "Semester", "Spring 2017", "Fall 2017", "Summer 2017"]
//             ])
//             map.setFilter("show6", ["all", ["==", "PrimaryMission", "Health & Wellness"],
//                 ['in', "Semester", "Spring 2017", "Fall 2017", "Summer 2017"]
//             ])
//         } else if (value == 2016) {
//             map.setFilter("show1", ["all", ["==", "PrimaryMission", "Social Justice"],
//                 ['in', "Semester", "Fall 2016"]
//             ])
//             map.setFilter("show2", ["all", ["==", "PrimaryMission", "Educational Support"],
//                 ['in', "Semester", "Fall 2016"]
//             ])
//             map.setFilter("show3", ["all", ["==", "PrimaryMission", "Economic Sufficiency"],
//                 ['in', "Semester", "Fall 2016"]
//             ])
//             map.setFilter("show4", ["all", ["==", "PrimaryMission", "International Service"],
//                 ['in', "Semester", "Fall 2016"]
//             ])
//             map.setFilter("show5", ["all", ["==", "PrimaryMission", "Environmental Stewardship"],
//                 ['in', "Semester", "Fall 2016"]
//             ])
//             map.setFilter("show6", ["all", ["==", "PrimaryMission", "Health & Wellness"],
//                 ['in', "Semester", "Fall 2016"]
//             ])
//         } else { //all
//
//             map.setFilter("show1", ["==", "ProjectMission", "Social Justice"])
//             map.setFilter("show2", ["==", "ProjectMission", "Educational Support"])
//             map.setFilter("show3", ["==", "ProjectMission", "Economic Sufficiency"])
//             map.setFilter("show4", ["==", "ProjectMission", "International Service"])
//             map.setFilter("show5", ["==", "ProjectMission", "Environmental Stewardship"])
//             map.setFilter("show6", ["==", "ProjectMission", "Health & Wellness"])
//         }
//
//     })
//
// });