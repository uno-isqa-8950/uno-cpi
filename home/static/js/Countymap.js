mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var colorcode = ['#17f3d1','#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00']
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
// function onlyUnique(value, index, self) {
//     return self.indexOf(value) === index;
// }

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-95.957309, 41.276479],
    // initial zoom
    zoom: 6
});


// var select = '';
// select += '<a href="#" ' + 'id='+'"all"><span style="background-color: black"></span><b>All Mission Areas</b></a>' + "<br>";
// for (var i=1;i<=Missionarea.length;i++){
//     var color = colorcode[i]
//     var mission = Missionarea[i]
//     select += '<a href="#"'  + 'id=' +
//         'valueOf(mission)><span style="background-color: color"></span>'+'<b>mission</b></a>' + "<br>";
// }
// $('#legend').html(select);




map.addControl(new mapboxgl.NavigationControl());
var countyData = JSON.parse(document.getElementById('county-data').textContent);

var popup = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: true,
});
var formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
});





function parseDescription(message) {
    var string = "";

    for (var i in message) {


        if (i == "CommunityPartner") {
            string += '<span style="font-weight:bold">' + 'Community Partner' + '</span>' + ": " + message[i] + "<br>";
        }if (i == "K-12 Partner") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i =="Address"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i =="Mission Area"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "City"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "  ";
        } else if (i == "State"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "Website"){
            var website = message[i];
            var base = "http://";
            if (!website.includes("http")){
                website = base.concat(website);
            }
            string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${i}</a><br>`;
        } else if (i == "STATE"){
            string += '<span style="font-weight:bold">' + 'State' + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "NAME"){
            string += '<span style="font-weight:bold">' + 'County' + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "Income"){
            if (message[i] != 0){
                string += '<span style="font-weight:bold">' + 'Household Income' + '</span>' + ": " + formatter.format(message[i]) + "<br>";
            }
        } else if (i=="income"){
            if (message[i] != 0){
                string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + formatter.format(message[i]) + "<br>"
            }
        } else if (i=="County"){
            if (message[i] !== null && message[i] !== "N/A"){
                string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + message[i] + "<br>"
            }
        } else if (i=="Legislative District Number"){
            if (message[i] !== 0){
                string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + message[i] + "<br>"
            }
        }  else if (i == "CommunityType"){
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        }
    }
    return string;
};

map.on("load",function() {

    map.addSource('communityData', {
        type: 'geojson',
        data: communityData,
    });
    map.addSource('countyData', {
            type: 'geojson',
            data: countyData,
    });
    map.addLayer({
            "id": "county",
            "type": "fill",
            "source": "countyData",
            'paint': {
                "fill-color": "#888",
                "fill-opacity": ["case",
                    ["boolean", ["feature-state", "hover"], false],
                    1,
                    0.3
                ],
                "fill-outline-color": "#0000AA"
            }
    });
    communityData.features.forEach(function(feature) {
        var primary = feature.properties["Mission Area"];
        var commType = feature.properties["CommunityType"]
        var base = "show"
        for (var i = 0; i < Missionarea.length; i++) {
            if (primary == Missionarea[i]) {
                layerID = base + (i + 1);
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "circle",
                        "source": "communityData",
                        "paint": {
                            "circle-radius": 8,
                            "circle-opacity": 1,
                            "circle-color": colorcode[i],
                        },
                        "filter": ["all",["==", "Mission Area", primary]]
                    })
                }
            }
        }
    });

    map.on("click", "show1", function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show2", function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show3", function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show4", function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show5", function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show6", function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });

   var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function(e) {
        var value = e.target.value.trim();
        if (value == "alltypes") {
            for (var i = 0; i<= CommunityType.length; i++){
                if(value==CommunityType[i]){
                    map.setFilter("show1", ["all", ["==", "Mission Area", Missionarea[0]],
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show2", ["all", ["==", "Mission Area", Missionarea[1]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show3", ["all", ["==", "Mission Area", Missionarea[2]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show4", ["all", ["==", "Mission Area", Missionarea[3]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show5", ["all", ["==", "Mission Area", Missionarea[4]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show6", ["all", ["==", "Mission Area", Missionarea[5]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                }
            }

        } else {
            for (var i = 0; i<= CommunityType.length; i++){
                if(value==CommunityType[i]){
                    map.setFilter("show1", ["all", ["==", "Mission Area", Missionarea[0]],
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show2", ["all", ["==", "Mission Area", Missionarea[1]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show3", ["all", ["==", "Mission Area", Missionarea[2]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show4", ["all", ["==", "Mission Area", Missionarea[3]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show5", ["all", ["==", "Mission Area", Missionarea[4]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                    map.setFilter("show6", ["all", ["==", "Mission Area", Missionarea[5]]
                        ["==", "CommunityType", CommunityType[i]]]
                    )
                }
            }
        }
    })

})
