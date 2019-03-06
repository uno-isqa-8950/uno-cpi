// mapboxgl.accessToken = 'pk.eyJ1IjoidmJoYXRob3NtYXQiLCJhIjoiY2pyNGc5MzNzMDNvZTQ1bzIxcmJ5ejJhayJ9.lMH6o8Nk36qm3lG3M0apdQ';
var projectData = JSON.parse(document.getElementById('project-data').textContent); //load the variable from views.py. See the line from html first
var districtData = JSON.parse(document.getElementById('district').textContent); //load the variable from views.py. See the line from html first
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00']
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityPartnerlist = JSON.parse(document.getElementById('communitypartner-list').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var Engagement = JSON.parse(document.getElementById('engagementType').textContent);


var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
var filterlist = ["all", "all", "all", "all", "all"]
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var count = 0;
projectData.features.forEach(function(feature) {
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
    zoom: 9,
    fullscreenControl: false,
});

//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option val=' + "all" + '>' + "All Legislative Districts" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);

// *********************************** Dynamically add the legends *****************************************************
var select = '';
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allmissions"><span style="background-color: transparent; border: 1px solid black"></span><b>All Engagement Types</b></a>' + "<br>";
for (var i = 0; i < Engagement.length; i++) {
    var color = colorcode[i]
    var engagement = Engagement[i]
    select += `<a href="#"  id="${engagement.valueOf()}" value="${engagement.valueOf()}"><span style="background-color: ${color}"></span><b>${engagement.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);



// *********************************** Dynamically add the legends *****************************************************
var select6 = '';
select6 += '<option val=' + "alltypes" + ' selected="selected">' + 'All Mission Areas' + '</option>';
for (i = 0; i < Missionarea.length; i++) {
    select6 += '<option val=' + Missionarea[i] + '>' + Missionarea[i] + '</option>';
}
$('#selectMisstype').html(select6);

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


//*********************************** Add Community Partner *****************************************************

var select5 = '';
select5 += '<option val=' + 0 + '>' + 'All Community Partners' + '</option>';
for (i = 0; i < communityPartnerlist.length; i++) {
    select5 += '<option val=' + i + '>' + communityPartnerlist[i] + '</option>';
}
$('#selectCommunity').html(select5);





//*********************************** Load the map *****************************************************
districtData.features.forEach(function(feature){
    var stand = feature.properties["id"];
    var number = 0;
    projectData.features.forEach(function(e){
        if (e.properties["Legislative District Number"] == stand){
            number += 1;
        }
    });
    feature.properties["density"] = number
})
// function getColor(d) {
//     return d > 100 ? '#8c2d04' :
//         d > 50  ? '#cc4c02' :
//             d > 30  ? '#ec7014' :
//                 d > 20  ? '#fe9929' :
//                     d > 10   ? '#fec44f' :
//                         d > 5   ? '#fee391' :
//                             d > 1   ? '#fff7bc' :
//                                 '#ffffe5';
// }

google.maps.event.addListenerOnce(map, 'idle', function () {
    map.data.add('projectData', {
        type: 'geojson',
        data: projectData,
    });
    map.data.add('districtData', {
        type: 'geojson',
        data: districtData,
    });
    map.data.loadGeoJson('../../static/GEOJSON/ID2.geojson')

    map.data.setStyle({
        fillColor: "#fee8c8",
        fillOpacity: 0.5,
        strokeWeight: 0.2
    })

// circle added to the map
    var circle = {
        path: google.maps.SymbolPath.CIRCLE,
        // fillColor: 'blue',
        fillOpacity: 1,
        strokeOpacity: 0.9,
        scale: 8,
        strokeColor: 'white',
        strokeWeight: 1.5
    };

    // contents of the infowindow
    // var contentString =
    var proj_name = projectData.features
    var miss_name = projectData.features
    var comm_partner = projectData.features
    var comm_partner_type = projectData.features
    var campus_partner = projectData.features
    var academic_year = projectData.features
    var eng_type = projectData.features

    console.log(projectData.features)
    var markers =[];
    for (i=0; i<projectData.features.length; i++) {
        var marker = new google.maps.Marker({
            position: {
                lat: parseFloat(projectData.features[i].geometry.coordinates[1]),
                lng: parseFloat(projectData.features[i].geometry.coordinates[0])
            },
            map: map,
            icon: circle, // set the icon here
        });


        var x=projectData.features[i].properties["Engagement Type"]

        if (x=="Community-Based Learning"){
            console.log(projectData.features[i].properties["Engagement Type"])
            circle.fillColor= colorcode[0]
            attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
                comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
                campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic year'],
                eng_type[i].properties['Engagement Type'] );

        }
        else if (projectData.features[i].properties["Engagement Type"]=="Knowledge/Info Sharing"){
            console.log(projectData.features[i].properties["Engagement Type"])
            circle.fillColor= colorcode[1]
            attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
                comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
                campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic year'],
                eng_type[i].properties['Engagement Type'] );

        }
        else if (projectData.features[i].properties["Engagement Type"]=="Providing Access") {
            console.log(projectData.features[i].properties["Engagement Type"])
            circle.fillColor = colorcode[2]
            attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
                comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
                campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic year'],
                eng_type[i].properties['Engagement Type'] );
        }
        else if (projectData.features[i].properties["Engagement Type"]=="Service Learning") {
            console.log(projectData.features[i].properties["Engagement Type"])
            circle.fillColor = colorcode[3]
            attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
                comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
                campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic year'],
                eng_type[i].properties['Engagement Type'] );
        }
        else if (projectData.features[i].properties["Engagement Type"]=="Volunteering") {
            console.log(projectData.features[i].properties["Engagement Type"])
            circle.fillColor = colorcode[4]
            attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
                comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
                campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic year'],
                eng_type[i].properties['Engagement Type'] );
        }
        markers.push(marker)

    }
    //adding the marker cluster functionality
    var markerCluster = new MarkerClusterer(map, markers,mcOptions);
    //To have different colors while clustering uncomment below line
    // {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

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
            height: 66,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 66
        },
        {
            height: 78,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 78
        },
        {
            height: 90,
            url: "https://googlemaps.github.io/js-marker-clusterer/images/m2.png",
            width: 90
        }]
};



// function to call the infowindow on clicking markers
function attachMessage(marker, projectName, missionArea,comm_partner, comm_partner_type, campus_partner,academic_year, eng_type) {
    var infowindow = new google.maps.InfoWindow({
        content: '<tr><td><span style="font-weight:bold">Project Name:</span>&nbsp;&nbsp; </td><td>' + projectName + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Area: </span>&nbsp </td><td>' + missionArea + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partners: </span>&nbsp </td><td>' + comm_partner + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partner Type: </span>&nbsp </td><td>' + comm_partner_type + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp </td><td>' + campus_partner + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp </td><td>' + academic_year + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Engagement Type: </span>&nbsp </td><td>' + eng_type + '</td></tr>'
    });
    //listner to check for on click event
    marker.addListener('click', function() {
        // infowindow.open(marker.get('map'), marker);
         setTimeout(function () {
            infowindow.close();
        }, 5000);

        infowindow.open(map, marker);

        google.maps.event.addListener(map, "click", function (event) {
            infowindow.close();
        })

    })
}

            var selectDistrict = document.getElementById('selectDistrict');
            selectDistrict.addEventListener("change", function(e) {
                var value = e.target.value.trim().toLowerCase();
                // console.log(value)
                var len = districtData.features[0].geometry['coordinates'][0][100]
                // console.log(len)
                for (j = 0; j < districtData.features.length; j++)
                    if (districtData.features[j].id == value)
                        var x= districtData.features[j].geometry['coordinates'][0][100]
                        map.setCenter({lat:x[1], lng:x[0]});
                        map.setZoom(10);

            })

//******************************************************************************************************************************

//Filter experimentation

    //*********************************** Campus Partner filter *****************************************************

var selectCampus = document.getElementById('selectCampus'); //get the element on HTML
selectCampus.addEventListener("change", function(e) {
    var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
    if (!CampusPartnerlist.includes(value)) { // in the case of all Campus partners
        filterlist[3] = "all";
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    } else { //in case a campus partner is chosen
        projectData.features.forEach(function(feature) { //iterate through the dataset
            console.log(projectData.features)
            var campuspartner = feature.properties["Campus Partner"] //get the campus partner
            if (campuspartner.includes(value)) { // if the partner has that campus partner
                feature.properties["campustest"] = 1 // assign this value 1
            } else {
                feature.properties["campustest"] = 0 //if not, assign this value 0
            }
        })
        map.data.add('projectData').setData(projectData); // update the dataset
        map.removeLayer("commMap");
        map.addLayer({
            "id": "commMap",
            "type": "circle",
            "source": "projectData",
            'layout': {},
            'paint': {
                "circle-radius": 8,
                "circle-opacity": 1,
                "circle-color": {
                    "property": "Engagement Type",
                    "type": 'categorical',
                    "stops": [
                        [Engagement[0], colorcode[0]],
                        [Engagement[1], colorcode[1]],
                        [Engagement[2], colorcode[2]],
                        [Engagement[3], colorcode[3]],
                        [Engagement[4], colorcode[4]],
                        [Engagement[5], colorcode[5]],
                    ]
                }
            }
        });
        filterlist[3] = 1;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    }
})
        //*********************************** Community Type filter *****************************************************

    var selectCommtype = document.getElementById('selectCommtype');
    selectCommtype.addEventListener("change", function(e) {
        var value = e.target.value.trim();
        if (!CommunityType.includes(value)) {
            //get the number of markers and show it on the HTML
            filterlist[1] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        } else {
            for (var i = 0; i <= CommunityType.length; i++) {
                if (value == CommunityType[i]) {
                    filterlist[1] = value
                    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
                }
            }
        }
    })

    //*********************************** Academic Year filter *****************************************************

    var selectYear = document.getElementById('selectYear'); //same concept as campus partner. Just for years
    selectYear.addEventListener("change", function(e) {
        var value = e.target.value.trim();
        if (!yearlist.includes(value)) {
            filterlist[4] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        } else {
            projectData.features.forEach(function(feature) {
                var year = feature.properties["Academic year"]
                console.log(year)
                if (year) {
                    for (var j = 0; j < year.length; j++){
                        if (year[j] == value){
                            feature.properties["yeartest"] = 1
                        } else {
                            feature.properties["yeartest"] = 0
                        }
                    }
                } else {
                    feature.properties["yeartest"] = 0
                }
            })
            map.data.add('projectData').setData(projectData); // update the dataset
            map.data.setStyle("commMap",{visible: false});
            map.addLayer({
                "id": "commMap",
                "type": "circle",
                "source": "projectData",
                'layout': {},
                'paint': {
                    "circle-radius": 8,
                    "circle-opacity": 1,
                    "circle-color": {
                        "property": "Mission Area",
                        "type": 'categorical',
                        "stops": [
                            [Missionarea[0], colorcode[0]],
                            [Missionarea[1], colorcode[1]],
                            [Missionarea[2], colorcode[2]],
                            [Missionarea[3], colorcode[3]],
                            [Missionarea[4], colorcode[4]],
                            [Missionarea[5], colorcode[5]],
                        ]
                    }
                }
            });
            filterlist[4] = 1
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        }
    })

    //*********************************** District filter *****************************************************

    var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function(e) {
        var value = e.target.value.trim().toLowerCase();
        value = parseInt(value)
        if (isNaN(value)) {
            // get the number of markers that fit the requirement and show on the HTML
            filterlist[2] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        } else {
            filterlist[2] = value
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        }
        var value = e.target.value.trim().toLowerCase();
        layerIDs.forEach(function(layerID) {
            console.log("dis:" + layerID.length);

            map.setLayoutProperty(layerID, 'visibility',
                (layerID.indexOf(value) == 4) && (layerID.length == (value.length + 4)) ? 'visible' : 'none');
        })
    })


//***********************************filter by clickable legends*****************************************************


var edu = document.getElementById("all"); //get the total number of dots
edu.addEventListener("click", function(e) {

    filterlist[0] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4],filterlist[5],filterlist[6])
})

$('#legend a').click(function(e) { //filter dots by mission areas and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    var i = Engagement.indexOf(clickedValue);
    if (i > -1) {
        filterlist[0] = clickedValue;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4],filterlist[5],filterlist[6]);
    }
});

$("#reset").click(function() {
    filterlist[0] = "all"
    filterlist[1] = "all"
    filterlist[2] = "all"
    filterlist[3] = "all"
    filterlist[4] = "all"
    filterlist[5] = "all"
    filterlist[6] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4],filterlist[5],filterlist[6]);
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
     $('#selectMisstype option').prop('selected', function() {
        return this.defaultSelected;
    });
      $('#selectDistrict option').prop('selected', function() {
        return this.defaultSelected;
    });
    layerIDs.forEach(function(layerID) {
        map.setProperty(layerID, 'visibility', 'visible');
    })
});

//To vary the total number of projects based on the filter selected
function calculation(a, b, c, d, e) {
    var totalnumber = ''
    var number = 0

    if (a == "all") {
        if (b == "all") {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        map.setFilter("commMap", null)
                        totalnumber += projectData.features.length
                    } else {
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['yeartest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "yeartest", 1])
                        totalnumber += number
                    }
                } else { //else for data[3] if
                    if (e = "all") {
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "campustest", 1])
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "Legislative District Number", c])
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "Legislative District Number", c],
                            ["==", "campustest", 1]
                        ])
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "CommunityType", b])
                        totalnumber += number
                    } else {
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["==", "CommunityType", b], ["==", "yeartest", 1])
                        totalnumber += number
                    }
                } else { //else for data[3] if
                    if (e == "all") {
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        })
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "campustest", 1]
                        ])
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "CommunityType", b],
                            ["==", "Legislative District Number", c]
                        ])
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a]]);
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "campustest", 1]
                        ]);
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "Legislative District Number", c]
                        ]);
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
                            if (feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                number += 1
                            }
                        });
                        map.setFilter("commMap", ["all", ["==", "Mission Area", a],
                            ["==", "CommunityType", b]
                        ])
                        totalnumber += number

                    } else {
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
                        projectData.features.forEach(function(feature) {
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
