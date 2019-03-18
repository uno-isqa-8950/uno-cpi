//*********************************** Get mapbox API and get data from HTML *****************************************************

//mapboxgl.accessToken = 'pk.eyJ1IjoidW5vY3BpZGV2dGVhbSIsImEiOiJjanJiZTk2cjkwNjZ5M3l0OGNlNWZqYm91In0.vPmkC3MFDrTlBk-ntUFruA';
var colorcode = ['#17f3d1', '#65dc1e', '#1743f3', '#ba55d3', '#e55e5e', '#FFFF00'];
var colorcode_gmap = ['17f3d1', '65dc1e', '1743f3', 'ba55d3', 'e55e5e', 'FFFF00'];
var Missionarea = JSON.parse(document.getElementById('missionlist').textContent);

var CommunityType = JSON.parse(document.getElementById('CommTypelist').textContent);
var CampusPartnerlist = JSON.parse(document.getElementById('campusPartner-list').textContent);
var communityData = JSON.parse(document.getElementById('commPartner-data').textContent); //load the variable from views.py. See the line from html first
var yearlist = JSON.parse(document.getElementById('year-list').textContent);
var filterlist = ["all", "all", "all", "all", "all"] //first is for Mission Areas, second is for Community Types, 3rd for districts
    //4th for Campus Partner, 5th for Academic year
    //*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var count = 0;
communityData.features.forEach(function(feature) {
        feature.properties["id"] = count;
        feature.properties["campustest"] = 0 //this variable will be used to filter by campus partners
        feature.properties["yeartest"] = 0 //this variable will be used to filter by academic years
        feature.properties["visible"] = true;
        count++;
    })
    //*********************************** Load the map *****************************************************

//var map = new mapboxgl.Map({
//    container: 'map',
//    style: 'mapbox://styles/mapbox/light-v9',
//    center: [-95.957309, 41.276479],
//    // initial zoom
//    zoom: 6
//});
//map.addControl(new mapboxgl.NavigationControl());
//var popup = new mapboxgl.Popup({
//    closeButton: true,
//    closeOnClick: true,
//});
//*********************************** Dynamically add the legends *****************************************************


var select = '';
select += '<a href="#" ' + 'id=' + '"all" ' + 'value=' + '"allcommunitys"><span style="background-color: transparent; border: 1px solid black"></span><b>All Community Type</b></a>' + "<br>";
for (var i = 0; i < CommunityType.length; i++) {
    var color = colorcode[i]
    var community = CommunityType[i]
    select += `<a href="#"  id="${community.valueOf()}" value="${community.valueOf()}"><span style="background-color: ${color}"></span><b>${community.toString()}</b></a>` + "<br>";
}
$('#legend').html(select);
//*********************************** Add the districts *****************************************************

//var select1 = '';
//select1 += '<option val=' + "all" + ' selected="selected">' + "All District" + ' </option>';
//for (i = 1; i <= 49; i++) {
//    select1 += '<option val=' + i + '>' + i + '</option>';
//}
//$('#selectDistrict').html(select1);

//*********************************** Add the community type drop-down *****************************************************

var select2 = '';
select2 += '<option val=' + "allmissions" + ' selected="selected">' + 'All Mission Area' + '</option>';
for (i = 0; i < Missionarea.length; i++) {
    select2 += '<option val=' + Missionarea[i] + '>' + Missionarea[i] + '</option>';
}
$('#selectMissionarea').html(select2);
//*********************************** Add id variable to Community Data GEOJSON for search function later *****************************************************

var select3 = '';
select3 += '<option val=' + "allcampus" + ' selected="selected">' + 'All Campus Partners' + '</option>';
for (i = 0; i < CampusPartnerlist.length; i++) {
    select3 += '<option val=' + CampusPartnerlist[i] + '>' + CampusPartnerlist[i] + '</option>';
}
$('#selectCampus').html(select3);

//*********************************** Add year filter *****************************************************

var select4 = '';
select4 += '<option val=' + 0 + ' >' + 'All Academic Years' + '</option>';
for (i = 0; i < yearlist.length; i++) {
    select4 += '<option val=' + i + '>' + yearlist[i] + '</option>';
}
$('#selectYear').html(select4);

//*********************************** Format the popup *****************************************************

var formatter = new Intl.NumberFormat('en-US', { //this is to format the current on the pop-up
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});


