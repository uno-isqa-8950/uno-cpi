
mapboxgl.accessToken = 'pk.eyJ1IjoidW5vY3BpZGV2dGVhbSIsImEiOiJjanJiZTk2cjkwNjZ5M3l0OGNlNWZqYm91In0.vPmkC3MFDrTlBk-ntUFruA';
var projectData = JSON.parse(document.getElementById('project-data').textContent); //load the variable from views.py. See the line from html first
var districtData = JSON.parse(document.getElementById('district').textContent); //load the variable from views.py. See the line from html first
var layerIDs = []; // Will contain a list used to filter against. This is for filtering Legislative Districts
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

//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option val=' + "all" + '>' + "All District" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);


function parseDescription(message) {
    var string = "";

    for (var i in message) {
        if (message[i] != null && message[i] != 0 && message[i] != "" && message[i] != []){
            if (i == "Address Line1") {
                string += '<span style="font-weight:bold">' + "Address" + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Address") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            }
        }
    }
    return string;
};
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
map.on("load", function() {

    map.addSource('projectData', {
        type: 'geojson',
        data: projectData,
    });
    map.addSource('districtData', {
        type: 'geojson',
        data: districtData,
    });
    //*********************************** Load the county in different household income levels *****************************************************

    districtData.features.forEach(function (feature) {
        var symbol = feature.properties['id'];
        var layerID = 'poi-' + symbol;
        var density = feature.properties['density']
        if (!map.getLayer(layerID)) {
            map.addLayer({
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
    map.addLayer({
        "id": "district",
        "type": "fill",
        "source": "districtData",
        'layout': {},
        'paint': {
            "fill-color": "#888",
            "fill-opacity": 0,
            "fill-outline-color": '#3c341f'
        }
    });

    map.addLayer({
        "id": "projectmap",
        "type": "circle",
        "source": "projectData",
        'layout': {},
        'paint': {
            "circle-radius": 8,
            "circle-opacity": 1,
            "circle-color": '#1743f3',
        }
    });

    map.on('click', 'projectmap', function(e) {
        var address = e.features[0].properties["Address Line1"];
        var number = 0;
        projectData.features.forEach(function(feature){
            var check = feature.properties["Address Line1"]
            if (check == address){
                number += 1
            }
        })
        popup.setLngLat(e.lngLat)
            // .setHTML('<span style="font-weight:bold">' + "Address" + '</span>' + ": " + address + ", there have been " + number + " projects")
            .setHTML('<tr><td><span style="font-weight:bold">Address: </span></td><td>' + address + '</td></tr><br />' +
                    '<tr><td><span style="font-weight:bold">Number of projects: </span></td><td>' + number + '</td></tr>')
            .addTo(map);
    });

    var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function(e) {
        var value = e.target.value.trim().toLowerCase();
        console.log(value)
        if (isNaN(value)) {
            // get the number of markers that fit the requirement and show on the HTML
            map.setFilter("projectmap", null);
            layerIDs.forEach(function(layerID) {
                map.setLayoutProperty(layerID, 'visibility', 'visible');
            })
        } else {
            layerIDs.forEach(function (layerID) {
                map.setLayoutProperty(layerID, 'visibility',
                    (layerID.indexOf(value) == 4) && (layerID.length == (value.length + 4)) ? 'visible' : 'none');
            })
        }
    })
})