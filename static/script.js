let currentLocation;
let map;
let marker;

function initMap() {
    if (navigator && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            currentLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            map = new google.maps.Map(
                document.getElementById('map'),
                {center: currentLocation, zoom: 17}
            );

            marker = new google.maps.Marker(
                {position: currentLocation, map: map, title: "Current location"}
            );
        }, function(error) {
            console.error(error);
            alert("Can't access location :(");
        });
    }
    else {
        alert('Please enable location!');
    }
}