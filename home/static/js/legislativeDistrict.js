//*********************************** Get mapbox API and get data from HTML *****************************************************

var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var districtData = JSON.parse(document.getElementById('district-data').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CollegeName = JSON.parse(document.getElementById('college-list').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);

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
select += '<a href="#" ' + 'id=' + '"All Focus Areas" ' + 'class="selectMission"' + 'value="' + 'All Focus Areas"' + 'onclick="filterData(this.id, true)"'+'><span style="background-color: #ffffff; border: 1px solid black"></span><b>All Focus Areas</b></a>' + "<br>";
for (var i = 0; i < Missionarea.length; i++) {
    var mission = Missionarea[i];
    var missionName = mission.split(':')[0];
    var missionColor = mission.split(':')[1];
    var color = missionColor;
    select += `<a href="#"  id="${missionName.valueOf()}" class="selectMission" value="${missionName.valueOf()}"  onclick="filterData(this.id, true)"><span style="background-color: ${color}"></span><b>${missionName.toString()}</b></a>` + "<br>";
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
   
   partnerGoogleMapfn(communityData);

   map.data.loadGeoJson('../../static/GEOJSON/ID3.geojson')


   map.data.setStyle({
       fillColor: "#fee8c8",
       fillOpacity: 0.4,
       strokeWeight: 0.2
    })
});


