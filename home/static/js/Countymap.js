//*********************************** Get mapbox API and get data from HTML *****************************************************

mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00']
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var filterlist = ["all", "all", "all", "all", "all", "all"] //first is for Mission Areas, second is for Community Types, 3rd for districts
    //4th for Campus Partner, 5th for Academic year, 6th for household income
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var count = 0;
communityData.features.forEach(function(feature) {
        feature.properties["id"] = count;
        feature.properties["campustest"] = 0 //this variable will be used to filter by campus partners
        feature.properties["yeartest"] = 0 //this variable will be used to filter by academic years
        count++;
    })
    //*********************************** Load the map *****************************************************

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-96.797885, 39.363438],
    // initial zoom
    zoom: 3.3
});
map.addControl(new mapboxgl.NavigationControl());
var popup = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: true,
});
//*********************************** Dynamically add the legends *****************************************************


var select = '';
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allmissions"><span style="background-color: transparent; border: 1px solid black"></span><b>All Mission Areas</b></a>' + "<br>";
for (var i = 0; i < Missionarea.length; i++) {
    var color = colorcode[i]
    var mission = Missionarea[i]
    select += `<a href="#"  id="${mission.valueOf()}" value="${mission.valueOf()}"><span style="background-color: ${color}"></span><b>${mission.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);
//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option val=' + "all" + ' selected="selected">' + "All District" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);

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
//*********************************** Load the county data here. Should be down here. Otherwise it won't load *****************************************************

var countyData = JSON.parse(document.getElementById('county-data').textContent);
//*********************************** Format the popup *****************************************************

var formatter = new Intl.NumberFormat('en-US', { //this is to format the current on the pop-up
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});


function parseDescription(message) {
    var string = "";

    for (var i in message) {
        if (message[i] != null && message[i] != 0 && message[i] != "" && message[i] != []){
            if (i == "CommunityPartner") {
                string += '<span style="font-weight:bold">' + 'Community Partner' + '</span>' + ": " + message[i] + "<br>";
            }
            if (i == "K-12 Partner") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Address") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Mission Area") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "City") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "  ";
            } else if (i == "State") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "STATE") {
                string += '<span style="font-weight:bold">' + 'State' + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "NAME") {
                string += '<span style="font-weight:bold">' + 'County' + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Income") {
                if (message[i]) {
                    string += '<span style="font-weight:bold">' + 'Household Income' + '</span>' + ": " + formatter.format(message[i]) + "<br>";
                }
            } else if (i == "income") {
                if (message[i]) {
                    string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + formatter.format(message[i]) + "<br>"
                }
            } else if (i == "County") {
                if (message[i]) {
                    string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + message[i] + "<br>"
                }
            } else if (i == "Legislative District Number") {
                if (message[i] !== 0) {
                    string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + message[i] + "<br>"
                }
            } else if (i == "CommunityType") {
                string += '<span style="font-weight:bold">' + "Community Type" + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Campus Partner") {
                if (message[i]) {
                    string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
                }
            } else if (i == "Number of projects") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Academic Year") {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            } else if (i == "Website") {
                var website = message[i];
                var base = "http://";
                if (!website.includes("http")) {
                    website = base.concat(website);
                }
                string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${i}</a><br>`;
            }
        }
    }
    return string;
};
//*********************************** Load the map *****************************************************
var fillcolor = '#3c341f'
map.on("load", function() {

    map.addSource('communityData', {
        type: 'geojson',
        data: communityData,
    });
    map.addSource('countyData', {
        type: 'geojson',
        data: countyData,
    });
    //*********************************** Load the county in different household income levels *****************************************************

    countyData.features.forEach(function(feature) {
            var income = feature.properties["Income"];
            if (income < 25000) {
                layerID = "income1";
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "fill",
                        "source": "countyData",
                        'layout': {},
                        'paint': {
                            "fill-color": "#B8B8B8",
                            "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                                1,
                                0.5
                            ],
                            "fill-outline-color": fillcolor
                        },
                        "filter": ["all", ["<", "Income", 25000]]
                    })
                }
            } else if (25000 <= income && income < 40000) {
                layerID = "income2";
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "fill",
                        "source": "countyData",
                        'layout': {},
                        'paint': {
                            "fill-color": "#989898",
                            "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                                1,
                                0.5
                            ],
                            "fill-outline-color": fillcolor
                        },
                        "filter": ["all", [">=", "Income", 25000],
                            ["<", "Income", 40000]
                        ]
                    })
                }
            } else if (40000 <= income && income < 60000) {
                layerID = "income3";
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "fill",
                        "source": "countyData",
                        'layout': {},
                        'paint': {
                            "fill-color": "#808080",
                            "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                                1,
                                0.5
                            ],
                            "fill-outline-color": fillcolor
                        },
                        "filter": ["all", [">=", "Income", 40000],
                            ["<", "Income", 60000]
                        ]
                    })
                }
            } else if (60000 <= income && income < 80000) {
                layerID = "income4";
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "fill",
                        "source": "countyData",
                        'layout': {},
                        'paint': {
                            "fill-color": "#686868",
                            "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                                1,
                                0.5
                            ],
                            "fill-outline-color": fillcolor
                        },
                        "filter": ["all", [">=", "Income", 60000],
                            ["<", "Income", 80000]
                        ]
                    })
                }
            } else if (80000 <= income && income < 100000) {
                layerID = "income5";
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "fill",
                        "source": "countyData",
                        'layout': {},
                        'paint': {
                            "fill-color": "#505050",
                            "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                                1,
                                0.5
                            ],
                            "fill-outline-color": fillcolor
                        },
                        "filter": ["all", [">=", "Income", 80000],
                            ["<", "Income", 100000]
                        ]
                    })
                }
            } else if (100000 <= income) {
                layerID = "income6";
                if (!map.getLayer(layerID)) {
                    map.addLayer({
                        "id": layerID,
                        "type": "fill",
                        "source": "countyData",
                        'layout': {},
                        'paint': {
                            "fill-color": "#303030",
                            "fill-opacity": ["case", ["boolean", ["feature-state", "hover"], false],
                                1,
                                0.5
                            ],
                            "fill-outline-color": fillcolor
                        },
                        "filter": ["all", [">=", "Income", 100000]]
                    })
                }
            }
        })
        //*********************************** Load partners *****************************************************

    map.addLayer({
        "id": "commMap",
        "type": "circle",
        "source": "communityData",
        'layout': {},
        'paint': {
            "circle-radius": 8,
            "circle-opacity": 1,
            "circle-color": {
                "property": "Mission Area",
                "type": 'categorical',
                "stops": [
                    [Missionarea[0], colorcode[0]],
                    [Missionarea[1], colorcode[1]],
                    [Missionarea[2], colorcode[2]],
                    [Missionarea[3], colorcode[3]],
                    [Missionarea[4], colorcode[4]],
                    [Missionarea[5], colorcode[5]],
                ]
            }
        }
    });
    //*********************************** function to show pop-up when clicking on the partner *****************************************************

    map.on("click", "commMap", function(e) { //go through every layer. Refer to showlist
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);
        map.flyTo({
            center: e.features[0].geometry.coordinates
        });
        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    //*********************************** Campus Partner filter *****************************************************

    var selectCampus = document.getElementById('selectCampus'); //get the element on HTML
    selectCampus.addEventListener("change", function(e) {
            var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
            if (!CampusPartnerlist.includes(value)) { // in the case of all Campus partners
                filterlist[3] = "all";
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
            } else { //in case a campus partner is chosen
                communityData.features.forEach(function(feature) { //iterate through the dataset
                    var campuspartner = feature.properties["Campus Partner"] //get the campus partner
                    if (campuspartner.includes(value)) { // if the partner has that campus partner
                        feature.properties["campustest"] = 1 // assign this value 1
                    } else {
                        feature.properties["campustest"] = 0 //if not, assign this value 0
                    }
                })
                map.getSource('communityData').setData(communityData); // update the dataset
                map.removeLayer("commMap");
                map.addLayer({
                    "id": "commMap",
                    "type": "circle",
                    "source": "communityData",
                    'layout': {},
                    'paint': {
                        "circle-radius": 8,
                        "circle-opacity": 1,
                        "circle-color": {
                            "property": "Mission Area",
                            "type": 'categorical',
                            "stops": [
                                [Missionarea[0], colorcode[0]],
                                [Missionarea[1], colorcode[1]],
                                [Missionarea[2], colorcode[2]],
                                [Missionarea[3], colorcode[3]],
                                [Missionarea[4], colorcode[4]],
                                [Missionarea[5], colorcode[5]],
                            ]
                        }
                    }
                });
                filterlist[3] = 1;
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
            }
        })

    //*********************************** Community Type filter *****************************************************

    var selectCommtype = document.getElementById('selectCommtype');
    selectCommtype.addEventListener("change", function(e) {
        var value = e.target.value.trim();
        if (!CommunityType.includes(value)) {
            //get the number of markers and show it on the HTML
            filterlist[1] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
        } else {
            for (var i = 0; i <= CommunityType.length; i++) {
                if (value == CommunityType[i]) {
                    filterlist[1] = value
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
                }
            }
        }
    })

    //*********************************** Academic Year filter *****************************************************

    var selectYear = document.getElementById('selectYear'); //same concept as campus partner. Just for years
    selectYear.addEventListener("change", function(e) {
        var value = e.target.value.trim();
        if (!yearlist.includes(value)) {
            filterlist[4] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
        } else {
            communityData.features.forEach(function(feature) {
                var year = feature.properties["Academic Year"]
                console.log(year)
                if (year) {
                    for (var j = 0; j < year.length; j++){
                        if (year[j] == value){
                            feature.properties["yeartest"] = 1
                        } else {
                            feature.properties["yeartest"] = 0
                        }
                    }
                } else {
                    feature.properties["yeartest"] = 0
                }
            })
            map.getSource('communityData').setData(communityData); // update the dataset
            map.removeLayer("commMap");
            map.addLayer({
                "id": "commMap",
                "type": "circle",
                "source": "communityData",
                'layout': {},
                'paint': {
                    "circle-radius": 8,
                    "circle-opacity": 1,
                    "circle-color": {
                        "property": "Mission Area",
                        "type": 'categorical',
                        "stops": [
                            [Missionarea[0], colorcode[0]],
                            [Missionarea[1], colorcode[1]],
                            [Missionarea[2], colorcode[2]],
                            [Missionarea[3], colorcode[3]],
                            [Missionarea[4], colorcode[4]],
                            [Missionarea[5], colorcode[5]],
                        ]
                    }
                }
            });
            filterlist[4] = 1
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
        }
    })

   //*********************************** District filter *****************************************************

    var selectDistrict = document.getElementById('selectDistrict');
    selectDistrict.addEventListener("change", function(e) {
        var value = e.target.value.trim().toLowerCase();
        value = parseInt(value)
        if (isNaN(value)) {
            // get the number of markers that fit the requirement and show on the HTML
            filterlist[2] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
        } else {
            filterlist[2] = value
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
        }
    })

        //*********************************** Household income filter *****************************************************

    var countyList = ["income1", "income2", "income3", "income4", "income5", "income6"];
    var edu = document.getElementById("allincome");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income1") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'visible');
            }
        })
        // get the number of markers that fit the requirement and show on the HTML
        filterlist[5] = "all"
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    })


    var edu = document.getElementById("income1");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income1") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'none');
            }
        });
        filterlist[5] = [0,25000]
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    });

    var edu = document.getElementById("income2");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income2") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'none');
            }
        })
        filterlist[5] = [25000, 40000]
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    })
    var edu = document.getElementById("income3");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income3") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'none');
            }
        })
        filterlist[5] = [40000, 60000]
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    })
    var edu = document.getElementById("income4");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income4") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'none');
            }
        })
        filterlist[5] = [60000, 80000]
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    })
    var edu = document.getElementById("income5");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income5") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'none');
            }
        })
        filterlist[5] = [80000, 100000]
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    })
    var edu = document.getElementById("income6");
    edu.addEventListener("click", function(e) {
        countyList.forEach(function(county) {
            if (county == "income6") {
                map.setLayoutProperty(county, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(county, 'visibility', 'none');
            }
        })
        filterlist[5] = [100000, 1000000]
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
    })

    //*********************************** Search function *****************************************************
    var valueFilter = document.getElementById("valueFilter");

    //Press the listening button
    valueFilter.addEventListener("keydown", function(e) {
        if (e.keyCode == 8) {
            map.setFilter("commMap", null);
        }
    });

    // the listening button off

    valueFilter.addEventListener("keyup", function(e) {
        //get the input value
        var value = e.target.value.trim().toLowerCase();

        if (value == "") {
            renderListings([]);
        } else {
            //get geojosn data from the map
            var cmValue = [];
            for (var j = 0; j < Missionarea.length; j++) {
                cmValue[j] = map.queryRenderedFeatures({
                    layers: ["commMap"]
                });
            }
            var filtered = [];
            var filtereds = [];
            for (var j = 0; j < Missionarea.length; j++) {
                filtered[j] = cmValue[j].filter(function(feature) {
                    var name = normalize(feature.properties.CommunityPartner);
                    return name.indexOf(value) == 0;
                });
                filtereds = filtereds.concat(filtered[j]);
            }

            console.log(filtereds);
            renderListings(filtereds);

            for (var j = 0; j < Missionarea.length; j++) {
                if (filtered[j].length > 0) {
                    map.setFilter("commMap", ['match', ['get', 'id'], filtered[j].map(function(feature) {
                        console.log(feature.properties.id);
                        return feature.properties.id;
                    }), true, false]);
                } else {
                    console.log("111111111111");
                    map.setFilter("commMap", ['match', ['get', 'id'], -1, true, false]);
                }
            }

        }
    });

})


