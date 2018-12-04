//*********************************** Get mapbox API and get data from HTML *****************************************************

mapboxgl.accessToken = 'pk.eyJ1IjoibG9va3VwbWFuIiwiYSI6ImNqbW41cmExODBxaTEzeHF0MjhoZGg1MnoifQ.LGL5d5zGa1z6ms-IVyn7sw';
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00'];
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);
var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent);



console.log(Missionarea);
console.log(CommunityType);
console.log(CampusPartnerlist);

//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var count = 0;
communityData.features.forEach(function(feature) {
    feature.properties["id"] = count;
    count++;
});

console.log(communityData);
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
//*********************************** Dynamically add the legends *****************************************************


var select = '';
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allmissions"><span style="background-color: black"></span><b>All Mission Areas</b></a>' + "<br>";
for (var i = 0; i < Missionarea.length; i++) {
    var color = colorcode[i]
    var mission = Missionarea[i]
    select += `<a href="#"  id="${mission.valueOf()}" value="${mission.valueOf()}"><span style="background-color: ${color}"></span><b>${mission.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);
//*********************************** Add the districts *****************************************************

var select1 = '';
select1 += '<option val=' + "all" + '>' + "All District" + '</option>';
for (i = 1; i <= 49; i++) {
    select1 += '<option val=' + i + '>' + i + '</option>';
}
$('#selectDistrict').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select2 = '';
select2 += '<option val=' + "alltypes" + '>' + 'All Community Types' + '</option>';
for (i = 0; i < CommunityType.length; i++) {
    select2 += '<option val=' + CommunityType[i] + '>' + CommunityType[i] + '</option>';
}
$('#selectCommtype').html(select2);
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

//reorganise CampusPartnerlist，void showing the same CampusPartner
var campus=[];

for(i=0;i<CampusPartnerlist.length;i++){
    for(var j=0;j<CampusPartnerlist[i].length;j++){
        if(!campus.includes(CampusPartnerlist[i][j])){
            campus.push(CampusPartnerlist[i][j]);
        }
    }
}
console.log(campus);

var select3 = '';
select3 += '<option val=' + "allcampus" + '>' + 'All Campus Partners' + '</option>';
for (i = 0; i < campus.length; i++) {
    select3 += '<option val="' + campus[i] + '">' + campus[i] + '</option>';

}
$('#selectCampus').html(select3);

//*********************************** Format the popup *****************************************************

var formatter = new Intl.NumberFormat('en-US', { //this is to format the current on the pop-up
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});


function parseDescription(message) {
    var string = "";

    for (var i in message) {


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
        } else if (i == "Website") {
            var website = message[i];
            var base = "http://";
            if (!website.includes("http")) {
                website = base.concat(website);
            }
            string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${i}</a><br>`;
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
            string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
        } else if (i == "Campus Partner") {
            if (message[i]) {
                string += '<span style="font-weight:bold">' + i + '</span>' + ": " + message[i] + "<br>";
            }
        }
    }
    return string;
};
//*********************************** Load the map *****************************************************

map.on("load", function() {

    map.addSource('communityData', {
        type: 'geojson',
        data: communityData,
    });
//*********************************** Load partners *****************************************************

    communityData.features.forEach(function(feature) {
        var primary = feature.properties["Mission Area"];
        var commType = feature.properties["CommunityType"];
        var base = "show";
        for (var i = 0; i < Missionarea.length; i++) {
            if (primary == Missionarea[i]) {
                layerID = base + (i + 1);
                // console.log(layerID);
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
                        "filter": ["all", ["==", "Mission Area", primary]]
                    })
                }
            }
        }
    });
