//*********************************** Get data from HTML *****************************************************

var colorcode = ['#27ffcb', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#29234b']
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var districtData = JSON.parse(document.getElementById('district-data').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CollegeNamelist = JSON.parse(document.getElementById('collegename-list').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
var filterlist = ["all", "all", "all", "all", "all","all"] //first is for Mission Areas, second is for Community Types, 3rd for districts
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
    zoom: 4,
    minZoom: 3,
    // maxZoom: 13,
    fullscreenControl: false,
    mapTypeControl: false,
    styles: [
        {
            "featureType": "landscape",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi.business",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.local",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "transit",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        }
    ]
});



//*********************************** Dynamically add the legends *****************************************************


var select = '';
select += '<a href="#" ' + 'id=' + '"allmiss" ' + 'value=' + '"allmissions"><span style="background-color: #ffffff; border: 1px solid #ffffff"></span><b>All Mission Areas</b></a>' + "<br>";
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
    select1 += '<option val=' + i + '>' + "Legislative District " + i + '</option>';
}
$('#selectDistrict').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select2 = '';
select2 += '<option val=' + "alltypes" + ' selected="selected">' + 'All Community Partner Types' + '</option>';
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

//*********************************** Add the community type drop-down *****************************************************

var select5 = '';
select5 += '<option val=' + "allcollege" + ' selected="selected">' + 'All Colleges' + '</option>';
for (i = 0; i < CollegeNamelist.length; i++) {
    select5 += '<option val=' + CollegeNamelist[i] + '>' + CollegeNamelist[i] + '</option>';
}
$('#selectCollege').html(select5);


// var districtData = JSON.parse(document.getElementById('district-data').textContent);


//*********************************** Format the popup *****************************************************

var formatter = new Intl.NumberFormat('en-US', { //this is to format the current on the pop-up
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});

//*****************************************District layer*************************************************

// dist_data = map.data.loadGeoJson('../../static/GEOJSON/ID2.geojson')
//
//     //Overlay for districts in Nebraska
//     map.data.setStyle({
//         fillColor: "#fee8c8",
//         fillOpacity: 0.4,
//         strokeWeight: 0.2
//     })



//*********************************** Load the map *****************************************************
var markers =[];
var oms = new OverlappingMarkerSpiderfier(map, {keepSpiderfied : true, markersWontMove : true, legWeight: 0.5});

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




