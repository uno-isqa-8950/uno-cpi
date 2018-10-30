mapboxgl.accessToken = 'pk.eyJ1IjoibWluaGR1b25nMjQzIiwiYSI6ImNqbHNvM3l0cTAxaXMzcHBiYnpvNjBsaXAifQ.NO598_UKYbyOIok45baiWA';
// This adds the map to your page
if (!('remove' in Element.prototype)) {
    Element.prototype.remove = function() {
        if (this.parentNode) {
            this.parentNode.removeChild(this);
        }
    };
}

var layerIDs = [];
var hoveredStateId = null;
var map = new mapboxgl.Map({
    // container id specified in the HTML
    container: 'map',
    // style URL
    style: 'mapbox://styles/mapbox/light-v9',
    // initial position in [lon, lat] format
    center: [-95.957309, 41.276479],
    // initial zoom
    zoom: 12
});

var popup = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: true
});
//******************************Create content for the popups**********************************
function parseDescription(message) {
    var string = ""


    for (var i in message) {

        if (i == "PhoneNumber") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        } else if (i == "Website") {
            var website = message[i];
            var base = "http://";
            if (website === null || website == "null" || website == "") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (!website.includes("http")) {
                website = base.concat(website);
                string += `<span style="font-weight:bold">${i}</span>:<a target="_blank" href="${website}" class="popup">${website}</a><br>`;
            } else {
                string += `<span style="font-weight:bold">${i}</span>:<a target="_blank" href="${website}" class="popup">${website}</a><br>`;
            }
        } else if (i == "Address") {
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>"
        }
    }
    return string;
}
//******************************Load data and put it on the map**********************************
var districtData = "";
var k12Datas = "";