//*********************************** function to show pop-up when clicking on the partner *****************************************************

    map.on("click", "show1", function(e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show2", function(e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show3", function(e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show4", function(e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show5", function(e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
    map.on("click", "show6", function(e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties;
        description = parseDescription(description);

        popup.setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
        close();
    });
//*********************************** Community Type filter *****************************************************

    $("#selectCommtype").change(function (e) {
        var value = e.target.value.trim();

        console.log(CommunityType.includes(value));
        if (!CommunityType.includes(value)) {
            for(var j=0;j<Missionarea.length;j++){
                map.setFilter(comlist[j], ["all", ["==", "Mission Area", Missionarea[j]]]);
            }
        } else {
            for(var j=0;j<Missionarea.length;j++){
                console.log(value);
                map.setFilter(comlist[j], ["all", ["==", "Mission Area", Missionarea[j]],
                    ["==", "CommunityType", value]
                ])
            }

        }
    });



   //*********************************** Campus Type filter *****************************************************
    var comlist = ["show1", "show2", "show3", "show4", "show5", "show6"];


     $("#selectCampus").on("select2:close",function (e) {

        for(var j=0;j<Missionarea.length;j++){
            map.setFilter(comlist[j], ["==", "Mission Area", Missionarea[j]]);
        }
    });



   $("#selectCampus").on("select2:select",function (e){

        var value = e.target.value.trim();
        setTimeout(function () {//set and execute after 50ms, in case it will start to filter before initiation
            var cmValue=[];
            for(var j=0;j<Missionarea.length;j++){
                cmValue[j]=map.queryRenderedFeatures({
                    layers: [comlist[j]]
                });
            }

            //filter all fit partner
            var filtered=[];
            for(var j=0;j<Missionarea.length;j++){
                filtered[j]=cmValue[j].filter(function(feature) {
                    var name = feature.properties["Campus Partner"].trim();
                    return name.includes(value);
                });
            }

            //filter on the map
            if (!campus.includes(value)) {
                for(var j=0;j<Missionarea.length;j++){
                    map.setFilter(comlist[j], ["all", ["==", "Mission Area", Missionarea[j]]]);
                }
            } else {
                for(var j=0;j<Missionarea.length;j++){
                    if (filtered[j].length > 0) {
                        map.setFilter(comlist[j], ['match', ['get', 'id'], filtered[j].map(function(feature) {
                            console.log(feature.properties.id);
                            return feature.properties.id;
                        }), true, false]);
                    } else {
                        map.setFilter(comlist[j], ['match', ['get', 'id'], -1, true, false]);
                    }
                }
            }
        },50);
    });



//*********************************** District filter *****************************************************


    $("#selectDistrict").change(function (e) {
        var value = e.target.value.trim().toLowerCase();
        value = parseInt(value);

        if (isNaN(value)) {
            for(var j=0;j<Missionarea.length;j++){
                map.setFilter(comlist[j], ["all", ["==", "Mission Area", Missionarea[j]]]);
            }

        } else {
            for(var j=0;j<Missionarea.length;j++){
                map.setFilter(comlist[j], ["all", ["==", "Mission Area", Missionarea[j]],
                    ["==", "Legislative District Number", value]
                ]);
            }
        }

    });


//*********************************** Search function *****************************************************

    var valueFilter = document.getElementById("valueFilter");

    //Press the listening button
    valueFilter.addEventListener("keydown", function(e) {
        if (e.keyCode == 8) {
            for(var j=0;j<Missionarea.length;j++){
                map.setFilter(comlist[j], ["==", "Mission Area", Missionarea[j]]);
            }

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
            var cmValue=[];
            for(var j=0;j<Missionarea.length;j++){
                cmValue[j]=map.queryRenderedFeatures({
                    layers: [comlist[j]]
                });
            }

            //filter the name(s) that include the input value
            var filtered=[];
            var filtereds = [];
            for(var j=0;j<Missionarea.length;j++){
                filtered[j]=cmValue[j].filter(function(feature) {
                    var name = normalize(feature.properties.CommunityPartner);
                    return name.indexOf(value) == 0;
                });
                filtereds=filtereds.concat(filtered[j]);
            }

            console.log(filtereds);
            renderListings(filtereds);

            for(var j=0;j<Missionarea.length;j++){
                if (filtered[j].length > 0) {
                    map.setFilter(comlist[j], ['match', ['get', 'id'], filtered[j].map(function(feature) {
                        console.log(feature.properties.id);
                        return feature.properties.id;
                    }), true, false]);
                } else {

                    map.setFilter(comlist[j], ['match', ['get', 'id'], -1, true, false]);
                }
            }


        }
    });

});


//***********************************search function*****************************************************
function normalize(string) {
    return string.trim().toLowerCase();
}


function renderListings(features) {
    // var parent = document.getElementById("sidebar");
    var parent = document.getElementById("filerCommunity");
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
                var activeItem = document.getElementsByClassName('active1');
                if (activeItem[0]) {
                    activeItem[0].classList.remove('active1');
                }
                this.parentNode.classList.add('active1');
            });


            //			var details = listing.appendChild(document.createElement('div'));
            //			details.innerHTML = description;
            i++;
        });

    } else {
        listings = document.createElement("div");
        console.log(listings);
        listings.setAttribute("id", "listings");
        listings.setAttribute("class", "listings");

        parent.appendChild(listings);
        var empty = document.createElement('p');
        empty.textContent = 'Drag the map to populate results';
        listings.appendChild(empty);
        listings.style.display = 'none';
    }
}

//***********************************clickable legends*****************************************************


var comlist = ["show1", "show2", "show3", "show4", "show5", "show6"];

