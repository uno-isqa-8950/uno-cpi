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
var filterlist = ["all", "all", "all", "all", "all","all","all"]
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
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allengagement"><span style="background-color: #ffffff; border: 1px solid #ffffff"></span><b>All Engagement Types</b></a>' + "<br>";
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

var markers =[];
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
        // fillColor: markercolor(fillColor),
        fillOpacity: 1,
        strokeOpacity: 0.9,
        scale: 8,
        strokeColor: 'white',
        strokeWeight: 1.5,
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
        var academic = projectData.features[i].properties["Academic year"]
        var engagementType = projectData.features[i].properties["Engagement Type"]
        var mission = projectData.features[i].properties["Mission Area"]
        var commType = projectData.features[i].properties["Community Type"]
        var yearTest = projectData.features[i].properties["yeartest"]
        var campusTest = projectData.features[i].properties["campustest"]
        var commmunityTest = projectData.features[i].properties["communitytest"]
        var projectName = projectData.features[i].properties["Project Name"]
        var marker = new google.maps.Marker({

            position: {
                lat: parseFloat(projectData.features[i].geometry.coordinates[1]),
                lng: parseFloat(projectData.features[i].geometry.coordinates[0])
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: markercolor(engagementType),
            category: category,
            year: academic,
            mission: mission,
            commType: commType,
            engagementType: engagementType,
            yearTest: yearTest,
            campusTest: campusTest,
            commmunityTest: commmunityTest,
            projectName: projectName
        });

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
            campus_partner[i].properties['Campus Partner'], academic_year[i].properties['Academic year'],
            eng_type[i].properties['Engagement Type'] );
        markers.push(marker)

    }
    //adding the marker cluster functionality
    markerCluster = new MarkerClusterer(map, markers,mcOptions);

});


var mcOptions = {
    minimumClusterSize: 5, //minimum number of points before which it should be clustered
    ignoreHiddenMarkers:true,
    maxZoom: 20,
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
///***********************************filter by clickable legends*****************************************************


//***************************Engagement type filter*****************************************************

var edu = document.getElementById("all"); //get the total number of dots
edu.addEventListener("click", function(e) {
    filterlist[0] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
})

$('#legend a').click(function(e) { //filter dots by mission areas and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    var i = Engagement.indexOf(clickedValue);
    if (i > -1) {
        filterlist[0] = clickedValue;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6]);
    }
});


//*********************************** Mission Area filter *****************************************************

var selectMisstype = document.getElementById('selectMisstype');
selectMisstype.addEventListener("change", function(e) {
    var value = e.target.value.trim();

    if (!Missionarea.includes(value)) {
        //get the number of markers and show it on the HTML
        filterlist[1] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
    } else {
        for (var i = 0; i <= Missionarea.length; i++) {
            if (value == Missionarea[i]) {
                filterlist[1] = value
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
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
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6]);
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
                }
            filterlist[4] = 1;
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6]);

    }
})


//*********************************** Community partner filter *****************************************************

var selectCommunity = document.getElementById('selectCommunity'); //get the element on HTML
selectCommunity.addEventListener("change", function(e) {
    var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
    if (!communityPartnerlist.includes(value)) { // in the case of all Campus partners
        filterlist[3] = "all";
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6]);
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
                }
            filterlist[3] = 1;
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6]);

    }
})





//*********************************** Community Type filter *****************************************************

var selectCommtype = document.getElementById('selectCommtype');
selectCommtype.addEventListener("change", function(e) {
    var value = e.target.value.trim();

    if (!CommunityType.includes(value)) {
        //get the number of markers and show it on the HTML
        filterlist[6] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
    } else {
        for (var i = 0; i <= CommunityType.length; i++) {
            if (value == CommunityType[i]) {
                filterlist[6] = value
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
            }
        }
    }
})

//*********************************** Academic Year filter *****************************************************

