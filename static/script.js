function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            let currentLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            let map = new google.maps.Map(
                document.getElementById('map'),
                {center: currentLocation, zoom: 15}
            );

            let marker = new google.maps.Marker(
                {position: currentLocation, map: map, title: "Temp"}
            );
        }, function() {
            alert("Can't access location :(");
        });
    }
    else {
        alert('Please enable location!');
    }
}