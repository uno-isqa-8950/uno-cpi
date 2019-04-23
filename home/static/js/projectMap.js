// mapboxgl.accessToken = 'pk.eyJ1IjoidmJoYXRob3NtYXQiLCJhIjoiY2pyNGc5MzNzMDNvZTQ1bzIxcmJ5ejJhayJ9.lMH6o8Nk36qm3lG3M0apdQ';
var projectData = JSON.parse(document.getElementById('project-data').textContent); //load the variable from views.py. See the line from html first
var districtData = JSON.parse(document.getElementById('district').textContent); //load the variable from views.py. See the line from html first
// const colorCodeObject = {
//     "Community-Based Learning": "#27ffcb",
//     "Knowledge/Info Sharing" : "#65dc1e",
//     "Providing Access": "#1743f3",
//     "Service Learning": "#ba55d3",
//     "Volunteering": "#e55e5e"
// }
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CollegeNamelist = JSON.parse(document.getElementById('collegename-list').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityPartnerlist = JSON.parse(document.getElementById('communitypartner-list').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var Engagement = JSON.parse(document.getElementById('engagementType').textContent);

const colorCodeObject = {
    [Engagement[0]]:         "#01B8AA",
    [Engagement[1]]:         "#374649",
    [Engagement[2]]:    "#FD625E",
    [Engagement[3]]:          "#8AD4EB",
    [Engagement[4]]:        "#FE9666",
    [Engagement[5]]:       "#A66999",
    [Engagement[6]]:       "#3599B8",
    [Engagement[7]]:       "#DFBFBF",
    [Engagement[8]]:       "#1743f3"
}
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
   "featureType": "road.highway",
   "elementType": "geometry.stroke",
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
select2 += '<option value=' + '"All Legislative Districts" '+ ' selected="selected">' + "All Legislative Districts" + '</option>';
for (i = 1; i <= 49; i++) {
    select2 += '<option value=' + i + '>' +'Legislative District ' + i + '</option>';
}
$('#selectDistrict').html(select2);

// *********************************** Dynamically add the legends *****************************************************
var select = '';
select += '<a href="#" ' + 'id=' + '"All Engagement Types" ' + 'class="selectEngagement"' + 'value="' + 'All Engagement Types"><span style="background-color: #ffffff; border: 1px solid #ffffff"></span><b>All Engagement Types</b></a>' + "<br>";
for (var i = 0; i < Engagement.length; i++) {
    var engagement = Engagement[i]
    var color = colorCodeObject[engagement];
    select += `<a href="#"  id="${engagement.valueOf()}" class="selectEngagement" value="${engagement.valueOf()}"><span style="background-color: ${color}"></span><b>${engagement.toString()}</b></a>` + "<br>";
}
$('#engagementFilters').html(select);



// *********************************** Dynamically add the legends *****************************************************
var select1 = '';
select1 += '<option value="' + "All Mission Areas" + '" selected="selected">' + 'All Mission Areas' + '</option>';
for (i = 0; i < Missionarea.length; i++) {
    select1 += '<option value="' + Missionarea[i] + '">' + Missionarea[i] + '</option>';
}
$('#selectMission').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select6 = '';
select6 += '<option value="' + "All Community Partner Types" + '" selected="selected">' + 'All Community Partner Types' + '</option>';
for (i = 0; i < CommunityType.length; i++) {
    select6 += '<option value="' + CommunityType[i] + '">' + CommunityType[i] + '</option>';
}
$('#selectCommunityType').html(select6);
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var select4 = '';
select4 += '<option value="' + "All Campus Partners" + '" selected="selected">' + 'All Campus Partners' + '</option>';
for (i = 0; i < CampusPartnerlist.length; i++) {
    select4 += '<option value="' + CampusPartnerlist[i].name + '">' + CampusPartnerlist[i].name + '</option>';
}
$('#selectCampus').html(select4);

//*********************************** Add year filter *****************************************************

var select5 = '';
select5 += '<option value="' + "All Academic Years" + '" selected="selected">' + 'All Academic Years' + '</option>';
for (i = 0; i < yearlist.length; i++) {
    select5 += '<option value="' + yearlist[i] + '">' + yearlist[i] + '</option>';
}
$('#selectYear').html(select5);


//*********************************** Add Community Partner *****************************************************

var select3 = '';
select3 += '<option value="' + "All Community Partners" + '" selected="selected">' + 'All Community Partners' + '</option>';
for (i = 0; i < communityPartnerlist.length; i++) {
    select3 += '<option value="' + communityPartnerlist[i] + '">' + communityPartnerlist[i] + '</option>';
}
$('#selectCommunity').html(select3);


//*********************************** Add Community Partner *****************************************************

var select7 = '';
select7 += '<option value="' + "All Colleges and Main Units" + '" selected="selected">' + 'All Colleges and Main Units' + '</option>';
for (i = 0; i < CollegeNamelist.length; i++) {
    select7 += '<option value="' + CollegeNamelist[i].id + '">' + CollegeNamelist[i].cname + '</option>';
}
$('#selectCollege').html(select7);

//*********************************** Load the map *****************************************************

var markers =[];
var oms = new OverlappingMarkerSpiderfier(map, {keepSpiderfied : true, markersWontMove : true, legWeight: 1.5});
var markerCluster = null;
var defaultFilterValues = [];
var filters = {};

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
        var selectDistrict = projectData.features[i].properties["Legislative District Number"]
        var selectYear = projectData.features[i].properties["Academic Year"]
        var selectEngagement = projectData.features[i].properties["Engagement Type"]
        var selectMission = projectData.features[i].properties["Mission Area"]
        var selectCommunityType = projectData.features[i].properties["Community Partner Type"]
        var yearTest = projectData.features[i].properties["yeartest"]
        var campusTest = projectData.features[i].properties["campustest"]
        var communityTest = projectData.features[i].properties["communitytest"]
        var projectName = projectData.features[i].properties["Project Name"]
        var selectCommunity = projectData.features[i].properties["Community Partner"]
        var selectCampus = projectData.features[i].properties["Campus Partner"]
        var selectCollege = projectData.features[i].properties["College Name"]
        var marker = new google.maps.Marker({

            position: {
                lat: parseFloat(projectData.features[i].geometry.coordinates[1])+ (Math.random() -.5) / 25000,
                lng: parseFloat(projectData.features[i].geometry.coordinates[0])+ (Math.random() -.5) / 25000
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: engagementColor(selectEngagement),
            selectDistrict: selectDistrict,
            selectYear: selectYear,
            selectMission: selectMission,
            selectCommunityType: selectCommunityType,
            selectEngagement: selectEngagement,
            yearTest: yearTest,
            selectCampus: selectCampus,
            selectCommunity: selectCommunity,
            projectName: projectName,
            selectCollege: selectCollege
        });

        //spiderify
        oms.addMarker(marker);

        function engagementColor(engagementType) {
            return circle.fillColor = colorCodeObject[engagementType];
        }

        attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area'],
            comm_partner[i].properties['Community Partner'], comm_partner_type[i].properties['Community Partner Type'],
            campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic Year'],
            eng_type[i].properties['Engagement Type'] );
        markers.push(marker)

    }
    //adding the marker cluster functionality
    markerCluster = new MarkerClusterer(map, markers,mcOptions);

     // Default value array for all filters
    defaultFilterValues = ["All Engagement Types", "All Mission Areas","All Colleges and Main Units", "All Campus Partners","All Community Partners", "All Community Partner Types","All Legislative Districts","All Academic Years",];
    // Object to identify filters set by the user
    filters = {
        "selectEngagement":     "All Engagement Types",
        "selectMission":        "All Mission Areas",
        "selectCollege":        "All Colleges and Main Units",
        "selectCampus":         "All Campus Partners",
        "selectCommunity":      "All Community Partners",
        "selectCommunityType":  "All Community Partner Types",
        "selectDistrict":       "All Legislative Districts",
        "selectYear":           "All Academic Years"
    };

});