$.get("static/GEOJSON//K-12Partners.geojson", function(data) { //load JSON file from static/GEOJSON
    k12Datas = jQuery.parseJSON(data);
})
$.get("static/GEOJSON/ID2.geojson", function(data) { //load JSON file from static/GEOJSON
    districtData = jQuery.parseJSON(data);
})
map.addControl(new mapboxgl.NavigationControl());
map.on('load', function(e) {

    map.addSource("k12Datas", {
        type: "geojson",
        data: k12Datas,
    });
    map.addSource('districtData', {
        type: 'geojson',
        data: districtData,
    });
    districtData.features.forEach(function(feature) {
        var symbol = feature.properties['id'];
        var layerID = 'poi-' + symbol;

        if (!map.getLayer(layerID)) {
            map.addLayer({
                "id": layerID,
                "type": "fill",
                "source": "districtData",
                'layout': {},
                'paint': {
                    "fill-color": "#888",
                    "fill-opacity": ["case",
                        ["boolean", ["feature-state", "hover"], false],
                        1,
                        0.4
                    ],
                    "fill-outline-color": "#0000AA"
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
            "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                1,
                0.08
            ],
            "fill-outline-color": "#0000AA"
        }
    });

    // Add the data to your map as a layer
    k12Datas.features.forEach(function(feature) {
        var level = feature.properties["Level"];

        if (level == "Elementary") {
            layerID = "show1";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "k12Datas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#2A0A12'
                    },
                    "filter": ["all", ["==", "Level", "Elementary"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "Fall 2017"]
                    ]
                })
            }
        } else if (level == "Secondary") {
            layerID = "show2";
            if (!map.getLayer(layerID)) {
                map.addLayer({
                    "id": layerID,
                    "type": "circle",
                    "source": "k12Datas",
                    "paint": {
                        "circle-radius": 8,
                        "circle-opacity": 0.8,
                        "circle-color": '#fbb03b'
                    },
                    "filter": ["all", ["==", "Level", "Secondary"],
                        ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018", "Fall 2017"]
                    ]
                })
            }
        }

    });
    buildLocationList(k12Datas); //add K12 partners to the left-hand sidebar
    //******************************Add an event when clicking on each item on the left-hand sidebar**********************************

    map.on('click', function(e) {
        // Query all the rendered points in the view
        map.getCanvas().style.cursor = 'pointer';
        var features = map.queryRenderedFeatures(e.point, {
            layers: ['show1', 'show2']
        });
        if (features.length) {
            var clickedPoint = features[0];
            // 1. Fly to the point
            flyToStore(clickedPoint);
            // 2. Close all other popups and display popup for clicked store
            createPopUp(clickedPoint);
            // 3. Highlight listing in sidebar (and remove highlight for all other listings)
            var activeItem = document.getElementsByClassName('active');
            if (activeItem[0]) {
                activeItem[0].classList.remove('active');
            }
            // Find the index of the store.features that corresponds to the clickedPoint that fired the event listener
            var selectedFeature = clickedPoint.properties['Address'];

            for (var i = 0; i < communityData.features.length; i++) {
                if (communityData.features[i].properties['Address'] === selectedFeature) {
                    selectedFeatureIndex = i;
                }
            }
            // Select the correct list item using the found index and add the active class
            var listing = document.getElementById('listing-' + selectedFeatureIndex);
            listing.classList.add('active');
        }
    });


    map.on('click', 'district', function(e) {
        popup.setLngLat(e.lngLat)
            .setHTML('<span style="font-weight:bold">District Number: </span>' + e.features[0].properties["id"])
            .addTo(map);
    });


    //****************************filter year*******************************************
    var selectYear = document.getElementById("selectYear");
    selectYear.addEventListener("change", function(e) {
        var value = e.target.value.trim().toLowerCase();

        if (value == 2018) {
            map.setFilter("show1",
                ["all", ["==", "Level", "Elementary"],
                    ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018"]
                ]
            )
            map.setFilter("show2",
                ["all", ["==", "Level", "Secondary"],
                    ['in', "time", "Spring 2018", "Fall 2018", "Summer 2018"]
                ]
            )

        } else if (value == 2017) {
            map.setFilter("show1",
                ["all", ["==", "Level", "Elementary"],
                    ['in', "time", "Fall 2017"]
                ]
            )
            map.setFilter("show2",
                ["all", ["==", "Level", "Secondary"],
                    ['in', "time", "Fall 2017"]
                ]
            )
        } else { //all

            map.setFilter("show1",
                ["==", "Level", "Elementary"]
            )
            map.setFilter("show2",
                ["==", "Level", "Secondary"]
            )
        }

    })


    //******************************Search Legislative District**********************************
    filterInput.addEventListener('keyup', function(e) {
        // If the input value matches a layerID set
        // it's visibility to 'visible' or else hide it.
        var value = e.target.value.trim().toLowerCase();
        layerIDs.forEach(function(layerID) {
            map.setLayoutProperty(layerID, 'visibility',
                layerID.indexOf(value) > -1 ? 'visible' : 'none');
        });
    });
});
//******************************Show a marker when clicking on the list on the left hand side**********************************
function buildLocationList(data) {
    // Iterate through the list of stores
    for (i = 0; i < data.features.length; i++) {
        var currentFeature = data.features[i];
        // Shorten data.feature.properties to just `prop` so we're not
        // writing this long form over and over again.
        var prop = currentFeature.properties;
        var description = parseDescription(prop);
        // Select the listing container in the HTML and append a div
        // with the class 'item' for each store
        var listings = document.getElementById('listings');
        var listing = listings.appendChild(document.createElement('div'));
        listing.className = 'item';
        listing.id = 'listing-' + i;

        // Create a new link with the class 'title' for each store
        // and fill it with the store address
        var link = listing.appendChild(document.createElement('a'));
        link.href = '#';
        link.className = 'title';
        link.dataPosition = i;
        link.innerHTML = prop['K-12 Partner'];
        var details = listing.appendChild(document.createElement('div'));
        details.innerHTML = description;

        link.addEventListener('click', function(e) {
            // Update the currentFeature to the store associated with the clicked link
            var clickedListing = data.features[this.dataPosition];
            // 1. Fly to the point associated with the clicked link
            flyToStore(clickedListing);
            // 2. Close all other popups and display popup for clicked store
            createPopUp(clickedListing);
            // 3. Highlight listing in sidebar (and remove highlight for all other listings)
            var activeItem = document.getElementsByClassName('active');
            if (activeItem[0]) {
                activeItem[0].classList.remove('active');
            }
            this.parentNode.classList.add('active');
        });

    }
}

//******************************Create a flying effect and popup**********************************
function flyToStore(currentFeature) {
    map.flyTo({
        center: currentFeature.geometry.coordinates,
        zoom: 15
    });
}

function createPopUp(currentFeature) {

    var popUps = document.getElementsByClassName('mapboxgl-popup');
    // Check if there is already a popup on the map and if so, remove it
    if (popUps[0]) popUps[0].remove();

    new mapboxgl.Popup().setLngLat(currentFeature.geometry.coordinates)
        .setHTML('<h3>' + currentFeature.properties['K-12 Partner'] + '</h3>' +
            '<h4>' + currentFeature.properties['Address'] + '</h4>')
        .addTo(map);
    close();
}

//******************************Add a clickable legend**********************************

var comlist = ["show1", "show2"];
var edu = document.getElementById("all");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show2") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'visible');
        }
    })

})

var edu = document.getElementById("elementary");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show1") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})

var edu = document.getElementById("secondary");
edu.addEventListener("click", function(e) {
    comlist.forEach(function(com) {
        if (com == "show2") {
            map.setLayoutProperty(com, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(com, 'visibility', 'none');
        }
    })

})