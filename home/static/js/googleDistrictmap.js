//*********************************** Get mapbox API and get data from HTML *****************************************************

// mapboxgl.accessToken = 'pk.eyJ1IjoidW5vY3BpZGV2dGVhbSIsImEiOiJjanJiZTk2cjkwNjZ5M3l0OGNlNWZqYm91In0.vPmkC3MFDrTlBk-ntUFruA';
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00']
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var districtData = JSON.parse(document.getElementById('district-data').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
var filterlist = ["all", "all", "all", "all", "all"] //first is for Mission Areas, second is for Community Types, 3rd for districts
//4th for Campus Partner, 5th for Academic year
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var count = 0;
communityData.features.forEach(function(feature) {
    feature.properties["id"] = count;
    feature.properties["campustest"] = 0 //this variable will be used to filter by campus partners
    feature.properties["yeartest"] = 0 //this variable will be used to filter by academic years
    count++;
})
//*********************************** Load the map *****************************************************

var map = new google.maps.Map(document.getElementById('map_canvas'),{
    // mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: {lng:-95.9345, lat: 41.2565},
    // initial zoom
    zoom: 7,
    // maxZoom: 12,
    fullscreenControl: false,
    mapTypeControl: false
});



//*********************************** Dynamically add the legends *****************************************************


var select = '';
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allmissions"><span style="background-color: #ffffff; border: 1px solid #ffffff"></span><b>All Mission Areas</b></a>' + "<br>";
for (var i = 0; i < Missionarea.length; i++) {
    var color = colorcode[i]
    var mission = Missionarea[i]
    select += `<a href="#"  id="${mission.valueOf()}" value="${mission.valueOf()}"><span style="background-color: ${color}"></span><b>${mission.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);
//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option val=' + "all" + ' selected="selected">' + "All Legislative Districts" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select2 = '';
select2 += '<option val=' + "alltypes" + ' selected="selected">' + 'All Community Types' + '</option>';
for (i = 0; i < CommunityType.length; i++) {
    select2 += '<option val=' + CommunityType[i] + '>' + CommunityType[i] + '</option>';
}
$('#selectCommtype').html(select2);
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var select3 = '';
select3 += '<option val=' + "allcampus" + ' selected="selected">' + 'All Campus Partners' + '</option>';
for (i = 0; i < CampusPartnerlist.length; i++) {
    select3 += '<option val=' + CampusPartnerlist[i] + '>' + CampusPartnerlist[i] + '</option>';
}
$('#selectCampus').html(select3);

//*********************************** Add year filter *****************************************************

var select4 = '';
select4 += '<option val=' + 0 + '>' + 'All Academic Years' + '</option>';
for (i = 0; i < yearlist.length; i++) {
    select4 += '<option val=' + i + '>' + yearlist[i] + '</option>';
}
$('#selectYear').html(select4);
//*********************************** Load the county data here. Should be down here. Otherwise it won't load *****************************************************

// var districtData = JSON.parse(document.getElementById('district-data').textContent);


//*********************************** Format the popup *****************************************************

var formatter = new Intl.NumberFormat('en-US', { //this is to format the current on the pop-up
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});


//*********************************** Load the map *****************************************************
var markers =[];
google.maps.event.addListenerOnce(map, 'idle', function () {
    // changeColor(circle);
    map.data.add('communityData', {
        type: 'geojson',
        data: communityData,
    });
    map.data.add('districtData', {
        type: 'geojson',
        data: districtData,
    });
    //*********************************** Load the county in different household income levels *****************************************************

    districtData.features.forEach(function (feature) {
        var symbol = feature.properties['id'];
        var layerID = 'poi-' + symbol;
        // var density = feature.properties['density']
        if (!map.data.getFeatureById(layerID)) {
            map.data.add({
                "id": layerID,
                "type": "fill",
                "source": "districtData",
                'layout': {},
                'paint': {
                    "fill-color": "#888",
                    "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                        1,
                        0.5
                    ],
                    "fill-outline-color": "#3c341f"
                },
                "filter": ["==", "id", symbol]
            });

            layerIDs.push(layerID);
        }
    })

    map.data.loadGeoJson('../../static/GEOJSON/ID2.geojson')

    map.data.setStyle({
        fillColor: "#fee8c8",
        fillOpacity: 0.5,
        strokeWeight: 0.2
    })





// circle added to the map
    var circle = {
        path: google.maps.SymbolPath.CIRCLE,
        fillOpacity: 1,
        strokeOpacity: 0.9,
        scale: 8,
        strokeColor: 'white',
        strokeWeight: 1.5
    };
    console.log(communityData.features)
    // contents of the infowindow
    var comm_name = communityData.features
    var miss_name = communityData.features
    var partner_name = communityData.features
    var district_number = communityData.features
    var project_number = communityData.features
    var campus_partner = communityData.features
    var academic_year = communityData.features
    var website = communityData.features
    var county = communityData.features
    // console.log(communityData.features.properties)
    // var markers =[];
    for (i=0; i<communityData.features.length; i++) {
        var category = communityData.features[i].properties["Legislative District Number"]
        var academic = communityData.features[i].properties["Academic Year"]
        var engagementType = communityData.features[i].properties["Engagement Type"]
        var commType = communityData.features[i].properties["CommunityType"]
        var missionArea = communityData.features[i].properties["Mission Area"]
        var campusPartner = communityData.features[i].properties["Campus Partner"]
        var marker = new google.maps.Marker({
            position: {
                lat: parseFloat(communityData.features[i].geometry.coordinates[1]),
                lng: parseFloat(communityData.features[i].geometry.coordinates[0])
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: missionColor(missionArea),
            category: category,
            year: academic,
            mission: missionArea,
            commType: commType,
            campusPartner: campusPartner
        });

        function missionColor(missionArea) {

            if (missionArea=="Economic Sufficiency"){
                return circle.fillColor= colorcode[0]
            }
            else if (missionArea=='Educational Support'){
                // communityData.features[i].properties["Mission Area"]
                return circle.fillColor=colorcode[1]
            }
            else if (missionArea=="Environmental Stewardship"){
                return circle.fillColor=colorcode[2]
            }
            else if (miss_name[i].properties["Mission Area"]=="Health and Wellness"){
                return circle.fillColor=colorcode[3]
            }
            else if (missionArea=="International Service"){
                return circle.fillColor=colorcode[4]
            }
            else if (missionArea=="Social Justice"){
                return circle.fillColor=colorcode[5]
            }
        }
              attachMessage(marker, partner_name[i].properties['CommunityPartner'],district_number[i].properties['Legislative District Number'],
            project_number[i].properties['Number of projects'],county[i].properties['County'],
            miss_name[i].properties["Mission Area"], comm_name[i].properties["CommunityType"],
            campus_partner[i].properties["Campus Partner"],
            academic_year[i].properties["Academic Year"],
            website[i].properties["Website"]);
        markers.push(marker)
    }
    //adding the marker cluster functionality
    markerCluster = new MarkerClusterer(map, markers,mcOptions);

})

var mcOptions = {
    minimumClusterSize: 5, //minimum number of points before which it should be clustered
    styles: [{
        height: 53,
        url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
        width: 53
    },
        {
            height: 56,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 56
        },
        {
            height: 60,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 60
        },
        {
            height: 80,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 80
        },
        {
            height: 100,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 100
        }]
};


// function to call the infowindow on clicking markers
function attachMessage(marker, partner_name,district_number,project_number,county,miss_name, comm_name, campus_partner,academic_year,website) {
    var infowindow = new google.maps.InfoWindow({
        content: '<tr><td><span style="font-weight:bold">Community Partner:</span>&nbsp;&nbsp; </td><td>' + partner_name + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Legislative District Number: </span>&nbsp; </td><td>' + district_number + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Number of Projects: </span>&nbsp; </td><td>' + project_number + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">County: </span>&nbsp; </td><td>' + county + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Area: </span>&nbsp; </td><td>' + miss_name + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Type:</span>&nbsp;&nbsp; </td><td>' + comm_name + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campus_partner + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp; </td><td>' + academic_year + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Website: </span>&nbsp; </td><td>' +  website + '</td></tr>'
    });
    //listner to check for on click event
    marker.addListener('click', function () {
        infowindow.open(marker.get('map'), marker);
        //time out after which the info window will close
        setTimeout(function () {
            infowindow.close();
        }, 5000);
        // infowindow.close();
        google.maps.event.addListener(map, "click", function (event) {
            infowindow.close();
        })
    })
}

//****************************filters from sidebar***************************************
//district change in filters
markerDistrict = function(category) {

    for (i=0; i < markers.length; i++) {
        if (category == 'All Legislative Districts') {
            markers[i].setVisible(true);
            markerCluster.addMarker(markers[i]);
        } else {
            if (markers[i].category == category) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);
            }
        }

    }
};
//******************************************************************************************************************************

//Filter for the academic year
filterYear = function(year) {

    for (i=0; i < markers.length; i++) {
        if (year == 'All Academic Years') {
            markers[i].setVisible(true);
            markerCluster.addMarker(markers[i]);
        } else {
            if (markers[i].year == year) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);
            }
        }
    }
    markerCluster.redraw();
};


//Filter for the Mission Areas
filterMission = function(mission) {

    for (i=0; i < markers.length; i++) {
        if (mission == 'All Mission Years') {
            markers[i].setVisible(true);
            markerCluster.addMarker(markers[i]);
        } else {
            if (markers[i].mission == mission) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);
            }
        }
    }
    markerCluster.redraw();
};


//Filter for the Cummunity Type
filterCommType = function(commType) {

    for (i=0; i < markers.length; i++) {
        if (commType == 'All Community Types') {
            markers[i].setVisible(true);
            markerCluster.addMarker(markers[i]);
        } else {
            if (markers[i].commType == commType) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);
            }
        }
    }
    markerCluster.redraw();
};

//Filter for the Campus Partner
filterCampusPartner = function(campusPartner) {

    for (i=0; i < markers.length; i++) {
        if (campusPartner == 'All Community Partners') {
            markers[i].setVisible(true);
            markerCluster.addMarker(markers[i]);
        } else {
            if (markers[i].campusPartner == campusPartner) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);
            }
        }
    }
    markerCluster.redraw();
};





//***********************************filter by clickable legends*****************************************************


var edu = document.getElementById("all"); //get the total number of dots
edu.addEventListener("click", function(e) {

    filterlist[0] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
})

$('#legend a').click(function(e) { //filter dots by mission areas and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    var i = Missionarea.indexOf(clickedValue);
    if (i > -1) {
        filterlist[0] = clickedValue;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    }
});

$("#reset").click(function() {
    filterlist[0] = "all"
    filterlist[1] = "all"
    filterlist[2] = "all"
    filterlist[3] = "all"
    filterlist[4] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    $('#selectCommtype option').prop('selected', function() {
        return this.defaultSelected;
    });
    $('#selectDistrict option').prop('selected', function() {
        return this.defaultSelected;
    });
    $('#selectCampus option').prop('selected', function() {
        return this.defaultSelected;
    });
    $('#selectYear option').prop('selected', function() {
        return this.defaultSelected;
    });
    layerIDs.forEach(function(layerID) {
        map.setLayoutProperty(layerID, 'visibility', 'visible');
    })
});

function calculation(a, b, c, d, e) {
    var totalnumber = ''
    var number = 0

    if (a == "all") {
        if (b == "all") {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        map.setFilter("commMap", null)
                        totalnumber += communityData.features.length
                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "yeartest", 1])
                        totalnumber += number
                    }
                } else { //else for data[3] if
                    if (e = "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "campustest", 1])
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1) {
                                if (feature.properties['yeartest'] == 1) {
                                    number += 1
                                }
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ])
                        totalnumber += number
                    }
                }
            } else { //else for data[2] if
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "Legislative District Number", c])
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "Legislative District Number", c],
                            ["==", "yeartest", 1]
                        ])
                        totalnumber += number
                    }
                } else {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "Legislative District Number", c],
                            ["==", "campustest", 1]
                        ])
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "Legislative District Number", c],
                            ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ])
                        totalnumber += number
                    }
                }
            }
        } else { //else if for data[1]
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "CommunityType", b])
                        totalnumber += number
                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "CommunityType", b], ["==", "yeartest", 1])
                        totalnumber += number
                    }
                } else { //else for data[3] if
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "campustest", 1]
                        ])
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ])
                        totalnumber += number
                    }
                }
            } else { //else for data[2] if
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c]
                        ])
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c],
                            ["==", "yeartest", 1]
                        ])
                        totalnumber += number

                    }
                } else {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c],
                            ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number

                    }
                }
            }
        }
    } else { // else for data[0]
        if (b == "all") {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a]]);
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number

                    }
                } else { //else for data[3] if
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "yeartest", 1],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number
                    }
                }
            } else { //else for data[2] if
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "Legislative District Number", c]
                        ]);
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "Legislative District Number", c],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number

                    }
                } else {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "Legislative District Number", c],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "Legislative District Number", c],
                            ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number

                    }
                }
            }
        } else {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b]
                        ])
                        totalnumber += number

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "yeartest", 1]
                        ])
                        totalnumber += number

                    }
                } else { //else for data[3] if
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number;

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number;

                    }
                }
            } else { //else for data[2] if
                if (d == "all") {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c]
                        ]);
                        totalnumber += number;

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number;

                    }
                } else {
                    if (e == "all") {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number;

                    } else {
                        communityData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter(showlist[i], ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c],
                            ["==", "campustest", 1],
                            ["==", "yeartest", 1]
                        ]);
                        totalnumber += number;
                    }
                }
            }
        }
    }
    $('#totalnumber').html(totalnumber);
}