function partnerGoogleMapfn(modifiedcommunityData){

    map.data.add('communityData', {
        type: 'geojson',
        data: modifiedcommunityData,
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
    
    for (i=0; i<modifiedcommunityData.features.length; i++) {
        if(modifiedcommunityData.features[i] != '' 
            && modifiedcommunityData.features[i] !=null 
            && modifiedcommunityData.features[i] != undefined){
        var communityType = modifiedcommunityData.features[i].properties["CommunityType"]
        var commMission = modifiedcommunityData.features[i].properties["Mission Area"]
        var commPartnerName = modifiedcommunityData.features[i].properties["CommunityPartner"]
        var projectCount = modifiedcommunityData.features[i].properties["Number of projects"]
        var cecStatus = modifiedcommunityData.features[i].properties["Community CEC Status"]
        var website = modifiedcommunityData.features[i].properties["Website"]
        var city = modifiedcommunityData.features[i].properties["City"]
        var academicYrs = modifiedcommunityData.features[i].properties["Academic Year"]
        var campusPartners = modifiedcommunityData.features[i].properties["Campus Partner"]
        var commProjects = modifiedcommunityData.features[i].communityprojects
        var marker = new google.maps.Marker({
            position: {
                lat: parseFloat(modifiedcommunityData.features[i].geometry.coordinates[1])+ (Math.random() -.5) / 25000,
                lng: parseFloat(modifiedcommunityData.features[i].geometry.coordinates[0])+ (Math.random() -.5) / 25000
            },
            map: map,
            icon: circle, // set the icon here
            fillColor: missionColor(commMission),
            
        });
        oms.addMarker(marker);
       function missionColor(mission) {
        var assignColor = '';
            for (var i = 0; i < Missionarea.length; i++) {
                var missiondtl = Missionarea[i];
                var missionName = missiondtl.split(':')[0];
                var missionColor = missiondtl.split(':')[1];
                if(mission == missionName){
                    assignColor = missionColor;
                }
            }
            return circle.fillColor = assignColor;
        }
         // contents of the infowindow
        attachMessage(marker, commPartnerName, projectCount,city,
            commMission, communityType,academicYrs,website,commProjects,cecStatus,campusPartners);
        markers.push(marker)
    }
    }
     markerCluster = new MarkerClusterer(map, markers,mcOptions);
}

var mcOptions = {
    maxZoom: 15,
    minimumClusterSize: 10, //minimum number of points before which it should be clustered
    averageCenter: true,
    styles: [{
        height: 53,
        url: "https://unocpi.s3.us-east-2.amazonaws.com/cluster_images/m2.png",
        width: 53
    },
        {
            height: 56,
            url: "https://unocpi.s3.us-east-2.amazonaws.com/cluster_images/m2.png",
            width: 56
        },
        {
            height: 60,
            url: "https://unocpi.s3.us-east-2.amazonaws.com/cluster_images/m2.png",
            width: 60
        },
        {
            height: 80,
            url: "https://unocpi.s3.us-east-2.amazonaws.com/cluster_images/m2.png",
            width: 80
        },
        {
            height: 100,
            url: "https://unocpi.s3.us-east-2.amazonaws.com/cluster_images/m2.png",
            width: 100
        }]
};

var openedInfoWindow = null;
var rightclickwindow = null;

// function to call the infowindow on clicking markers

function attachMessage(marker, partner_name,project_number,city,miss_name, comm_name, academic_year,website,projects,commCecStatus,campusPartners) {
    var infowindow = new google.maps.InfoWindow();
    google.maps.event.addListener(marker, 'click', function () {
       var commInnerHtml = '';
       var commBodyHtml = '';
       var commCecHtml = '';
       var campusPartersVal = ''
       var acasdemicYrVal = ''
       if (campusPartners !=null && campusPartners !=''){
            campusPartersVal = campusPartners.join(" | ")
       }
        if (academic_year !=null && academic_year !=''){
            acasdemicYrVal = academic_year.join(" | ")
       }
 
       var commHeadHtml ='<tr><td style="margin-top: 5%"><span style="font-weight:bold">Community Partner:</span>&nbsp;&nbsp; </td><td>' + partner_name +'</td></tr><br />'+
                         '<tr><td><span style="font-weight:bold">Total Number of Projects: </span>&nbsp; </td><td>' + project_number + '</td></tr><br />' +
                        '<tr><td><span style="font-weight:bold">City: </span>&nbsp; </td><td>' + city + '</td></tr><br />' +
                        '<tr><td><span style="font-weight:bold">Focus Areas: </span>&nbsp; </td><td>' + miss_name + '&nbsp;&nbsp;</td></tr><br />' +
                        '<tr><td><span style="font-weight:bold">Community Partner Type:</span>&nbsp;&nbsp; </td><td>' + comm_name + '&nbsp;&nbsp;</td></tr><br />' +
                        '<tr><td><span style="font-weight:bold">Campus Partner: </span>&nbsp; </td><td>' + campusPartersVal + '&nbsp;&nbsp;</td></tr><br />' +
                        '<tr><td><span style="font-weight:bold">Academic Year: </span>&nbsp; </td><td>' + acasdemicYrVal  + '&nbsp;&nbsp;</td></tr><br />' +
                        '<tr><td><span style="font-weight:bold">Website Link: </span>&nbsp;<a id="websitelink" href="' + website + '" target="_blank" style="color:#FF0000;">' + website + '</a></td></tr><br /><br>';
                        
        if(commCecStatus == 'Current'){
            commCecHtml ='<tr><td><span style="font-weight:bold">'+commCecStatus +' CEC Building Partner - </span>&nbsp; </td><td><span style="font-weight:bold">'+ partner_name +'</span> is a <a id="websitelink" href="https://www.unomaha.edu/community-engagement-center/index.php" target="_blank" style="color:#FF0000;">Barbara Weitz Community Engagement Center </a> (CEC) building partner. '+
                        'The CEC bridges the campus and community by housing UNO and community partners in the building.</td></tr></br></br>';
        }
        if(commCecStatus == 'Former'){
         commCecHtml ='<tr><td><span style="font-weight:bold">'+commCecStatus +' CEC Building Partner - </span>&nbsp; </td><td><span style="font-weight:bold">'+ partner_name +'</span> has been a <a id="websitelink" href="https://www.unomaha.edu/community-engagement-center/index.php" target="_blank" style="color:#FF0000;">Barbara Weitz Community Engagement Center </a> (CEC) building partner. '+
                        'The CEC bridges the campus and community by housing UNO and community partners in the building.</td></tr></br></br>';
        }
                        
        if(project_number != 0 ){
            commBodyHtml +='<tr style="margin-top: 5%"><td><span style="font-weight:lighter">Right-click on the marker to see the list of projects</span></td></tr>';
        }
        commInnerHtml = commHeadHtml + commCecHtml + commBodyHtml;

        if (openedInfoWindow != null) openedInfoWindow.close();  // <-- changed this
        infowindow.setContent(commInnerHtml);
        infowindow.open(map, marker);
        // map.setZoom(16);
        map.panTo(this.getPosition());
        // added next 4 lines
        openedInfoWindow = infowindow;
        google.maps.event.addListener(infowindow, 'closeclick', function () {
            openedInfoWindow = null;
        });
    });
    google.maps.event.addListener(marker, 'rightclick', function() {
         var projectHtml = ''
         var projHeadHtml =  '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Community Partner:</span>&nbsp;&nbsp; </td><td>' + partner_name + '</td></tr><br />' +
            //'<tr><td style="margin-top: 5%"><span style="font-weight:bold">Projects:</span>&nbsp;&nbsp; </td><td>' + projects.join("<br>").replace(/\s*\(.*?\)\s*/g,"")+ '</td></tr><br />')
        '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Projects:</span></td></tr><br />' + 
        '<tr><td style="margin-top: 5%">'+
        '<table border="1"><tr>'+
        '<td><span style="font-weight:bold">&nbsp;Academic Year&nbsp;</span></td>'+
        '<td><span style="font-weight:bold">&nbsp;Name&nbsp;</span></td>'+
        '<td><span style="font-weight:bold">&nbsp;Engagement Type&nbsp;</span></td></tr>';
        var projInnerHtml = ''

        for(var i=0;i<projects.length;i++){
            var projFullName = projects[i]["name"];
            var projName = '';
            var projAcademicyr = '';
            var projdetail = projFullName.split(';');
            if (projdetail !=null){ 
                    projName = projdetail[0];
                    projAcademicyr = projdetail[1];
            }

            if(projName != '' && projName != null){
                projName = projName.replace(/\s*\(.*?\)\s*/g,"");
            }
            var projEngType = projects[i]["engagementType"];
            if(projEngType != '' && projEngType != null){
                projEngType = projEngType.replace(/\s*\(.*?\)\s*/g,"");
            }
            projInnerHtml += '<tr><td><span>&nbsp;'+projAcademicyr+'&nbsp;</span></td>'+
        '<td><span>&nbsp;'+projName+'&nbsp;</span></td>'+
        '<td><span >&nbsp;'+projEngType+'&nbsp;</span></td></tr>';
        }
        projectHtml = projHeadHtml + projInnerHtml +'</table></td></tr>';
        infowindow.setContent(projectHtml)
         // '<tr><td style="margin-top: 5%"><span style="font-weight:bold">Projects:</span>&nbsp;&nbsp; </td><td>' + projects.toString().split(",").join("<br>")+ '</td></tr><br />')
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

// Get the size of cluster in the current state
function getClusterSize() {
    return markerCluster.getMarkers().length;
}

function filterData(selectedField, selectType){
    var missionObjval = 'All Focus Areas';
    if (selectType != '' && selectType == true){
        missionObjval = selectedField
    }

    var campusObj = document.getElementById('selectCampus');
    var collegeObj = document.getElementById('selectCollege');
    var communityObj = document.getElementById('selectCommtype');
    var yearObj = document.getElementById('selectYear');
    var legDistrictObj = document.getElementById('selectDistrict');
    var inputCommunity = document.getElementById('valueFilter');

    var commObjVal = communityObj.options[communityObj.selectedIndex].value;
    var campusObjVal = campusObj.options[campusObj.selectedIndex].value;
    var collegeObjval = collegeObj.options[collegeObj.selectedIndex].text;
    var yearObjVal = yearObj.options[yearObj.selectedIndex].value;
    var legisDistVal = legDistrictObj.options[legDistrictObj.selectedIndex].value;
    var inputCommunityVal = inputCommunity.value;
    if (inputCommunityVal != ''){
        inputCommunityVal.trim().toLowerCase();
    }

    if (selectedField == 'selectCollege'){
        var select3 = '';
        select3 += '<option value="' + "All Campus Partners" + '" selected="selected">' + 'All Campus Partners' + '</option>';
        for (i = 0; i < CampusPartnerlist.length; i++) {
            if(CampusPartnerlist[i].c_id == collegeObjval || collegeObjval == 'All Colleges and Main Units')
                select3 += '<option value= "' + CampusPartnerlist[i].name + '">' + CampusPartnerlist[i].name + '</option>';
        }
        $('#selectCampus').html(select3);
    }
    if (selectedField =='selectDistrict'){
        // redrawLegislativemap(legisDistVal);
    }
    //alert('collegeObjval---'+collegeObjval);
    //alert('campusObjVal---'+campusObjVal);
    var filteredCommunitydata = getMapFilteredData(communityData,missionObjval,commObjVal,legisDistVal,yearObjVal,collegeObjval,campusObjVal,inputCommunityVal);
    resetPartnerMarkers(filteredCommunitydata);
}

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
            if (value == districtData.features[i].properties["DISTRICT"]) {
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

function getMapFilteredData (communityPartners, mission_value ,comm_type, legislative_value, academic_year, college_name, campus_partner, search) {
    var updatedCommunityPartners = JSON.parse(JSON.stringify(communityPartners));
    var updated_CommunityPartners = updatedCommunityPartners.features;
    
    var not_set = [undefined, "All", '', 'All Focus Areas', 'All Community Partner Types', 'All Colleges and Main Units', 'All Campus Partners', 'All Legislative Districts', 'All Academic Years'];
    if (!not_set.includes(mission_value)) {
        var updated_CommunityPartners = updated_CommunityPartners.filter(d => d.properties["Mission Area"] == mission_value);
    }
    if (!not_set.includes(comm_type)) {
        var updated_CommunityPartners = updated_CommunityPartners.filter(d => d.properties.CommunityType == comm_type);
    }
    if (!not_set.includes(legislative_value)) {
        var updated_CommunityPartners = updated_CommunityPartners.filter(d => d.properties["Legislative District Number"] == legislative_value);
    }
    if (!not_set.includes(search)) {
        var updated_CommunityPartners = updated_CommunityPartners.filter(d => d.properties.CommunityPartner.toLowerCase().includes(search));
    }
    
    var indexList = new Set();
    if (!not_set.includes(academic_year)) {
        updated_CommunityPartners.forEach(function(feature, index, object) {
            var Projects = feature["communityprojects"].filter(d => d.academicYear.includes(academic_year));
            if (Projects.length == 0) {indexList.add(index);}
            feature["communityprojects"] = Projects;
        });
    }
    if (!not_set.includes(college_name)) {
        updated_CommunityPartners.forEach(function(feature, index, object) {
            var Projects = feature["communityprojects"].filter(d => d.collegeNames.includes(college_name));
            if (Projects.length == 0) {indexList.add(index);}
            feature["communityprojects"] = Projects;
        });
    }
    if (!not_set.includes(campus_partner)) {
        updated_CommunityPartners.forEach(function(feature, index, object) {
            var Projects = feature["communityprojects"].filter(d => d.campuspartner.includes(campus_partner));
            if (Projects.length == 0) {indexList.add(index);}
            feature["communityprojects"] = Projects;
        });
    }

    if (!not_set.includes(academic_year) || !not_set.includes(college_name) || !not_set.includes(campus_partner)) {
        let keys = Object.keys(updated_CommunityPartners);
        var indexList = Array.from(indexList).sort();        
        for (i in indexList) {
            delete updated_CommunityPartners[keys[indexList[i]]];
        }
    }
    var filteredCommunityKeys = Object.keys(updated_CommunityPartners);
    if (filteredCommunityKeys.length > 0){
        return { "type": "FeatureCollection", "features":updated_CommunityPartners};
    }else{
        return null;
    }
}

function resetPartnerMarkers(modifiedCommPartnerObj){ 
    oms.clearMarkers();
    markerCluster.clearMarkers();
    markers = [];
     if(modifiedCommPartnerObj != null){
        partnerGoogleMapfn(modifiedCommPartnerObj);
        markerCluster.redraw();
        $('#totalnumber').html(getClusterSize());
     }else{
        $('#totalnumber').html(0);
     }
    }

$("#reset").click(function () {
    document.getElementById("valueFilter").value = '';
    document.getElementById('selectCollege').selectedIndex=0;
    document.getElementById('selectCommtype').selectedIndex=0;
    document.getElementById('selectYear').selectedIndex=0;
    document.getElementById('selectDistrict').selectedIndex=0;

    var select3 = '';
    select3 += '<option value="' + "All Campus Partners" + '" selected="selected">' + 'All Campus Partners' + '</option>';
    for (i = 0; i < CampusPartnerlist.length; i++) {
        select3 += '<option value= "' + CampusPartnerlist[i].name + '">' + CampusPartnerlist[i].name + '</option>';
    }
    $('#selectCampus').html(select3);
    resetPartnerMarkers(communityData)
});