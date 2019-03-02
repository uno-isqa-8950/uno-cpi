// mapboxgl.accessToken = 'pk.eyJ1IjoidmJoYXRob3NtYXQiLCJhIjoiY2pyNGc5MzNzMDNvZTQ1bzIxcmJ5ejJhayJ9.lMH6o8Nk36qm3lG3M0apdQ';
var projectData = JSON.parse(document.getElementById('project-data').textContent); //load the variable from views.py. See the line from html first
var districtData = JSON.parse(document.getElementById('district').textContent); //load the variable from views.py. See the line from html first
var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
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
select1 += '<option val=' + "all" + '>' + "All District" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);


// function parseDescription(message) {
//     var string = "";
//
//     for (var i in message) {
//         if (message[i] != null && message[i] != 0 && message[i] != "" && message[i] != []){
//             if (i == "Address Line1") {
//                 string += '<span style="font-weight:bold">' + "Address" + '</span>' + ": " + message[i] + "<br>";
//             } else if (i == "Address") {
//                 string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
//             }
//         }
//     }
//     return string;
// };
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
function getColor(d) {
    return d > 100 ? '#8c2d04' :
        d > 50  ? '#cc4c02' :
            d > 30  ? '#ec7014' :
                d > 20  ? '#fe9929' :
                    d > 10   ? '#fec44f' :
                        d > 5   ? '#fee391' :
                            d > 1   ? '#fff7bc' :
                                '#ffffe5';
}

google.maps.event.addListenerOnce(map, 'idle', function () {
    map.data.add('projectData', {
        type: 'geojson',
        data: projectData,
    });
    map.data.add('districtData', {
        type: 'geojson',
        data: districtData,
    });
    //*********************************** Load the county in different household income levels *****************************************************
    districtData.features.forEach(function (feature) {
        var symbol = feature.properties['id'];
        var layerID = 'poi-' + symbol;
        var density = feature.properties['density']
        if (!map.data.getFeatureById(layerID)) {
            map.data.add({
                "id": layerID,
                "type": "fill",
                "source": "districtData",
                'layout': {},
                'paint': {
                    "fill-color": getColor(density),
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
        fillColor: 'blue',
        fillOpacity: .7,
        strokeOpacity: 0.9,
        scale: 8,
        strokeColor: 'white',
        strokeWeight: 1.5
    };

    // contents of the infowindow
    // var contentString =
    var proj_name = projectData.features
    var miss_name = projectData.features
    console.log(projectData.features.properties)
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
        attachMessage(marker, proj_name[i].properties['Project Name'],miss_name[i].properties['Mission Area']);
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
        url: "https://googlemaps.github.io/js-marker-clusterer/images/m1.png",
        width: 53
    },
    {
        height: 56,
        url: "https://googlemaps.github.io/js-marker-clusterer/images/m1.png",
        width: 56
    },
    {
        height: 66,
        url: "https://googlemaps.github.io/js-marker-clusterer/images/m1.png",
        width: 66
    },
    {
        height: 78,
        url: "https://googlemaps.github.io/js-marker-clusterer/images/m1.png",
        width: 78
    },
    {
        height: 90,
        url: "https://googlemaps.github.io/js-marker-clusterer/images/m1.png",
        width: 90
    }]
};



// function to call the infowindow on clicking markers
function attachMessage(marker, projectName, missionArea) {
    var infowindow = new google.maps.InfoWindow({
        content: '<tr><td><span style="font-weight:bold">Project Name:</span>&nbsp;&nbsp; </td><td>' + projectName + '</td></tr><br />' +
            '<tr><td><span style="font-weight:bold">Mission Area: </span>&nbsp </td><td>' + missionArea + '</td></tr>'
    });
    //listner to check for on click event
    marker.addListener('click', function() {
        infowindow.open(marker.get('map'), marker);
        //time out after which the info window will close
        setTimeout(function () { infowindow.close(); }, 5000);
    });
}

var selectDistrict = document.getElementById('selectDistrict');
selectDistrict.addEventListener("change", function(e) {
    var value = e.target.value.trim().toLowerCase();
    console.log(value)
    for (j = 1; j < districtData.features.length; j++)
        if (districtData.features[j].id == value)
            map.setCenter({lat:41.4925, lng:-99.9018});
            map.setZoom(7);

})



