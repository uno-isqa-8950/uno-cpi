//*********************************** Get mapbox API and get data from HTML *****************************************************

// mapboxgl.accessToken = 'pk.eyJ1IjoidW5vY3BpZGV2dGVhbSIsImEiOiJjanJiZTk2cjkwNjZ5M3l0OGNlNWZqYm91In0.vPmkC3MFDrTlBk-ntUFruA';
// var colorcode = ['#27ffcb', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#29234b'] --old code
// const colorCodeObject = {
//     "Economic Sufficiency":         "#27ffcb",
//     "Educational Support" :         "#65dc1e",
//     "Environmental Stewardship":    "#1743f3",
//     "Health and Wellness":          "#ba55d3",
//     "International Service":        "#e55e5e",
//     "Social Justice":               "#29234b"
// }
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var districtData = JSON.parse(document.getElementById('district-data').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CollegeName = JSON.parse(document.getElementById('college-list').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);

const colorCodeObject = {
    [Missionarea[0]]:         "#01B8AA",
    [Missionarea[1]]:         "#374649",
    [Missionarea[2]]:    "#FD625E",
    [Missionarea[3]]:          "#8AD4EB",
    [Missionarea[4]]:        "#FE9666",
    [Missionarea[5]]:       "#A66999",
    [Missionarea[6]]:       "#3599B8",
    [Missionarea[7]]:       "#DFBFBF",
    [Missionarea[8]]:       "#1743f3"
}
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



//*********************************** Dynamically add the legends *****************************************************
var select = '';
select += '<a href="#" ' + 'id=' + '"All Mission Areas" ' + 'class="selectMission"' + 'value="' + 'All Mission Areas"><span style="background-color: #ffffff; border: 1px solid #ffffff"></span><b>All Mission Areas</b></a>' + "<br>";
for (var i = 0; i < Missionarea.length; i++) {
    var mission = Missionarea[i];
    var color = colorCodeObject[mission];
    select += `<a href="#"  id="${mission.valueOf()}" class="selectMission" value="${mission.valueOf()}"><span style="background-color: ${color}"></span><b>${mission.toString()}</b></a>` + "<br>";
}
$('#missionAreaFilters').html(select);
//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option value="' + "All Legislative Districts" + '" selected="selected">' + "All Legislative Districts" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option value=' + i + '>' +'Legislative District ' + i + '</option>';
}
$('#selectDistrict').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select2 = '';
select2 += '<option value="' + "All Community Partner Types" + '" selected="selected">' + 'All Community Partner Types' + '</option>';
for (i = 0; i < CommunityType.length; i++) {
    select2 += '<option value="' + CommunityType[i] + '">' + CommunityType[i] + '</option>';
}
$('#selectCommtype').html(select2);
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var select3 = '';
select3 += '<option value="' + "All Campus Partners" + '" selected="selected">' + 'All Campus Partners' + '</option>';
for (i = 0; i < CampusPartnerlist.length; i++) {

    select3 += '<option value= "' + CampusPartnerlist[i].name + '">' + CampusPartnerlist[i].name + '</option>';
}
$('#selectCampus').html(select3);

//*********************************** Add year filter *****************************************************

var select4 = '';
select4 += '<option value="' + "All Academic Years" + '" selected="selected">' + 'All Academic Years' + '</option>';
for (i = 0; i < yearlist.length; i++) {
    select4 += '<option value="' + yearlist[i] + '">' + yearlist[i] + '</option>';
}
$('#selectYear').html(select4);

//*********************************** Add id variable to College Data GEOJSON for search function later *****************************************************

var select5 = '';
select5 += '<option value="' + "All Colleges and Main Units" + '" selected="selected">' + 'All Colleges and Main Units' + '</option>';
for (i = 0; i < CollegeName.length; i++) {
    select5 += '<option value="' + CollegeName[i].id + '">' + CollegeName[i].cname + '</option>';
}
$('#selectCollege').html(select5);