var edu = document.getElementById("all");
edu.addEventListener("click", function(e) {
    for(var i=0;i<Missionarea.length;i++){
        map.setLayoutProperty(comlist[i], 'visibility', 'visible');
    }
    // comlist.forEach(function(com) {
    //     map.setLayoutProperty(com, 'visibility', 'visible');
    // })

});



var edu = document.getElementById("Economic Sufficiency");
if(edu){
    edu.addEventListener("click", function(e) {
        var index=Missionarea.indexOf("Economic Sufficiency")
        for(var i=0;i<Missionarea.length;i++) {
            if (i==index) {
                map.setLayoutProperty(comlist[i], 'visibility', 'visible');
            } else {
                map.setLayoutProperty(comlist[i], 'visibility', 'none');
            }
        }

    })
}


var edu = document.getElementById("Educational Support");
if(edu){
    edu.addEventListener("click", function(e) {
        var index=Missionarea.indexOf("Educational Support")
        for(var i=0;i<Missionarea.length;i++){
            if (i==index) {
                map.setLayoutProperty(comlist[i], 'visibility', 'visible');
            } else {
                map.setLayoutProperty(comlist[i], 'visibility', 'none');
            }
        }

    })
}


var edu = document.getElementById("Environmental Stewardship");
if(edu){
    edu.addEventListener("click", function(e) {
        var index=Missionarea.indexOf("Environmental Stewardship");
        for(var i=0;i<Missionarea.length;i++){
            if (i==index) {
                map.setLayoutProperty(comlist[i], 'visibility', 'visible');
            } else {
                map.setLayoutProperty(comlist[i], 'visibility', 'none');
            }
        }

    })
}


var edu = document.getElementById("Health and Wellness");
if(edu){
    edu.addEventListener("click", function(e) {
        var index=Missionarea.indexOf("Health and Wellness");
        for(var i=0;i<Missionarea.length;i++){
            if (i==index) {
                map.setLayoutProperty(comlist[i], 'visibility', 'visible');
            } else {
                map.setLayoutProperty(comlist[i], 'visibility', 'none');
            }
        }

    });
}


var edu = document.getElementById("International Service");
if(edu){
    edu.addEventListener("click", function(e) {
        var index=Missionarea.indexOf("International Service")
        for(var i=0;i<Missionarea.length;i++){
            if (i==index) {
                map.setLayoutProperty(comlist[i], 'visibility', 'visible');
            } else {
                map.setLayoutProperty(comlist[i], 'visibility', 'none');
            }
        }

    })
}

var edu = document.getElementById("Social Justice");
if(edu){
   edu.addEventListener("click", function(e) {
       var index=Missionarea.indexOf("Social Justice")
        for(var i=0;i<Missionarea.length;i++) {
            if (i==index) {
                map.setLayoutProperty(comlist[i], 'visibility', 'visible');
            } else {
                map.setLayoutProperty(comlist[i], 'visibility', 'none');
            }
        }

    })
}


// var edu = document.getElementById("selectCommtype");
// edu.addEventListener("change", function(e) {
//     var value = e.target.value.trim();
//         if (!CommunityType.includes(value)) {
//             map.setFilter("show1", ["all", ["==", "Mission Area", Missionarea[0]]])
//             map.setFilter("show2", ["all", ["==", "Mission Area", Missionarea[1]]])
//             map.setFilter("show3", ["all", ["==", "Mission Area", Missionarea[2]]])
//             map.setFilter("show4", ["all", ["==", "Mission Area", Missionarea[3]]])
//             map.setFilter("show5", ["all", ["==", "Mission Area", Missionarea[4]]])
//             map.setFilter("show6", ["all", ["==", "Mission Area", Missionarea[5]]])
//         } else {
//             var ind = Missionarea.indexOf(value)
//             if (com == comlist[ind]) {
//                 map.setLayoutProperty(com, 'visibility', 'visible');
//             } else {
//                 map.setLayoutProperty(com, 'visibility', 'none');
//             }
//         }
//
// })


function flyToStore(currentFeature) {
    map.flyTo({
        center: currentFeature.geometry.coordinates,
        zoom: 10
    });
}

function createPopUp(currentFeature) {

    var popUps = document.getElementsByClassName('mapboxgl-popup');
    map.getCanvas().style.cursor = 'pointer';
    // Check if there is already a popup on the map and if so, remove it
    if (popUps[0]) popUps[0].remove();
    var description = currentFeature.properties;
    description = parseDescription(description);


    new mapboxgl.Popup().setLngLat(currentFeature.geometry.coordinates)
        .setHTML(description)
        // .setHTML('<h3>' + currentFeature.properties['CommunityPartner'] + '</h3>' +
        //     '<h4>' + currentFeature.properties['Address'] + '</h4>')
        .addTo(map);
    close();



}