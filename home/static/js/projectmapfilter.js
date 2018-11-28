//*********************************** Get mapbox API and get data from HTML *****************************************************

mapboxgl.accessToken = 'pk.eyJ1IjoibWluaGR1b25nMjQzIiwiYSI6ImNqbHNvM3l0cTAxaXMzcHBiYnpvNjBsaXAifQ.NO598_UKYbyOIok45baiWA';
var colorcode = ['#17f3d1','#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00'];
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var EngagementType = JSON.parse(document.getElementById('engagementlist').textContent);
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

//*********************************** Add the Engagement *****************************************************

var select3 = '';
select3 += '<option val=' + "all" + '>' + "All Engagement Types" + '</option>';
for (var i = 0; i < EngagementType.length; i++) {
var engagement = EngagementType[i] ;
select3 += '<option val=' + {engagement:valueOf()} + '>' + i + '</option>';
}
$('#selectEngagement').html(select3);
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
        } else if (i == "district") {
            string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + message[i] + "<br>";
        } else if (i=="income"){
            string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + formatter.format(message[i]) + "<br>"
        } else if (i=="County"){
            string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + message[i] + "<br>"
        }else if (i=="Activity Type"){
            string += '<span style="font-weight:bold">' + "Activity Type" + '</span>' + ": " + message[i] + "<br>"
        }else if (i=="Engagement Type"){
            string += '<span style="font-weight:bold">' + "Engagement Type" + '</span>' + ": " + message[i] + "<br>"
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
    map.addSource('countyData', {
        type: 'geojson',
        data: countyData,
    });


    //*********************************** Load the county in different household income levels *****************************************************
    //
    // countyData.features.forEach(function(feature) {
    //     var income = feature.properties["Income"];
    //     if (income < 25000) {
    //         layerID = "income1";
    //         if (!map.getLayer(layerID)) {
    //             map.addLayer({
    //                 "id": layerID,
    //                 "type": "fill",
    //                 "source": "countyData",
    //                 'layout': {},
    //                 'paint': {
    //                     "fill-color": "#B8B8B8",
    //                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
    //                         1,
    //                         0.5
    //                     ],
    //                     "fill-outline-color": "#0000AA"
    //                 },
    //                 "filter": ["all", ["<", "Income", 25000]]
    //             })
    //         }
    //     } else if (25000 <= income && income < 40000) {
    //         layerID = "income2";
    //         if (!map.getLayer(layerID)) {
    //             map.addLayer({
    //                 "id": layerID,
    //                 "type": "fill",
    //                 "source": "countyData",
    //                 'layout': {},
    //                 'paint': {
    //                     "fill-color": "#989898",
    //                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
    //                         1,
    //                         0.5
    //                     ],
    //                     "fill-outline-color": "#0000AA"
    //                 },
    //                 "filter": ["all", [">=", "Income", 25000],
    //                     ["<", "Income", 40000]
    //                 ]
    //             })
    //         }
    //     } else if (40000 <= income && income < 60000) {
    //         layerID = "income3";
    //         if (!map.getLayer(layerID)) {
    //             map.addLayer({
    //                 "id": layerID,
    //                 "type": "fill",
    //                 "source": "countyData",
    //                 'layout': {},
    //                 'paint': {
    //                     "fill-color": "#808080",
    //                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
    //                         1,
    //                         0.5
    //                     ],
    //                     "fill-outline-color": "#0000AA"
    //                 },
    //                 "filter": ["all", [">=", "Income", 40000],
    //                     ["<", "Income", 60000]
    //                 ]
    //             })
    //         }
    //     } else if (60000 <= income && income < 80000) {
    //         layerID = "income4";
    //         if (!map.getLayer(layerID)) {
    //             map.addLayer({
    //                 "id": layerID,
    //                 "type": "fill",
    //                 "source": "countyData",
    //                 'layout': {},
    //                 'paint': {
    //                     "fill-color": "#686868",
    //                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
    //                         1,
    //                         0.5
    //                     ],
    //                     "fill-outline-color": "#0000AA"
    //                 },
    //                 "filter": ["all", [">=", "Income", 60000],
    //                     ["<", "Income", 80000]
    //                 ]
    //             })
    //         }
    //     } else if (80000 <= income && income < 100000) {
    //         layerID = "income5";
    //         if (!map.getLayer(layerID)) {
    //             map.addLayer({
    //                 "id": layerID,
    //                 "type": "fill",
    //                 "source": "countyData",
    //                 'layout': {},
    //                 'paint': {
    //                     "fill-color": "#505050",
    //                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
    //                         1,
    //                         0.5
    //                     ],
    //                     "fill-outline-color": "#0000AA"
    //                 },
    //                 "filter": ["all", [">=", "Income", 80000],
    //                     ["<", "Income", 100000]
    //                 ]
    //             })
    //         }
    //     } else if (100000 <= income) {
    //         layerID = "income6";
    //         if (!map.getLayer(layerID)) {
    //             map.addLayer({
    //                 "id": layerID,
    //                 "type": "fill",
    //                 "source": "countyData",
    //                 'layout': {},
    //                 'paint': {
    //                     "fill-color": "#303030",
    //                     "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
    //                         1,
    //                         0.5
    //                     ],
    //                     "fill-outline-color": "#0000AA"
    //                 },
    //                 "filter": ["all", [">=", "Income", 100000]]
    //             })
    //         }
    //     }
    // })
//*********************************** Load project data *****************************************************
    projectData.features.forEach(function (feature) {
        var primary = feature.properties["Mission Area"];
        var base = "show";
        for (var i = 0; i < Missionarea.length; i++) {
            if (primary == Missionarea[i]) {
                layerID = base + (i + 1);
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
});

//*********************************** District filter *****************************************************

    var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function(e) {
        var value = e.target.value.trim().toLowerCase();
        value = parseInt(value);
        if (isNaN(value)) {
            map.setFilter("show1", ["all", ["==", "Mission Area", Missionarea[0]]]);
            map.setFilter("show2", ["all", ["==", "Mission Area", Missionarea[1]]]);
            map.setFilter("show3", ["all", ["==", "Mission Area", Missionarea[2]]]);
            map.setFilter("show4", ["all", ["==", "Mission Area", Missionarea[3]]]);
            map.setFilter("show5", ["all", ["==", "Mission Area", Missionarea[4]]]);
            map.setFilter("show6", ["all", ["==", "Mission Area", Missionarea[5]]])
        } else {
            map.setFilter("show1", ["all", ["==", "Mission Area", Missionarea[0]],
                ["==", "Legislative District Number", value]
            ]);
            map.setFilter("show2", ["all", ["==", "Mission Area", Missionarea[1]],
                ["==", "Legislative District Number", value]
            ]);
            map.setFilter("show3", ["all", ["==", "Mission Area", Missionarea[2]],
                ["==", "Legislative District Number", value]
            ]);
            map.setFilter("show4", ["all", ["==", "Mission Area", Missionarea[3]],
                ["==", "Legislative District Number", value]
            ]);
            map.setFilter("show5", ["all", ["==", "Mission Area", Missionarea[4]],
                ["==", "Legislative District Number", value]
            ]);
            map.setFilter("show6", ["all", ["==", "Mission Area", Missionarea[5]],
                ["==", "Legislative District Number", value]
            ])
        }

    });

//***********************************clickable legends*****************************************************


var comlist = ["show1", "show2", "show3", "show4", "show5", "show6"];

var edu = document.getElementById("all");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        map.setLayoutProperty(com, 'visibility', 'visible');
    })

})

var edu = document.getElementById("Economic Sufficiency");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show1") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("Educational Support");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show2") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("Environmental Stewardship");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show3") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("Health and Wellness");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show4") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})
var edu = document.getElementById("International Service");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show5") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})
var edu = document.getElementById("Social Justice");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show6") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