var mcOptions = {
    minimumClusterSize: 10, //minimum number of points before which it should be clustered
    maxZoom: 15,
    averageCenter: true,
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
    google.maps.event.addListener(marker, 'click', function() {
        if (openedInfoWindow != null) openedInfoWindow.close();
        infowindow.setContent('<tr><td><span style="font-weight:bold">Project Name:</span>&nbsp;&nbsp; </td><td>' + projectName.toString().split(":")[0] + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Areas: </span>&nbsp; </td><td>' + missionArea + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partners: </span>&nbsp; </td><td>' + comm_partner.join(" | ") + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partner Type: </span>&nbsp; </td><td>' + comm_partner_type.join(" | ")  + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campus_partner.join(" | ") + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp; </td><td>' + academic_year.join(" | ")  + '</td></tr><br />' +
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
    infowindow.close(map);
})


///***********************************filter by clickable legends*****************************************************
var states = new Array();
var selectDistrict = document.getElementById('selectDistrict');
selectDistrict.addEventListener("change", function (e) {
    var value = e.target.value.trim()
    // var value=value1.split("Legislative District")[1]
    value = parseInt(value)
    // console.log(value1, value)
    if (isNaN(value)) {
        for (var k=0; k<states.length; k++) {
            states[k].setMap(null);
        }
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

    }
})

// Check if a marker already exists in a cluster
function isMarkerAlreadyAdded(marker) {
    var clusterMarkers = markerCluster.getMarkers();
    if (clusterMarkers.indexOf) {
        return clusterMarkers.indexOf(marker) != -1;
    } else {
        for (var i = 0, m; m = clusterMarkers[i]; i++) {
            if (m == marker) {
                return true;
            }
        }
    }
    return false;
};

// Get the size of cluster in the current state
function getClusterSize() {
    return markerCluster.getMarkers().length;
}

function mapFilter(id, value) {
    if (filters[id]) {
        filters[id] = value;
    }
}

function getSetFilterOptions() {
    var returnArray = [];
    for (option in filters) {
        if (!defaultFilterValues.includes(filters[option])) {
            returnArray.push(option);
        }
    }
    return returnArray;
}

function returnKeepValue(setFilters, marker) {
    let returnValue = false;
    for (let opt of setFilters) {
        if (Array.isArray(marker[opt]) && marker[opt].includes(filters[opt])) {
            returnValue = true;
        } else if (marker[opt] == filters[opt]) {
            returnValue = true;
        } else {
            // reset keep variable to false even if one of them is false and return
            return false;
        }
    }
    return returnValue;
}

function filterMarkers() {
    const setFilters = getSetFilterOptions();
    console.log("Set filters: ", setFilters);

    for (var i = 0; i < markers.length; i++) {
        let marker = markers[i];
        let keep = returnKeepValue(setFilters, marker);
        if (!setFilters.length) {
            // This is case when all filters are set to default values, so all markers are needed
            keep = true;
        }
        marker.setVisible(keep);
        if (keep && !(isMarkerAlreadyAdded(marker))) {
            markerCluster.addMarker(marker);
        } else if (!keep) {
            markerCluster.removeMarker(marker);
        }
    }
}

const selectCollege_tag = document.getElementById('selectCollege');
selectCollege_tag.addEventListener("change", function(event) {
    var select3 = '';
    select3 += '<option value="' + "All Campus Partners" + '" selected="selected">' + 'All Campus Partners' + '</option>';
    for (i = 0; i < CampusPartnerlist.length; i++) {
        if(CampusPartnerlist[i].c_id == selectCollege_tag.value || selectCollege_tag.value == 'All Colleges and Main Units')
            select3 += '<option value= "' + CampusPartnerlist[i].name + '">' + CampusPartnerlist[i].name + '</option>';
    }
    $('#selectCampus').html(select3);
    mapFilter('selectCampus', 'All Campus Partners');

    mapFilter('selectCollege', selectCollege_tag.options[selectCollege_tag.selectedIndex].text);
    filterMarkers();
    $('#totalnumber').html(getClusterSize());
});

// Create a wrapper div around all the filters and a change event listener
// when any of the filters are changed
const selectFilters = document.getElementById('state-legend');
selectFilters.addEventListener("change", function(event) {
    if (event.target == valueFilter){
        return
    }
    else {
        const selectFilterChildren = Array.from(selectFilters.children);

        selectFilterChildren.forEach((child) => {
            // Set each filter's value
            if (child.id !== "engagementFilters" && child.id !== "selectCollege") {
                mapFilter(child.id, child.value);
            }
        });
        filterMarkers();
        $('#totalnumber').html(getClusterSize());
    }
});




var engagementFilters = Array.from(document.getElementsByClassName("selectEngagement"));
for (let engageFilter of engagementFilters) {
    engageFilter.addEventListener("click", function(event) {
        let value = engageFilter.textContent;
        mapFilter("selectEngagement", value);
        filterMarkers();
        $('#totalnumber').html(getClusterSize());
    });
}

//*********************************** Search function *****************************************************
var valueFilter = document.getElementById("valueFilter");

//Press the listening button
valueFilter.addEventListener("keydown", function (e) {
    if (e.keyCode == 8 || e.keyCode == 46) {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setVisible(false);
            markerCluster.clearMarkers(markers[i]);
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
            cpname = markers[i].projectName.toLowerCase();
            if (cpname.includes(value)) {
                markers[i].setVisible(true);
                markerCluster.addMarker(markers[i]);
            } else {
                markers[i].setVisible(false);
                markerCluster.removeMarker(markers[i]);

            }
        }
        markerCluster.redraw();
    }
});

$("#reset").click(function () {
    const defaultFilterObject = {
        "selectEngagement":     "All Engagement Types",
        "selectMission":        "All Mission Areas",
        "selectCollege":        "All Colleges and Main Units",
        "selectCampus":         "All Campus Partners",
        "selectCommunity":      "All Community Partners",
        "selectCommunityType":  "All Community Partner Types",
        "selectDistrict":       "All Legislative Districts",
        "selectYear":           "All Academic Years"
    };
    valueFilter.value = '';
    Object.assign(filters, defaultFilterObject);
    for (const filter in filters) {
        console.log(`${filters[filter]}`)
        $('#' + filter).val(`${filters[filter]}`);
    }
    for (var k=0; k<states.length; k++) {
            states[k].setMap(null);
        }
    var select3 = '';
    select3 += '<option value="' + "All Campus Partners" + '" selected="selected">' + 'All Campus Partners' + '</option>';
    for (i = 0; i < CampusPartnerlist.length; i++) {
        select3 += '<option value= "' + CampusPartnerlist[i].name + '">' + CampusPartnerlist[i].name + '</option>';
    }
    $('#selectCampus').html(select3);

    filterMarkers();
    $('#totalnumber').html(getClusterSize());
});