function parseDescription(message) {
    var string = "";
    message.forEachProperty(function(value,property) {
        if (value != null && value != 0 && value != "" && value != [] && value != "[]"){
            if (property == "CommunityPartner") {
                string += '<span style="font-weight:bold">' + 'Community Partner' + '</span>' + ": " + value + "<br>";
            }
            if (property == "K-12 Partner") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
            } else if (property == "Address") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
            } else if (property == "Mission Area") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
            } else if (property == "City") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "  ";
            } else if (property == "State") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
            } else if (property == "STATE") {
                string += '<span style="font-weight:bold">' + 'State' + '</span>' + ": " + value + "<br>";
            } else if (property == "NAME") {
                string += '<span style="font-weight:bold">' + 'County' + '</span>' + ": " + value + "<br>";
            } else if (property == "Income") {
                if (value) {
                    string += '<span style="font-weight:bold">' + 'Household Income' + '</span>' + ": " + formatter.format(value) + "<br>";
                }
            } else if (property == "income") {
                if (value) {
                    string += '<span style="font-weight:bold">' + "Household Income" + '</span>' + ": " + formatter.format(value) + "<br>"
                }
            } else if (property == "County") {
                if (value) {
                    string += '<span style="font-weight:bold">' + "County" + '</span>' + ": " + value + "<br>"
                }
            } else if (property == "Legislative District Number") {
                if (value !== 0) {
                    string += '<span style="font-weight:bold">' + "Legislative District Number" + '</span>' + ": " + value + "<br>"
                }
            } else if (property == "CommunityType") {
                string += '<span style="font-weight:bold">' + "Community Type" + '</span>' + ": " + value + "<br>";
            } else if (property == "Campus Partner") {
                if (value) {
                    string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
                }
            } else if (property == "Number of projects") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
            } else if (property == "Academic Year") {
                string += '<span style="font-weight:bold">' + property + '</span>' + ": " + value + "<br>";
            } else if (property == "Website") {
                var website = value;
                var base = "http://";
                if (!website.includes("http")) {
                    website = base.concat(website);
                }
                string += `<a target="_blank" href="${website}" class="popup" style="color:darkblue">View ${property}</a><br>`;
            }
        }
    });
    return string;
};
//*********************************** Load the map *****************************************************

