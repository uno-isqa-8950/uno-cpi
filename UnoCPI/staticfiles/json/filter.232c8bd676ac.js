var map
var markers = []

// start out with filter features set to false, so no filtering happens by default
var filters = {shower:false, vault:false, flush:false}

$(function () {
    $('input[name=filter]').change(function (e) {
     map_filter(this.id);
      filter_markers()
  });


})

var get_set_options = function() {
  ret_array = []
  for (option in filters) {
    if (filters[option]) {
      ret_array.push(option)
    }
  }
  return ret_array;
}

var filter_markers = function() {
  set_filters = get_set_options()

  // for each marker, check to see if all required options are set
  for (i = 0; i < markers.length; i++) {
    marker = markers[i];

    // start the filter check assuming the marker will be displayed
    // if any of the required features are missing, set 'keep' to false
    // to discard this marker
    keep=true
    for (opt=0; opt<set_filters.length; opt++) {
      if (!marker.properties[set_filters[opt]]) {
        keep = false;
      }
    }
    marker.setVisible(keep)
  }
}

var map_filter = function(id_val) {
   if (filters[id_val])
      filters[id_val] = false
   else
      filters[id_val] = true
}


// after the geojson is loaded, iterate through the map data to create markers
// and add the pop up (info) windows
function loadMarkers() {
  console.log('creating markers')
  var infoWindow = new google.maps.InfoWindow()
  geojson_url = 'https://raw.githubusercontent.com/gizm00/blog_code/master/appendto/python_maps_2/collection.geojson'
  $.getJSON(geojson_url, function(result) {
      // Post select to url.
      data = result['features']
      $.each(data, function(key, val) {
        var point = new google.maps.LatLng(
                parseFloat(val['geometry']['coordinates'][1]),
                parseFloat(val['geometry']['coordinates'][0]));
        var titleText = val['properties']['title']
        var descriptionText = val['properties']['description']
        var marker = new google.maps.Marker({
          position: point,
          title: titleText,
          map: map,
          properties: val['properties']
         });

        var markerInfo = "<div><h3>" + titleText + "</h3>Amenities: " + descriptionText + "</div>"


        marker.addListener('click', function() {
           $('#campground_info').html(markerInfo)
        });
        markers.push(marker)

      });
  });
}

function initMap() {
    map_options = {
      zoom: 10,
      mapTypeId: google.maps.MapTypeId.HYBRID,
      center: {lat: 42.9456, lng: -122.2}
    }

    map_document = document.getElementById('map')
    map = new google.maps.Map(map_document,map_options);
    loadMarkers()

}

google.maps.event.addDomListener(window, 'load', initMap);