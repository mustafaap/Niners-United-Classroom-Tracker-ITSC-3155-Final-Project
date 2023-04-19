function initMap() {
  let buildings = [
    {
      name: "Student Union",
      lat: 35.30877807870519,
      lng: -80.73375730520932
    },
    {
      name: "Woodward Hall",
      lat: 35.30734769178602,
      lng: -80.73549720057893
    },
    {
      name: "Atkins Library",
      lat: 35.30587055087016,
      lng: -80.73213129167284
    }
  ];

    if (navigator.geolocation) {
      navigator.geolocation.watchPosition(position => {
        let currentLocation = { lat: position.coords.latitude, lng: position.coords.longitude };
        // let currentLocation = { lat: 35.3073476917860, lng:  -80.73549720057900 };
        let closestBuilding = null;
        let minDist = Number.MAX_VALUE;

        let map = new google.maps.Map(
          document.getElementById('map'), { center: currentLocation, zoom: 17 }
        );
        let marker = new google.maps.Marker(
          { position: currentLocation, map: map, title: "Current location" }
        );

        buildings.forEach(building => {
          let dist = google.maps.geometry.spherical.computeDistanceBetween(
            new google.maps.LatLng(currentLocation),
            new google.maps.LatLng(building.lat, building.lng)
          );

          if (dist < minDist) {
            closestBuilding = building;
            minDist = dist;
          }
        });

        document.querySelector('#closest').textContent = `The closest building to your location is: ${closestBuilding.name}.`;
      }, (error) => {
        console.error(error);
        alert("Can't access location :(");
      });
    }
    else {
      alert('Please enable location!');
    }
}