var selectYear = document.getElementById('selectYear'); //same concept as campus partner. Just for years
selectYear.addEventListener("change", function(e) {
    var value = e.target.value.trim();
    if (!yearlist.includes(value)) {
        filterlist[5] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
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
                }

            filterlist[5] = 1
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])


    }
})

    //*********************************** District filter *****************************************************

    var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function (e) {
        var value = e.target.value.trim().toLowerCase();
        value = parseInt(value)
        if (isNaN(value)) {
            // get the number of markers that fit the requirement and show on the HTML
            filterlist[2] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
        } else {
            var value = e.target.value.trim().toLowerCase();
             // districtData.features.forEach(function (feature) {
             //    if (feature.properties['id'] == value) {
             //        var arrlength=districtData.features[i].geometry['coordinates'][0].length;
                    // for (j = 0; j < arrlength; j++) {
                    //     var x = parseFloat(districtData.features[i].geometry['coordinates'][0][j][1])
                    //     var y = parseFloat(districtData.features[i].geometry['coordinates'][0][j][0])
                        // console.log(x, y)
                        // var arr=[]
                        // for (k = 0; k < arrlength.length; k++) {
                        //     arr.push([{x, y}])


                        // console.log(polycord)

                        // console.log(arr)
                        //     }
                        //     for (k = 0; k < polycord.length; k++) {
                        //         var values = polycord[k]
                        //     }
                        //
                        // }
                        //  }
                        // console.log(polycord)
                        //     console.log(values)


                        // console.log("In district poly", districtPoly)
                    //     var districtPoly = new google.maps.Polygon({
                    //         paths: arr,
                    //         strokeColor: "#4ffe83",
                    //         strokeOpacity: 0.8,
                    //         strokeWeight: 2,
                    //         fillColor: "#61adfe",
                    //         fillOpacity: 0.5
                    //     });
                    //     console.log("In district poly", districtPoly)
                    //     // districtPoly.setMap(null);
                    //     districtPoly.setMap(map);
                    // }
            //     }
            //
            // })

            // map.data.setStyle({
            //     fillColor: '#42e2f4',
            //     strokeWeight:1
            // })



            filterlist[2] = value
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5], filterlist[6])
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
                projName = markers[i].projectName.toLowerCase();
                if (projName.includes(value)) {
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

     $('#selectCommunity option').prop('selected', function() {
        return this.defaultSelected;
    });

});