//***********************************search function*****************************************************
function normalize(string) {
    return string.trim().toLowerCase();
}


function renderListings(features) {
    var parent = document.getElementById("sidebar");
    console.log(parent);
    var listings = document.getElementById("listings");
    console.log(listings);
    if (listings != null) {
        parent.removeChild(listings);
    }


    if (features.length) {

        listings = document.createElement("div");
        console.log(listings);
        listings.setAttribute("id", "listings");
        listings.setAttribute("class", "listings");

        parent.appendChild(listings);
        listings.innerHTML = '';

        var i = 0;

        features.forEach(function(feature) {
            listings.style.display = 'block';

            var prop = feature.properties;
            var description = parseDescription(prop);

            var listing = listings.appendChild(document.createElement('div'));
            listing.className = 'item';
            listing.id = 'listing-' + i;

            var link = listing.appendChild(document.createElement('a'));
            link.href = '#';
            link.className = 'title';
            link.dataPosition = i;
            link.innerHTML = prop.CommunityPartner;
            link.addEventListener('click', function(e) {
                // Update the currentFeature to the store associated with the clicked link
                var clickedListing = features[this.dataPosition];
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


            //			var details = listing.appendChild(document.createElement('div'));
            //			details.innerHTML = description;
            i++;
        });

    } else {
        var empty = document.createElement('p');
        empty.textContent = 'Drag the map to populate results';
        listings.appendChild(empty);
        listings.style.display = 'none';
    }
}

//***********************************filter by clickable legends*****************************************************


var edu = document.getElementById("all"); //get the total number of dots
edu.addEventListener("click", function(e) {

    filterlist[0] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5])
})

