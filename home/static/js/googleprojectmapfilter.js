// mapboxgl.accessToken = 'pk.eyJ1IjoidmJoYXRob3NtYXQiLCJhIjoiY2pyNGc5MzNzMDNvZTQ1bzIxcmJ5ejJhayJ9.lMH6o8Nk36qm3lG3M0apdQ';
var projectData = JSON.parse(document.getElementById('project-data').textContent); //load the variable from views.py. See the line from html first
var districtData = JSON.parse(document.getElementById('district').textContent); //load the variable from views.py. See the line from html first
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00']
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CollegeNamelist = JSON.parse(document.getElementById('collegename-list').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityPartnerlist = JSON.parse(document.getElementById('communitypartner-list').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var Engagement = JSON.parse(document.getElementById('engagementType').textContent);


var filterlist = ["all", "all", "all", "all", "all","all","all","all"]
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var count = 0;
projectData.features.forEach(function(feature) {
    feature.properties["id"] = count;
    feature.properties["campustest"] = 0 //this variable will be used to filter by campus partners
    feature.properties["yeartest"] = 0 //this variable will be used to filter by academic years
    feature.properties["communitytest"] = 0
    count++;
})

//*********************************** Load the map *****************************************************
var map = new google.maps.Map(document.getElementById('map_canvas'),{
    // mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: {lng:-95.9345, lat: 41.2565},
    // initial zoom
    zoom: 5,
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


//*********************************** Add the districts *****************************************************

var select2 = '';
select2 += '<option val=' + "all" + ' selected="selected">' + "All Legislative Districts" + '</option>';
for (i = 1; i <= 49; i++) {
    select2 += '<option val=' + i + '>' +'Legislative District ' + i + '</option>';
}
$('#selectDistrict').html(select2);

// *********************************** Dynamically add the legends *****************************************************
var select = '';
select += '<a href="#" ' + 'id=' + '"alleng" ' + 'value=' + '"allengagement"><span style="background-color: #ffffff; border: 1px solid #ffffff"></span><b>All Engagement Types</b></a>' + "<br>";
for (var i = 0; i < Engagement.length; i++) {
    var color = colorcode[i]
    var engagement = Engagement[i]
    select += `<a href="#"  id="${engagement.valueOf()}" value="${engagement.valueOf()}"><span style="background-color: ${color}"></span><b>${engagement.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);



// *********************************** Dynamically add the legends *****************************************************
var select1 = '';
select1 += '<option val=' + "allmiss" + ' selected="selected">' + 'All Mission Areas' + '</option>';
for (i = 0; i < Missionarea.length; i++) {
    select1 += '<option val=' + Missionarea[i] + '>' + Missionarea[i] + '</option>';
}
$('#selectMisstype').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select6 = '';
select6 += '<option val=' + "alltypes" + ' selected="selected">' + 'All Community Partner Types' + '</option>';
for (i = 0; i < CommunityType.length; i++) {
    select6 += '<option val=' + CommunityType[i] + '>' + CommunityType[i] + '</option>';
}
$('#selectCommtype').html(select6);
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var select4 = '';
select4 += '<option val=' + "allcampus" + ' selected="selected">' + 'All Campus Partners' + '</option>';
for (i = 0; i < CampusPartnerlist.length; i++) {
    select4 += '<option val=' + CampusPartnerlist[i] + '>' + CampusPartnerlist[i] + '</option>';
}
$('#selectCampus').html(select4);

//*********************************** Add year filter *****************************************************

var select5 = '';
select5 += '<option val=' + 0 + '>' + 'All Academic Years' + '</option>';
for (i = 0; i < yearlist.length; i++) {
    select5 += '<option val=' + i + '>' + yearlist[i] + '</option>';
}
$('#selectYear').html(select5);


//*********************************** Add Community Partner *****************************************************

var select3 = '';
select3 += '<option val=' + 0 + '>' + 'All Community Partners' + '</option>';
for (i = 0; i < communityPartnerlist.length; i++) {
    select3 += '<option val=' + i + '>' + communityPartnerlist[i] + '</option>';
}
$('#selectCommunity').html(select3);


//*********************************** Add Community Partner *****************************************************

var select7 = '';
select7 += '<option val=' + "allcollege" + ' selected="selected">' + 'All Colleges' + '</option>';
for (i = 0; i < CollegeNamelist.length; i++) {
    select7 += '<option val=' + i + '>' + CollegeNamelist[i] + '</option>';
}
$('#selectCollege').html(select7);





//*********************************** Load the map *****************************************************

var markers =[];
var oms = new OverlappingMarkerSpiderfier(map, {keepSpiderfied : true, markersWontMove : true, legWeight: 0.5});

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
    // console.log(districtData)

    map.data.setStyle({
        fillColor: "#fee8c8",
        fillOpacity: 0.5,
        strokeWeight: 0.2
    })

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
    // var contentString =
    var proj_name = projectData.features
    var miss_name = projectData.features
    var comm_partner = projectData.features
    var comm_partner_type = projectData.features
    var campus_partner = projectData.features
    var academic_year = projectData.features
    var eng_type = projectData.features

    console.log(projectData.features)
    for (i=0; i<projectData.features.length; i++) {
        var category = projectData.features[i].properties["Legislative District Number"]
        var academic = projectData.features[i].properties["Academic Year"]
        var engagementType = projectData.features[i].properties["Engagement Type"]
        var mission = projectData.features[i].properties["Mission Area"]
        var commType = projectData.features[i].properties["Community Partner Type"]
        var yearTest = projectData.features[i].properties["yeartest"]
        var campusTest = projectData.features[i].properties["campustest"]
        var commmunityTest = projectData.features[i].properties["communitytest"]
        var projectName = projectData.features[i].properties["Project Name"]
        var collegeName = projectData.features[i].properties["College Name"]
        var marker = new google.maps.Marker({

            position: {
                lat: parseFloat(projectData.features[i].geometry.coordinates[1]+ (Math.random() -.5) / 50000),
                lng: parseFloat(projectData.features[i].geometry.coordinates[0]+ (Math.random() -.5) / 50000)
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: markercolor(engagementType),
            category: category,
            year: academic,
            mission: mission,
            commPartType: commType,
            engagementType: engagementType,
            yearTest: yearTest,
            campusTest: campusTest,
            commmunityTest: commmunityTest,
            projectName: projectName,
            collegeName: collegeName
        });

        //spiderify
        oms.addMarker(marker);

        function markercolor(engagementType) {
            if (engagementType == "Community-Based Learning"){
                return circle.fillColor= colorcode[0]
            }
            else if (engagementType == "Knowledge/Info Sharing"){
                return circle.fillColor= colorcode[1]
            }
            else if (engagementType == "Providing Access") {
                return circle.fillColor = colorcode[2]
            }
            else if (engagementType == "Service Learning") {
                return circle.fillColor = colorcode[3]

            }
            else if (engagementType == "Volunteering") {
                return circle.fillColor = colorcode[4]
            }
        }

        attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
            comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
            campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic Year'],
            eng_type[i].properties['Engagement Type'] );
        markers.push(marker)

    }
    //adding the marker cluster functionality
    markerCluster = new MarkerClusterer(map, markers,mcOptions);

});


var mcOptions = {
    minimumClusterSize: 10, //minimum number of points before which it should be clustered
    maxZoom: 15,
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

var openedInfoWindow=null;

// function to call the infowindow on clicking markers
function attachMessage(marker, projectName, missionArea,comm_partner, comm_partner_type, campus_partner,academic_year, eng_type) {
    var infowindow = new google.maps.InfoWindow();
    google.maps.event.addListener(marker, 'click', function () {
        if (openedInfoWindow != null) openedInfoWindow.close();
        infowindow.setContent('<tr><td><span style="font-weight:bold">Project Name:</span>&nbsp;&nbsp; </td><td>' + projectName.toString().split(":")[0] + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Areas: </span>&nbsp; </td><td>' + missionArea + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partners: </span>&nbsp; </td><td>' + comm_partner + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partner Type: </span>&nbsp; </td><td>' + comm_partner_type + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campus_partner + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp; </td><td>' + academic_year + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Engagement Type: </span>&nbsp; </td><td>' + eng_type + '</td></tr>')
        infowindow.open(map, marker);
        // map.setZoom(16);
        map.panTo(this.getPosition());
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


///***********************************filter by clickable legends*****************************************************


//***************************Engagement type filter*****************************************************

var edu = document.getElementById("alleng"); //get the total number of dots
edu.addEventListener("click", function(e) {
    filterlist[0] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
})

$('#legend a').click(function(e) { //filter dots by mission areas and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    var i = Engagement.indexOf(clickedValue);
    if (i > -1) {
        filterlist[0] = clickedValue;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    }
});


//*********************************** Mission Area filter *****************************************************

var selectMisstype = document.getElementById('selectMisstype');
selectMisstype.addEventListener("change", function(e) {
    var value = e.target.value.trim();
    console.log(value)
    if (!Missionarea.includes(value)) {
        //get the number of markers and show it on the HTML
        filterlist[1] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    } else {
        for (var i = 0; i <= Missionarea.length; i++) {
            if (value == Missionarea[i]) {
                filterlist[1] = value
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
            }
        }
    }
})





//*********************************** Campus Partner filter *****************************************************

var selectCampus = document.getElementById('selectCampus'); //get the element on HTML
selectCampus.addEventListener("change", function(e) {
    var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
    if (!CampusPartnerlist.includes(value)) { // in the case of all Campus partners
        filterlist[4] = "all";
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    } else { //in case a campus partner is chosen
        projectData.features.forEach(function(feature) { //iterate through the dataset
            var campuspartner = feature.properties["Campus Partner"] //get the campus partner
            if (campuspartner.includes(value)) { // if the partner has that campus partner
                feature.properties["campustest"] = 1 // assign this value 1
            } else {
                feature.properties["campustest"] = 0 //if not, assign this value 0
            }
        })

        for (i=0;i<markers.length; i++){
            if(projectData.features[i].properties['campustest']==1){
                markers[i].campusTest=1;
            }
            else
                markers[i].campusTest=0;

            filterlist[4] = 1;
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
        }
    }
})


//*********************************** Community partner filter *****************************************************

var selectCommunity = document.getElementById('selectCommunity'); //get the element on HTML
selectCommunity.addEventListener("change", function(e) {
    var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
    if (!communityPartnerlist.includes(value)) { // in the case of all Campus partners
        filterlist[3] = "all";
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    } else { //in case a campus partner is chosen
        projectData.features.forEach(function(feature) { //iterate through the dataset
            var communitypartner = feature.properties["Community Partner"] //get the campus partner
            if (communitypartner.includes(value)) { // if the partner has that campus partner
                feature.properties["communitytest"] = 1 // assign this value 1
            } else {
                feature.properties["communitytest"] = 0 //if not, assign this value 0
            }
        })

        for (i=0;i<markers.length; i++){
            if(projectData.features[i].properties['communitytest']==1){
                markers[i].communityTest=1;
            }
            else
                markers[i].commmunityTest=0;

            filterlist[3] = 1;
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
        }
    }
})





//*********************************** Community Type filter *****************************************************

var selectCommtype = document.getElementById('selectCommtype');
selectCommtype.addEventListener("change", function(e) {
    var value = e.target.value.trim();

    if (!CommunityType.includes(value)) {
        //get the number of markers and show it on the HTML
        filterlist[6] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    } else {
        for (var i = 0; i < CommunityType.length; i++) {
            if (value == CommunityType[i]) {
                filterlist[6] = value
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
            }
        }
    }
})


//*********************************** College Name filter *****************************************************

var selectCollege = document.getElementById('selectCollege');
selectCollege.addEventListener("change", function(e) {
    var value = e.target.value.trim();

    if (!CollegeNamelist.includes(value)) {
        //get the number of markers and show it on the HTML
        filterlist[7] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    } else {
        for (var i = 0; i < CollegeNamelist.length; i++) {
            if (value == CollegeNamelist[i]) {
                filterlist[6] = value
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
                    filterlist[6], filterlist[7]);
            }
        }
    }
})




//*********************************** Academic Year filter *****************************************************

var selectYear = document.getElementById('selectYear'); //same concept as campus partner. Just for years
selectYear.addEventListener("change", function(e) {
    var value = e.target.value.trim();
    // conole.log(value)
    if (!yearlist.includes(value)) {
        filterlist[5] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
    } else {
        projectData.features.forEach(function (feature) {
            var year = feature.properties["Academic year"]
            if (year) {
                for (var j = 0; j < year.length; j++) {
                    if (year[j] == value) {
                        feature.properties["yeartest"] = 1;

                    } else {
                        feature.properties["yeartest"] = 0;

                    }
                }
            } else {
                feature.properties["yeartest"] = 0
            }
        })
        for (i=0;i<markers.length; i++){
            if(projectData.features[i].properties['yeartest']==1){
                markers[i].yearTest=1;
            }
            else
                markers[i].yearTest=0;

            filterlist[5] = 1
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);
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
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6],
            filterlist[7])
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
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5],
            filterlist[6], filterlist[7]);

    }
})


//*******************h**************** Search function *****************************************************
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
            projName = markers[i].projectName.toLowerCase();
            if (projName.includes(value)) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);

            }
        }
        markerCluster.redraw();
    }
})



$("#reset").click(function() {
    filterlist[0] = "all";
    filterlist[1] = "all";
    filterlist[2] = "all";
    filterlist[3] = "all";
    filterlist[4] = "all";
    filterlist[5] = "all";
    filterlist[6] = "all";
    filterlist[7] = "all";
    for (var k=0; k<states.length; k++) {
        states[k].setMap(null);
    }
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4],filterlist[5],filterlist[6],
        filterlist[7]);
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

    $('#selectCommunity option').prop('selected', function() {
        return this.defaultSelected;
    });
     $('#alleng option').prop('selected', function() {
        return this.defaultSelected;
    });

    $('#selectCollege option').prop('selected', function() {
        return this.defaultSelected;
    });

});


//To vary the total number of projects based on the filter selected

//To vary the total number of projects based on the filter selected
    function calculation(a, b, c, d, e, f, g, h) {
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
                            totalnumber += projectData.features.length
                        } else {
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].campusTest !== 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1) {
                                    number += 1
                                }
                            })
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1) {
                                    if (feature.properties['campustest'] == 1) {
                                        number += 1
                                    }
                                }
                            })

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].campusTest == 1 && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['campustest'] == 1) {
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
                        }
                    } else {
                        if (e == "all") {
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].category == c && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].category == c && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Mission Area'] == b && feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].communityTest == 1) {
                                    markers[i].setVisible(true);
                                    markerCluster.addMarker(markers[i]);
                                } else {
                                    markers[i].setVisible(false);
                                    markerCluster.removeMarker(markers[i]);
                                }
                            }
                            totalnumber += number

                        } else {
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();

                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].category == c) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].category == c && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            })
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].category == c && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == b) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].mission == b && markers[i].category == c && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].category == c) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['campustest'] == 1 && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].category == c && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].category == c && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].category == c && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Mission Area'] == b && feature.properties['campustest'] == 1 && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].category == c) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].category == c && markers[i].campusTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].category == c && markers[i].communityTest == 1) {
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
                            projectData.features.forEach(function (feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['communitytest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == b && feature.properties['Engagement Type'] == a) {
                                    number += 1
                                }
                            });
                            markerCluster.clearMarkers();
                            for (var i = 0; i < markers.length; i++) {
                                if (markers[i].engagementType == a && markers[i].mission == b && markers[i].category == c && markers[i].communityTest == 1 && markers[i].campusTest == 1) {
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