//To vary the total number of projects based on the filter selected
 function calculation(a, b, c, d, e, f, g) {
        var totalnumber = ''
        var number = 0

     if (a =="all"){
         if (b == "all"){
             if (c == "all"){
                 if(d=="all"){
                     if(e=="all"){
                         if(f=="all"){
                             if(g=="all"){
                                 for (var i = 0; i < markers.length; i++) {
                                     markers[i].setVisible(true);
                                     markerCluster.addMarker(markers[i]);
                                 }
                                 markerCluster.redraw();
                                 totalnumber += projectData.features.length
                             }
                             else {                                 //For filter - Selected Community Type
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['Community Partner Type'] == g) {
                                         number += 1
                                     }
                                 })
                                 for (var i = 0; i < markers.length; i++) {
                                     if (markers[i].commType == g) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }
                         }
                         else{
                             if(g=="all"){
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['yeartest'] == 1) {
                                         number += 1
                                     }
                                 })
                                 for (var i = 0; i < markers.length; i++) {
                                     if (markers[i].yearTest == 1) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }else { // Combination of Academic Year and Campus Partner Type being selected
                                 projectData.features.forEach(function (feature) {
                                     if ((feature.properties['Community Partner Type'] == g) && (feature.properties['yeartest'] == 1)) {
                                         number += 1
                                     }
                                 })
                                 for (var i = 0; i < markers.length; i++) {
                                     if ((markers[i].yearTest == 1) && (markers[i].commType == g)) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }
                         }
                     }
                     else{
                         if (f=="all") {

                             if (g=="all") {
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['campustest'] == 1) {number += 1}})
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
                             totalnumber+=number
                             }
                             else {//Combination of Community Partner Type and Campus Test is selected
                                 projectData.features.forEach(function (feature) {
                                     if ((feature.properties['Community Partner Type'] == g) && (feature.properties['campustest'] == 1)) {
                                         number += 1
                                     }
                                 })
                                 for (var i = 0; i < markers.length; i++) {
                                     if ((markers[i].commType == g) && (markers[i].campusTest == 1)) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }}
                         else {// Combination of Community Partner Type, Academic Year and Campus Partner selected
                             projectData.features.forEach(function (feature) {
                                 if ((feature.properties['Community Partner Type'] == g) && (feature.properties['campustest'] == 1)&& (feature.properties['yeartest'] == 1)) {
                                     number += 1
                                 }
                             })
                             for (var i = 0; i < markers.length; i++) {
                                 if ((markers[i].commType == g) && (markers[i].campusTest == 1) && (markers[i].yearTest)) {
                                     markers[i].setVisible(true);
                                     markerCluster.addMarker(markers[i]);
                                 } else {
                                     markers[i].setVisible(false);
                                     markerCluster.removeMarker(markers[i]);
                                 }
                                 markerCluster.redraw();
                             }
                         totalnumber+=number
                         }
                     }
                 }


                 else{
                     if (e=="all"){
                         if (f=="all") {
                             if(g=="all") { //Community Partner is selected
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['communitytest'] == 1) {number += 1}})
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
                             totalnumber+=number
                             }else {//Community Partner Type and Community PArtner is selected
                                 projectData.features.forEach(function (feature) {
                                     if ((feature.properties['Community Partner Type'] == g) && (feature.properties['communitytest'] == 1)) {
                                         number += 1
                                     }})
                                 for (var i = 0; i < markers.length; i++) {
                                     if ((markers[i].commType == g) && (markers[i].communityTest == 1)) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }
                         }
                         else {//Combination of Year Test , Community Partner Type and Community Partner
                             projectData.features.forEach(function (feature) {
                                 if ((feature.properties['Community Partner Type'] == g) && (feature.properties['communitytest'] == 1) && (feature.properties['yeartest']==1)) {
                                     number += 1
                                 }})
                             for (var i = 0; i < markers.length; i++) {
                                 if ((markers[i].commType == g) && (markers[i].communityTest == 1) && (markers[i].yearTest == 1)) {
                                     markers[i].setVisible(true);
                                     markerCluster.addMarker(markers[i]);
                                 } else {
                                     markers[i].setVisible(false);
                                     markerCluster.removeMarker(markers[i]);
                                 }
                                 markerCluster.redraw();
                             }
                         totalnumber+=number
                         }

                     }else {//Combination of Community Partner, Campus Partner, Community Partner Type and Academic Year
                         projectData.features.forEach(function (feature) {
                             if ((feature.properties['Community Partner Type'] == g) && (feature.properties['communitytest'] == 1) && (feature.properties['yeartest']==1) && (feature.properties['campustest']==1) ) {
                                 number += 1
                             }})
                         for (var i = 0; i < markers.length; i++) {
                             if ((markers[i].commType == g) && (markers[i].communityTest == 1) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1)) {
                                 markers[i].setVisible(true);
                                 markerCluster.addMarker(markers[i]);
                             } else {
                                 markers[i].setVisible(false);
                                 markerCluster.removeMarker(markers[i]);
                             }
                             markerCluster.redraw();
                         }
                     totalnumber+=number
                     }
                 }
             }
             else{
                 if (d=="all") {
                     if (e == "all") {
                         if (f=="all") {
                             if (g=="all") {//Legislative District is selected
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['Legislative District Number'] == c) {number += 1}})
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
                             totalnumber+=number
                             }
                             else { //Combination of Community Partner Type and Legislative District is selected
                                 projectData.features.forEach(function (feature) {
                                     if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Legislative District Number'] == c)) {
                                         number += 1
                                     }})
                                 for (var i = 0; i < markers.length; i++) {
                                     if ((markers[i].commType == g) && (markers[i].category == c)) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }
                         }
                         else { //Combination of Academic Year, Community Partner Type and Legislative District Number
                             projectData.features.forEach(function (feature) {
                                 if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Legislative District Number'] == c) && (feature.properties['yeartest'] == 1)) {
                                     number += 1
                                 }})
                             for (var i = 0; i < markers.length; i++) {
                                 if ((markers[i].commType == g) && (markers[i].category == c) && (markers[i].yearTest == 1)) {
                                     markers[i].setVisible(true);
                                     markerCluster.addMarker(markers[i]);
                                 } else {
                                     markers[i].setVisible(false);
                                     markerCluster.removeMarker(markers[i]);
                                 }
                                 markerCluster.redraw();
                             }
                         totalnumber+=number
                         }
                     }
                     else { //Combination of Academic year, Community Partner Type, Campus Partner and Legislative District Number
                         projectData.features.forEach(function (feature) {
                             if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Legislative District Number'] == c) && (feature.properties['yeartest'] == 1) && (feature.properties['campustest'] == 1)) {
                                 number += 1
                             }})
                         for (var i = 0; i < markers.length; i++) {
                             if ((markers[i].commType == g) && (markers[i].category == c) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1)) {
                                 markers[i].setVisible(true);
                                 markerCluster.addMarker(markers[i]);
                             } else {
                                 markers[i].setVisible(false);
                                 markerCluster.removeMarker(markers[i]);
                             }
                             markerCluster.redraw();
                         }
                     totalnumber+=number
                     }
                 }
                 else {//Combination of Community Partner, Campus PArtner,Community Partner Type, Academic Year and Legislative District Number
                     projectData.features.forEach(function (feature) {
                         if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Legislative District Number'] == c) && (feature.properties['yeartest'] == 1) && (feature.properties['campustest'] == 1) && (feature.properties['communitytest'] == 1)) {
                             number += 1
                         }})
                     for (var i = 0; i < markers.length; i++) {
                         if ((markers[i].commType == g) && (markers[i].category == c) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1) && (markers[i].communityTest == 1)) {
                             markers[i].setVisible(true);
                             markerCluster.addMarker(markers[i]);
                         } else {
                             markers[i].setVisible(false);
                             markerCluster.removeMarker(markers[i]);
                         }
                         markerCluster.redraw();
                     }
                 totalnumber+=number
                 }

             }
         }
         else {
             if (c="all") {
                 if ( d == "all") {
                     if (e == "all") {
                         if (f == "all") {
                             if (g == "all") { //Mission Area is selected
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['Mission Area'] == b) {number += 1}})
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
                             totalnumber+=number

                             }
                             else { // Community Partner Type and Mission area is selected
                                 projectData.features.forEach(function (feature) {
                                     if ((feature.properties['Mission Area'] == b) && (feature.properties['Community Partner Type'] == g))
                                     {number += 1}})
                                 for (var i = 0; i < markers.length; i++) {
                                     if ((markers[i].mission == b) && (markers[i].commType == g)) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number

                             }
                         }
                         else { //Academic Year, Community Partner Type and Mission area is selected
                             projectData.features.forEach(function (feature) {
                                 if ((feature.properties['Mission Area'] == b) && (feature.properties['Community Partner Type'] == g)&& (feature.properties['yeartest'] == 1))
                                 {number += 1}})
                             for (var i = 0; i < markers.length; i++) {
                                 if ((markers[i].mission == b) && (markers[i].commType == g) && (markers[i].yearTest == 1)) {
                                     markers[i].setVisible(true);
                                     markerCluster.addMarker(markers[i]);
                                 } else {
                                     markers[i].setVisible(false);
                                     markerCluster.removeMarker(markers[i]);
                                 }
                                 markerCluster.redraw();
                             }
                         totalnumber+=number
                         }
                     }
                     else {// Campus Partner, Academic Year, Community Partner Type and Mission area is selected
                         projectData.features.forEach(function (feature) {
                             if ((feature.properties['Mission Area'] == b) && (feature.properties['Community Partner Type'] == g)&& (feature.properties['yeartest'] == 1) &&  (feature.properties['campustest'] == 1))
                             {number += 1}})
                         for (var i = 0; i < markers.length; i++) {
                             if ((markers[i].mission == b) && (markers[i].commType == g) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1)) {
                                 markers[i].setVisible(true);
                                 markerCluster.addMarker(markers[i]);
                             } else {
                                 markers[i].setVisible(false);
                                 markerCluster.removeMarker(markers[i]);
                             }
                             markerCluster.redraw();
                         }
                     totalnumber+=number
                     }
                 }
                 else { // Community Partner, Campus Partner, Academic Year, Community Partner Type and Mission area is selected
                     projectData.features.forEach(function (feature) {
                         if ((feature.properties['Mission Area'] == b) && (feature.properties['Community Partner Type'] == g)&& (feature.properties['yeartest'] == 1) &&  (feature.properties['campustest'] == 1) && (feature.properties['communitytest'] == 1) )
                         {number += 1}})
                     for (var i = 0; i < markers.length; i++) {
                         if ((markers[i].mission == b) && (markers[i].commType == g) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1) && (markers[i].communityTest == 1)) {
                             markers[i].setVisible(true);
                             markerCluster.addMarker(markers[i]);
                         } else {
                             markers[i].setVisible(false);
                             markerCluster.removeMarker(markers[i]);
                         }
                         markerCluster.redraw();
                     }
                 totalnumber+=number
                 }
             }
             else { // Legislative District Number, Community Partner, Campus Partner, Academic Year, Community Partner Type and Mission area is selected
                 projectData.features.forEach(function (feature) {
                     if ((feature.properties['Mission Area'] == b) && (feature.properties['Community Partner Type'] == g)&& (feature.properties['yeartest'] == 1) &&  (feature.properties['campustest'] == 1) && (feature.properties['communitytest'] == 1)   && (feature.properties['Legislative District Number'] == c))
                     {number += 1}})
                 for (var i = 0; i < markers.length; i++) {
                     if ((markers[i].mission == b) && (markers[i].commType == g) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1) && (markers[i].communityTest == 1) && (markers[i].category == c)) {
                         markers[i].setVisible(true);
                         markerCluster.addMarker(markers[i]);
                     } else {
                         markers[i].setVisible(false);
                         markerCluster.removeMarker(markers[i]);
                     }
                     markerCluster.redraw();
                 }
             totalnumber+=number
             }

         }
     }
     else{
         if (b="all") {
             if (c="all") {
                 if (d="all") {
                     if (e="all") {
                         if (f="all") {
                             if (g="all") {//Engagement Type is Selected
                                 projectData.features.forEach(function (feature) {
                                     if (feature.properties['Engagement Type'] == a) {number += 1}})
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
                             totalnumber+=number
                             }
                             else{// Combination of Community Partner Type and Engagement Type is Selected
                                 projectData.features.forEach(function (feature) {
                                     if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Engagement Type'] == a)) {
                                         number += 1
                                     }})
                                 for (var i = 0; i < markers.length; i++) {
                                     if ((markers[i].commType == g) && (markers[i].engagementType == a)) {
                                         markers[i].setVisible(true);
                                         markerCluster.addMarker(markers[i]);
                                     } else {
                                         markers[i].setVisible(false);
                                         markerCluster.removeMarker(markers[i]);
                                     }
                                     markerCluster.redraw();
                                 }
                             totalnumber+=number
                             }

                         }
                         else {// Academic Year, Combination of Community Partner Type and Engagement Type is Selected
                             projectData.features.forEach(function (feature) {
                                 if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Engagement Type'] == a) && (feature.properties['yeartest'] == 1) ) {
                                     number += 1
                                 }})
                             for (var i = 0; i < markers.length; i++) {
                                 if ((markers[i].commType == g) && (markers[i].engagementType == a) && (markers[i].yearTest == 1)) {
                                     markers[i].setVisible(true);
                                     markerCluster.addMarker(markers[i]);
                                 } else {
                                     markers[i].setVisible(false);
                                     markerCluster.removeMarker(markers[i]);
                                 }
                                 markerCluster.redraw();
                             }
                         totalnumber+=number
                         }
                     }
                     else{// Campus Partner, Academic Year, Combination of Community Partner Type and Engagement Type is Selected
                         projectData.features.forEach(function (feature) {
                             if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Engagement Type'] == a) && (feature.properties['yeartest'] == 1) && (feature.properties['campustest'] == 1) ) {
                                 number += 1
                             }})
                         for (var i = 0; i < markers.length; i++) {
                             if ((markers[i].commType == g) && (markers[i].engagementType == a) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1)) {
                                 markers[i].setVisible(true);
                                 markerCluster.addMarker(markers[i]);
                             } else {
                                 markers[i].setVisible(false);
                                 markerCluster.removeMarker(markers[i]);
                             }
                             markerCluster.redraw();
                         }
                     totalnumber+=number
                     }

                 }
                 else{// Community Partner, Campus Partner, Academic Year, Combination of Community Partner Type and Engagement Type is Selected
                     projectData.features.forEach(function (feature) {
                         if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Engagement Type'] == a) && (feature.properties['yeartest'] == 1) && (feature.properties['campustest'] == 1) && (feature.properties['communitytest'] == 1) ) {
                             number += 1
                         }})
                     for (var i = 0; i < markers.length; i++) {
                         if ((markers[i].commType == g) && (markers[i].engagementType == a) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1) && (markers[i].communityTest == 1)) {
                             markers[i].setVisible(true);
                             markerCluster.addMarker(markers[i]);
                         } else {
                             markers[i].setVisible(false);
                             markerCluster.removeMarker(markers[i]);
                         }
                         markerCluster.redraw();
                     }
                 totalnumber+=number
                 }

             }
             else{//  Legislative District, Community Partner, Campus Partner, Academic Year, Combination of Community Partner Type and Engagement Type is Selected

                 projectData.features.forEach(function (feature) {
                     if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Engagement Type'] == a) && (feature.properties['yeartest'] == 1) && (feature.properties['campustest'] == 1) && (feature.properties['communitytest'] == 1) && (feature.properties['Legislative District Number'] == c) ) {
                         number += 1
                     }})
                 for (var i = 0; i < markers.length; i++) {
                     if ((markers[i].commType == g) && (markers[i].engagementType == a) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1) && (markers[i].communityTest == 1) && (markers[i].category == c)) {
                         markers[i].setVisible(true);
                         markerCluster.addMarker(markers[i]);
                     } else {
                         markers[i].setVisible(false);
                         markerCluster.removeMarker(markers[i]);
                     }
                     markerCluster.redraw();
                 }
             totalnumber+=number
             }

         }
         else{// Mission Area, Legislative District, Community Partner, Campus Partner, Academic Year, Combination of Community Partner Type and Engagement Type is Selected
             projectData.features.forEach(function (feature) {
                 if ((feature.properties['Community Partner Type'] == g) && (feature.properties['Engagement Type'] == a) && (feature.properties['yeartest'] == 1) && (feature.properties['campustest'] == 1) && (feature.properties['communitytest'] == 1) && (feature.properties['Legislative District Number'] == c) && (feature.properties['Mission Area'] == b)) {
                     number += 1
                 }})
             for (var i = 0; i < markers.length; i++) {
                 if ((markers[i].commType == g) && (markers[i].engagementType == a) && (markers[i].yearTest == 1) && (markers[i].campusTest == 1) && (markers[i].communityTest == 1) && (markers[i].category == c) && (markers[i].mission == b)) {
                     markers[i].setVisible(true);
                     markerCluster.addMarker(markers[i]);
                 } else {
                     markers[i].setVisible(false);
                     markerCluster.removeMarker(markers[i]);
                 }
                 markerCluster.redraw();
             }
         totalnumber+=number

         }

     }

        $('#totalnumber').html(totalnumber);
    }