$('#legend a').click(function(e) { //filter dots by mission areas and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    var i = Missionarea.indexOf(clickedValue);
    if (i > -1) {
        filterlist[0] = clickedValue;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4],filterlist[5]);
    }
});

$("#reset").click(function() {
    filterlist[0] = "all";
    filterlist[1] = "all";
    filterlist[2] = "all";
    filterlist[3] = "all";
    filterlist[4] = "all";
    filterlist[5] = "all";
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4], filterlist[5]);
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

    var countyList = ["income1", "income2", "income3", "income4", "income5", "income6"];
    countyList.forEach(function(county) {
        if (county == "income1") {
            map.setLayoutProperty(county, 'visibility', 'visible');
        } else {
            map.setLayoutProperty(county, 'visibility', 'visible');
        }
    })
});


function calculation(a, b, c, d, e, f) {
    var totalnumber = ''
    var number = 0

    if (a == "all") {
        if (b == "all") {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            map.setFilter("commMap", null);
                            totalnumber += communityData.features.length
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1]) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1]])
                            totalnumber += number
                        }
                    }
                }
            } else { //else for c
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "Legislative District Number", c]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "Legislative District Number", c]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1],
                            ["==", "Legislative District Number", c]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "Legislative District Number", c]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1],
                            ["==", "Legislative District Number", c]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "Legislative District Number", c]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "Legislative District Number", c]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1],
                            ["==", "Legislative District Number", c]])
                            totalnumber += number
                        }
                    }
                }
            }
        } else {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1], ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    }
                }
            } else { //else for b
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['CommunityType'] == b && feature.properties['Legislative District Number'] == c) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "CommunityType", b], ["==", "Legislative District Number", c]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "Legislative District Number", c], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1],
                            ["==", "Legislative District Number", c], ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "Legislative District Number", c], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1],
                            ["==", "Legislative District Number", c], ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "Legislative District Number", c], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "Legislative District Number", c],
                            ["==", "CommunityType", b]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1],
                            ["==", "Legislative District Number", c], ["==", "CommunityType", b]])
                            totalnumber += number
                        }
                    }
                }
            }
        }
    } else {
        if (b == "all") {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                }
            } else { //else for c
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1],
                            ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1],
                            ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1],
                            ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                }
            }
        } else {
            if (c == "all") {
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                }
            } else { //else for b
                if (d == "all") {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['CommunityType'] == b && feature.properties['Legislative District Number'] == c && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "CommunityType", b], ["==", "Legislative District Number", c], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "Legislative District Number", c], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1],
                            ["==", "Legislative District Number", c], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "Legislative District Number", c], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                } else {
                    if (e == "all") {
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "campustest", 1],
                            ["==", "Legislative District Number", c], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "campustest", 1], ["==", "Legislative District Number", c], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    } else { //else for e
                        if (f == "all") {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['yeartest'] == 1 && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", ["==", "yeartest", 1], ["==", "campustest", 1], ["==", "Legislative District Number", c],
                            ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        } else {
                            communityData.features.forEach(function(feature) {
                                if (feature.properties['Income'] > f[0] && feature.properties["Income"] < f[1] && feature.properties['yeartest'] == e && feature.properties['campustest'] == 1 && feature.properties['Legislative District Number'] == c && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                                    number += 1
                                }
                            })
                            map.setFilter("commMap", ["all", [">", "Income", f[0]],
                                ["<", "Income", f[1]], ["==", "yeartest", 1], ["==", "campustest", 1],
                            ["==", "Legislative District Number", c], ["==", "CommunityType", b], ["==", "Mission Area", a]])
                            totalnumber += number
                        }
                    }
                }
            }
        }
    }
    $('#totalnumber').html(totalnumber);
}