// circle added to the map
    var circle = {
        path: google.maps.SymbolPath.CIRCLE,
        fillOpacity: 0.6,
        strokeOpacity: 1,
        scale: 8,
        strokeColor: 'white',
        strokeWeight: 1.5
    };
    // contents of the infowindow
    var comm_name = communityData.features
    var miss_name = communityData.features
    var partner_name = communityData.features
    var district_number = communityData.features
    var project_number = communityData.features
    var campus_partner = communityData.features
    var academic_year = communityData.features
    var website = communityData.features
    var city = communityData.features
    // var markers =[];
    for (i=0; i<communityData.features.length; i++) {
        var category = communityData.features[i].properties["Legislative District Number"]
        var academic = communityData.features[i].properties["Academic Year"]
        var engagementType = communityData.features[i].properties["Engagement Type"]
        var commType = communityData.features[i].properties["CommunityType"]
        var missionArea = communityData.features[i].properties["Mission Area"]
        var campusPartner = communityData.features[i].properties["Campus Partner"]
        var yearTest = communityData.features[i].properties["yeartest"]
        var campusTest = communityData.features[i].properties["campustest"]
        var commPartnerName = communityData.features[i].properties["CommunityPartner"]
        var marker = new google.maps.Marker({
            position: {
                lat: parseFloat(communityData.features[i].geometry.coordinates[1]+ (Math.random() -.5) / 50000),
                lng: parseFloat(communityData.features[i].geometry.coordinates[0]+ (Math.random() -.5) / 50000)
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: missionColor(missionArea),
            category: category,
            year: academic,
            mission: missionArea,
            commType: commType,
            campusPartner: campusPartner,
            yearTest: yearTest,
            campusTest: campusTest,
            commPartnerName: commPartnerName
        });

        oms.addMarker(marker);
        function missionColor(mission) {

            if (mission=="Economic Sufficiency"){
                return circle.fillColor= colorcode[0]
            }
            else if (mission=='Educational Support'){
                // communityData.features[i].properties["Mission Area"]
                return circle.fillColor=colorcode[1]
            }
            else if (mission=="Environmental Stewardship"){
                return circle.fillColor=colorcode[2]
            }
            else if (mission=="Health and Wellness"){
                return circle.fillColor=colorcode[3]
            }
            else if (mission=="International Service"){
                return circle.fillColor=colorcode[4]
            }
            else if (mission=="Social Justice"){
                return circle.fillColor=colorcode[5]
            }
        }
        attachMessage(marker, partner_name[i].properties['CommunityPartner'],district_number[i].properties['Legislative District Number'],
            project_number[i].properties['Number of projects'],city[i].properties['City'],
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
    maxZoom: 15,
    minimumClusterSize: 10, //minimum number of points before which it should be clustered
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


var openedInfoWindow = null;

// function to call the infowindow on clicking markers
function attachMessage(marker, partner_name,district_number,project_number,city,miss_name, comm_name, campus_partner,academic_year,website) {
    var infowindow = new google.maps.InfoWindow();
    google.maps.event.addListener(marker, 'click', function () {
        if (openedInfoWindow != null) openedInfoWindow.close();  // <-- changed this
        infowindow.setContent('<tr><td style="margin-top: 5%"><span style="font-weight:bold">Community Partner:</span>&nbsp;&nbsp; </td><td>' + partner_name + '</td></tr><br />' +
            // '<tr><td><span style="font-weight:bold">Legislative District Number: </span>&nbsp; </td><td>' + district_number + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Number of Projects: </span>&nbsp; </td><td>' + project_number + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">City: </span>&nbsp; </td><td>' + city + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Areas: </span>&nbsp; </td><td>' + miss_name + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partner Type:</span>&nbsp;&nbsp; </td><td>' + comm_name + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campus_partner.toString().split(",").join(" , ") + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp; </td><td>' + academic_year + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Website: </span>&nbsp;<a id="websitelink" href="' + website + '" target="_blank">' + website + '</a></td></tr><br /><br>')
        infowindow.open(map, marker);
        // map.setZoom(16);
        map.panTo(this.getPosition());
        // added next 4 lines
        openedInfoWindow = infowindow;
        google.maps.event.addListener(infowindow, 'closeclick', function () {
            openedInfoWindow = null;
        });
    });
}

// To prevent Info window opening on the first click on spiderfier
oms.addListener('spiderfy', function(markers) {
  infowindow.close();
})

// *******************************filter by clickable legends*****************************************************


var edu = document.getElementById("allmiss"); //get the total number of dots
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


//*********************************** Campus Partner filter *****************************************************

var selectCampus = document.getElementById('selectCampus'); //get the element on HTML
selectCampus.addEventListener("change", function(e) {
    var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
    if (!CampusPartnerlist.includes(value)) { // in the case of all Campus partners
        filterlist[3] = "all";
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    } else { //in case a campus partner is chosen
        communityData.features.forEach(function(feature) { //iterate through the dataset
            var campuspartner = feature.properties["Campus Partner"] //get the campus partner
            if (campuspartner.includes(value)) { // if the partner has that campus partner
                feature.properties["campustest"] = 1 // assign this value 1
            } else {
                feature.properties["campustest"] = 0 //if not, assign this value 0
            }
            })

               for (i=0;i<markers.length; i++){
                    if(communityData.features[i].properties['campustest']==1){
                        markers[i].campusTest=1;
                    }
                    else
                        markers[i].campusTest=0;
            filterlist[3] = 1;
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
}
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
        filterlist[4] = "all";
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
    } else {
        communityData.features.forEach(function (feature) {
            var year = feature.properties["Academic Year"];
                if (year) {
                    for (var j = 0; j < year.length; j++) {
                        if (year[j] == value) {
                            feature.properties["yeartest"] = 1;

                        } else {
                            feature.properties["yeartest"] = 0;

                        }
                    }
                } else {
                    feature.properties["yeartest"] = 0;
                }
                 });
         for (i=0;i<markers.length; i++){
                    if(communityData.features[i].properties['yeartest']==1){
                        markers[i].yearTest=1;
                    }
                    else
                        markers[i].yearTest=0;

            filterlist[4] = 1;
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
}

    }
})
   //*********************************** District filter *****************************************************
var states = new Array();
var selectDistrict = document.getElementById('selectDistrict');
selectDistrict.addEventListener("change", function (e) {
    var value1 = e.target.value.trim()
    var value=value1.split("Legislative District")[1]
    value = parseInt(value)
    if (isNaN(value)) {
        for (var k=0; k<states.length; k++) {
            states[k].setMap(null);
        }
        // get the number of markers that fit the requirement and show on the HTML
        filterlist[2] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
    } else {
        var coords = []
        for (var k=0; k<states.length; k++) {
            states[k].setMap(null);
        }
        for (i = 0; i < districtData.features.length; i++) {
            if (value == districtData.features[i].id) {
                for (j = 0; j < districtData.features[i].geometry['coordinates'][0].length; j++) {
                    coords.push({
                        lat: parseFloat(districtData.features[i].geometry['coordinates'][0][j][1]),
                        lng: parseFloat(districtData.features[i].geometry['coordinates'][0][j][0])
                    });
                }
            }
        }
        var state = new google.maps.Polygon({
            paths: coords,
            strokeColor: '#fe911d',
            strokeOpacity: 0.8,
            strokeWeight: 1,
            fillColor: '#fe911d',
            fillOpacity: 0.25,
        });

        states.push(state)
        state.setMap(map)

        filterlist[2] = value
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
    }
})


    //*********************************** Search function *****************************************************
    var valueFilter = document.getElementById("valueFilter");

    //Press the listening button
    valueFilter.addEventListener("keydown", function (e) {
        if (e.keyCode == 8) {
            for (var i = 0; i < markers.length; i++) {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);
            }
            markerCluster.redraw();
        }
    });

    // the listening button off
    valueFilter.addEventListener("keyup", function (e) {
        //get the input value
        var value = e.target.value.trim().toLowerCase();

        if (value == "") {
            for (var i = 0; i < markers.length; i++) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            }
            markerCluster.redraw();
        } else {

            for (var i = 0; i < markers.length; i++) {
                cpname = markers[i].commPartnerName.toLowerCase();
                if (cpname.includes(value)) {
                    markers[i].setVisible(true);
                    markerCluster.addMarker(markers[i]);
                    // marker.setCenter(markers[i].getPosition());
                } else {
                    markers[i].setVisible(false);
                    markerCluster.removeMarker(markers[i]);

                }
            }
            markerCluster.redraw();
        }
    })


    $("#reset").click(function () {
        filterlist[0] = "all";
        filterlist[1] = "all";
        filterlist[2] = "all";
        filterlist[3] = "all";
        filterlist[4] = "all";
        filterlist[5] = "all";
        for (var k=0; k<states.length; k++) {
            states[k].setMap(null);
        }
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
        $('#selectCommtype option').prop('selected', function () {
            return this.defaultSelected;
        });
        $('#selectDistrict option').prop('selected', function () {
            return this.defaultSelected;
        });
        $('#selectCampus option').prop('selected', function () {
            return this.defaultSelected;
        });
        $('#selectYear option').prop('selected', function () {
            return this.defaultSelected;
        });
        $('#selectMisstype option').prop('selected', function () {
            return this.defaultSelected;
        });
    });

//To vary the total number of projects based on the filter selected
    function calculation(a, b, c, d, e) {
        var totalnumber = '';
        var number = 0;

        if (a == "all") {
            if (b == "all") {
                if (c == "all") {
                    if (d == "all") {
                        if (e == "all") {
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                }
                            markerCluster.redraw();
                            totalnumber += communityData.features.length
                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['yeartest'] == 1) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].yearTest !== 1) {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number
                        }
                    } else { //else for data[3] if
                        if (e == "all") {
                            markerCluster.clearMarkers();
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        } else {
                            markerCluster.clearMarkers();
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1) {
                                    if (feature.properties['yeartest'] == 1) {
                                        number += 1
                                    }
                                }
                            })

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].yearTest == 1 && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);

                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number
                        }
                    }
                } else { //else for data[2] if
                    if (d == "all") {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].category == c) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].category == c && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number
                        }
                    } else {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].category == c && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].category == c && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number
                        }
                    }
                }
            } else { //else if for data[1]
                if (c == "all") {
                    if (d == "all") {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number
                        }
                    } else { //else for data[3] if
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                            }
                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number
                        }
                    }
                } else { //else for data[2] if
                    if (d == "all") {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].category == c) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].category == c && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number

                        }
                    } else {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].category == c && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].commType == b && markers[i].category == c && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

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
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        }
                    } else { //else for data[3] if
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number
                        }
                    }
                } else { //else for data[2] if
                    if (d == "all") {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].category == c) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].category == c && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        }
                    } else {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].category == c && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].category == c && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        }
                    }
                }
            } else {
                if (c == "all") {
                    if (d == "all") {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number

                        }
                    } else { //else for data[3] if
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number;

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number;

                        }
                    }
                } else { //else for data[2] if
                    if (d == "all") {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].category == c) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number;

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].category == c && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number;

                        }
                    } else {
                        if (e == "all") {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].category == c && markers[i].campusTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }
                            totalnumber += number;

                        } else {
                            communityData.features.forEach(function (feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == a && markers[i].commType == b && markers[i].category == c && markers[i].campusTest == 1 && markers[i].yearTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                                markerCluster.redraw();
                            }

                            totalnumber += number;
                        }
                    }
                }
            }
        }
        $('#totalnumber').html(totalnumber);
    }