function calculation(a, b, c, d, e) {
    var totalnumber = ''
    var number = 0

    if (a == "all") {
        if (b == "all") {
            if (d == "all") {
                if (e == "all") {
                    for (var i = 0; i < partners_a.length; i++){
                       partners_a[i].setProperty('visible', true);
                    }
                    totalnumber += communityData.features.length
                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['yeartest'] == 1) {
                            number += 1
                        }
                    })

                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number
                }
            } else { //else for data[3] if
                if (e = "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1) {
                            number += 1
                        }
                    })
                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('campustest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1) {
                            if (feature.properties['yeartest'] == 1) {
                                number += 1
                            }
                        }
                    })

                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('yeartest') == 1 && partners_a[i].getProperty('campustest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }

                    totalnumber += number
                }
            }
        } else { //else if for data[1]
            if (d == "all") {
                if (e == "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['CommunityType'] == b) {
                            number += 1
                        }
                    })
                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('CommunityType') == b)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number
                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1) {
                            number += 1
                        }
                    })
                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('CommunityType') == b && partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number
                }
            } else { //else for data[3] if
                if (e == "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b) {
                            number += 1
                        }
                    })
                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('CommunityType') == b && partners_a[i].getProperty('campustest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b) {
                            number += 1
                        }
                    })
                    for (var i = 0; i < partners_a.length; i++){
                        if( partners_a[i].getProperty('CommunityType') == b && partners_a[i].getProperty('campustest') == 1 && partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number
                }
            }
        }
    } else { // else for data[0]
        if (b == "all") {
            if (d == "all") {
                if (e == "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                }
            } else { //else for data[3] if
                if (e == "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1 && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('campustest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('campustest') == 1  && partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number
                }
            }
        } else {
            if (d == "all") {
                if (e == "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('CommunityType') == b)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['CommunityType'] == b && feature.properties['yeartest'] == 1 && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('CommunityType') == b && partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number

                }
            } else { //else for data[3] if
                if (e == "all") {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('CommunityType') == b && partners_a[i].getProperty('campustest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }

                    totalnumber += number;

                } else {
                    communityData.features.forEach(function(feature) {
                        if (feature.properties['campustest'] == 1 && feature.properties['yeartest'] == 1 && feature.properties['CommunityType'] == b && feature.properties['Mission Area'] == a) {
                            number += 1
                        }
                    });
                    for (var i = 0; i < partners_a.length; i++){
                        if(partners_a[i].getProperty('Mission Area') == a && partners_a[i].getProperty('CommunityType') == b && partners_a[i].getProperty('campustest') == 1  && partners_a[i].getProperty('yeartest') == 1)
                            partners_a[i].setProperty('visible', true);
                        else
                            partners_a[i].setProperty('visible', false);
                    }
                    totalnumber += number;

                }
            }
        }
    }
    $('#totalnumber').html(totalnumber);
}


var map; //start a map
var partners_a;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), { //get the base map and Omaha zoomed out
        zoom: 7,  //zoom level
        center: {lat: 41.276479, lng: -95.957309} //Omaha coordinates
    });

    var partners = new google.maps.Data(); //create an object for Community Partner GEOJSON
    partners_a = partners.addGeoJson(communityData);

     partners.setStyle(function(feature) {
        var color = 'FF0000';
        for (var i = 0; i < CommunityType.length; i++)
        {
            if(feature.getProperty('CommunityType') == CommunityType[i]){
                color = colorcode_gmap[i];
                break;
            }
        }
        var symbol = '%E2%80%A2';  // dot

        return /** @type {google.maps.Data.StyleOptions} */ {
            visible: feature.getProperty('visible'),
            icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter_withshadow&chld=' + symbol + '|' + color
        };
    });


    partners.setMap(map); //add the object to the map


    var infowindow = new google.maps.InfoWindow(); //create the infowindow object

    // When the user clicks, open an infowindow
    partners.addListener('click', function (event) {
        var myHTML = parseDescription(event.feature);
        infowindow.setContent("<div style='width:200px; text-align: left;'>" + myHTML + "</div>");
        infowindow.setPosition(event.feature.getGeometry().get());
        infowindow.setOptions({pixelOffset: new google.maps.Size(0, -30)});
        infowindow.open(map);
        close();
    })
    //*********************************** Campus Partner filter *****************************************************

    var selectCampus = document.getElementById('selectCampus'); //get the element on HTML
    selectCampus.addEventListener("change", function(e) {
            var value = e.target.value.trim(); //get the value of the drop-down. In this case, the text on the drop-down
            if (!CampusPartnerlist.includes(value)) { // in the case of all Campus partners
                filterlist[3] = "all";
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
            } else { //in case a campus partner is chosen
                communityData.features.forEach(function(feature) { //iterate through the dataset
                    var campuspartner = feature.properties["Campus Partner"] //get the campus partner
                    if (campuspartner.includes(value)) { // if the partner has that campus partner
                        feature.properties["campustest"] = 1 // assign this value 1
                    } else {
                        feature.properties["campustest"] = 0 //if not, assign this value 0
                    }
                })
//                for (var i = 0; i < partners_a.length; i++)
//                    map.data.remove(partners_a[i]);
//
//                partners_a = partners.addGeoJson(communityData);
                filterlist[3] = 1;
                calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
            }
        })
        //*********************************** Community Type filter *****************************************************

    var selectMissionarea = document.getElementById('selectMissionarea');
    selectMissionarea.addEventListener("change", function(e) {
        var value = e.target.value.trim();

        if (!Missionarea.includes(value)) {
            //get the number of markers and show it on the HTML
            filterlist[0] = "all"
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        } else {
            for (var i = 0; i <= Missionarea.length; i++) {
                if (value == Missionarea[i]) {
                    filterlist[0] = value
                    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
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
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
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

            filterlist[4] = 1
            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
        }
    })

    //*********************************** District filter *****************************************************

//    var selectDistrict = document.getElementById('selectDistrict');
//    selectDistrict.addEventListener("change", function(e) {
//        var value = e.target.value.trim().toLowerCase();
//        value = parseInt(value)
//        if (isNaN(value)) {
//            // get the number of markers that fit the requirement and show on the HTML
//            filterlist[2] = "all"
//            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
//        } else {
//            filterlist[2] = value
//            calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
//        }
//    })

    //*********************************** Search function *****************************************************
    var valueFilter = document.getElementById("valueFilter");

    //Press the listening button
    valueFilter.addEventListener("keydown", function(e) {
        if (e.keyCode == 8) {
            for (var i = 0; i < partners_a.length; i++){
               partners_a[i].setProperty('visible', true);
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

}
google.maps.event.addDomListener(window, 'load', initMap);

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
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4])
})

$('#legend a').click(function(e) { //filter dots by community types and show the number
    var clickedValue = $(e.target).text(); //get the value from the choice
    var i = CommunityType.indexOf(clickedValue);
    if (i > -1) {
        filterlist[1] = clickedValue;
        calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    }
});

$("#reset").click(function() {
    filterlist[0] = "all"
    filterlist[1] = "all"
    filterlist[2] = "all"
    filterlist[3] = "all"
    filterlist[4] = "all"
    calculation(filterlist[0], filterlist[1], filterlist[2], filterlist[3], filterlist[4]);
    $('#selectMissionarea option').prop('selected', function() {
        return this.defaultSelected;
    });
//    $('#selectDistrict option').prop('selected', function() {
//        return this.defaultSelected;
//    });
    $('#selectCampus option').prop('selected', function() {
        return this.defaultSelected;
    });
    $('#selectYear option').prop('selected', function() {
        return this.defaultSelected;
    });
});