//*********************************** Load the map *****************************************************
var markers =[];
var oms = new OverlappingMarkerSpiderfier(map, {keepSpiderfied : true, markersWontMove : true, legWeight: 1.5});
var markerCluster = null;
var defaultFilterValues = [];
var filters = {};

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

     map.data.loadGeoJson('../../static/GEOJSON/ID2.geojson')

    //To DO :If any district is selected highlight it
    map.data.setStyle({
        fillColor: "#fee8c8",
        fillOpacity: 0.4,
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
    var comm_name = communityData.features
    var miss_name = communityData.features
    var partner_name = communityData.features
    var district_number = communityData.features
    var project_number = communityData.features
    var campus_partner = communityData.features
    var academic_year = communityData.features
    var website = communityData.features
    var city = communityData.features
    var projects = communityData.features
    for (i=0; i<communityData.features.length; i++) {
        var selectDistrict = communityData.features[i].properties["Legislative District Number"]
        var selectYear = communityData.features[i].properties["Academic Year"]
        var engagementType = communityData.features[i].properties["Engagement Type"]
        var selectCommtype = communityData.features[i].properties["CommunityType"]
        var selectMission = communityData.features[i].properties["Mission Area"]
        var selectCampus = communityData.features[i].properties["Campus Partner"]
        var yearTest = communityData.features[i].properties["yeartest"]
        var campusTest = communityData.features[i].properties["campustest"]
        var communityPartnerInputFilter = communityData.features[i].properties["CommunityPartner"]
        var commPartnerName = communityData.features[i].properties["CommunityPartner"]
        var selectCollege = communityData.features[i].properties["College Name"]
        var marker = new google.maps.Marker({
            position: {
                lat: parseFloat(communityData.features[i].geometry.coordinates[1])+ (Math.random() -.5) / 25000,
                lng: parseFloat(communityData.features[i].geometry.coordinates[0])+ (Math.random() -.5) / 25000
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: missionColor(selectMission),
            selectDistrict: selectDistrict,
            selectYear: selectYear,
            selectMission: selectMission,
            selectCommtype: selectCommtype,
            selectCampus: selectCampus,
            yearTest: yearTest,
            campusTest: campusTest,
            commPartnerName: commPartnerName,
            communityPartnerInputFilter: communityPartnerInputFilter,
            selectCollege: selectCollege
        });

        oms.addMarker(marker);
       function missionColor(mission) {
            return circle.fillColor = colorCodeObject[mission];
        }
        attachMessage(marker, partner_name[i].properties['CommunityPartner'],
            project_number[i].properties['Number of projects'],city[i].properties['City'],
            miss_name[i].properties["Mission Area"], comm_name[i].properties["CommunityType"],
            campus_partner[i].properties["Campus Partner"],
            academic_year[i].properties["Academic Year"],
            website[i].properties["Website"],projects[i].properties["Projects"]);
        markers.push(marker)
    }
    //adding the marker cluster functionality
    markerCluster = new MarkerClusterer(map, markers,mcOptions);

     // Default value array for all filters
    defaultFilterValues = ["All Mission Areas", "All Campus Partners", "All Community Partner Types", "All Legislative Districts", "All Academic Years", "All Colleges and Main Units"];
    // Object to identify filters set by the user
    filters = {
        "selectMission":        "All Mission Areas",
        "selectCampus":         "All Campus Partners",
        "selectCommtype":       "All Community Partner Types",
        "selectDistrict":       "All Legislative Districts",
        "selectYear":           "All Academic Years",
        "selectCollege":        "All Colleges and Main Units"
    };

});

var mcOptions = {
    maxZoom: 15,
    minimumClusterSize: 10, //minimum number of points before which it should be clustered
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
var rightclickwindow = null;

// function to call the infowindow on clicking markers
function attachMessage(marker, partner_name,project_number,city,miss_name, comm_name, campus_partner,academic_year,website,projects) {
    var infowindow = new google.maps.InfoWindow();

    google.maps.event.addListener(marker, 'click', function() {
        if (openedInfoWindow != null) openedInfoWindow.close();  // <-- changed this
        infowindow.setContent('<tr><td style="margin-top: 5%"><span style="font-weight:bold">Community Partner:</span>&nbsp;&nbsp; </td><td>' + partner_name + '</td></tr><br />' +
            // '<tr><td><span style="font-weight:bold">Legislative District Number: </span>&nbsp; </td><td>' + district_number + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Number of Projects: </span>&nbsp; </td><td>' + project_number + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">City: </span>&nbsp; </td><td>' + city + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Areas: </span>&nbsp; </td><td>' + miss_name + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Community Partner Type:</span>&nbsp;&nbsp; </td><td>' + comm_name + '&nbsp;&nbsp;</td></tr><br />' +
            // '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campus_partner.toString().split(",").join(" , ")+ '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campus_partner.join(" | ")+ '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp; </td><td>' + academic_year.join(" | ")  + '&nbsp;&nbsp;</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Website:</span>&nbsp;&nbsp;<td><a id="websitelink" href="' + website + '" target="_blank">' + website + '</a></td></tr><br /><br>' +
            (project_number == 0 ? '':
                ('<tr style="margin-top: 5%"><td><span style="font-weight:lighter">Right-click on the marker to see the list of projects</span></td></tr>')));
        infowindow.open(map, marker);
        // map.setZoom(16);
        map.panTo(this.getPosition());
        // added next 4 lines
        openedInfoWindow = infowindow;
        google.maps.event.addListener(infowindow, 'closeclick', function() {
            openedInfoWindow = null;
        });
    });
    google.maps.event.addListener(marker, 'rightclick', function() {
        infowindow.setContent(
            '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Community Partner:</span>&nbsp;&nbsp; </td><td>' + partner_name + '</td></tr><br />' +
            // '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Projects:</span>&nbsp;&nbsp; </td><td>' + projects.toString().replace(/\s*\(.*?\)(?:,)\s*/g,"<br> ")+ '</td></tr><br />')
         // '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Projects:</span>&nbsp;&nbsp; </td><td>' + projects.toString().split(",").join("<br>")+ '</td></tr><br />')
        '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Projects:</span>&nbsp;&nbsp; </td><td>' + projects.join("<br>").replace(/\s*\(.*?\)\s*/g,"")+ '</td></tr><br />')
        map.panTo(this.getPosition());

        // google.maps.event.addListener(marker, 'rightclick', function() {
        if (rightclickwindow != null) rightclickwindow.close();  // <-- changed this
        infowindow.open(map, marker);
        rightclickwindow = infowindow;
        google.maps.event.addListener(infowindow, 'closeclick', function() {
            rightclickwindow = null;
        });
    });
}


// To prevent Info window opening on the first click on spiderfier
oms.addListener('spiderfy', function(markers) {
    infowindow.close(map);
})

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
        if (child.id !== "missionAreaFilters" && child.id !== "selectCollege") {
            mapFilter(child.id, child.value);
        }
    });
    filterMarkers();
    $('#totalnumber').html(getClusterSize());
    }
});

var missionAreaFilters = Array.from(document.getElementsByClassName("selectMission"));
for (let missionAreaFilter of missionAreaFilters) {
    missionAreaFilter.addEventListener("click", function(event) {
        let value = missionAreaFilter.textContent;
        mapFilter("selectMission", value);
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
            cpname = markers[i].commPartnerName.toLowerCase();
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
        "selectMission":        "All Mission Areas",
        "selectCampus":         "All Campus Partners",
        "selectCommtype":       "All Community Partner Types",
        "selectDistrict":       "All Legislative Districts",
        "selectYear":           "All Academic Years",
        "selectCollege":        "All Colleges and Main Units"
    };
    valueFilter.value = '';
    Object.assign(filters, defaultFilterObject);
    for (const filter in filters) {
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