function initMap() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      let currentLocation = { lat: position.coords.latitude, lng: position.coords.longitude };
      // let currentLocation = { lat: 35.3073501955218, lng: -80.73549898386916 };
      
      let map = new google.maps.Map(
        document.getElementById('map'), { center: currentLocation, zoom: 17 }
      );
      
      let marker = new google.maps.Marker(
        { position: currentLocation, map: map, title: "Current location" }
      );

      let campus = new google.maps.places.PlacesService(map);
      campus.nearbySearch({
        location: currentLocation,
        radius: 1000
      }, (results, status) => {
        if (status !== 'OK') {
          console.error('Error searching for nearby buildings:', status);
          return;
        }

        let buildings = results.map(result => {
          return {
            name: result.name,
            lat: result.geometry.location.lat(),
            lng: result.geometry.location.lng()
          };
        });

        let closestBuilding = null;
        let minDist = Number.MAX_VALUE;

        buildings.forEach(building => {
          let dist = google.maps.geometry.spherical.computeDistanceBetween(
            new google.maps.LatLng(currentLocation),
            new google.maps.LatLng(building.lat, building.lng)
          );

          console.log(`Distance to ${building.name} is ${dist}`);

          if (dist < minDist) {
            closestBuilding = building;
            minDist = dist;
          }
        });

        document.querySelector('#closest').textContent = `The closest building to your location is: ${closestBuilding.name}.`;
      });
    }, (error) => {
      console.error(error);
      alert("Can't access location :(");
    });
  } else {
    alert('Please enable location!');
  }
}


function checkPasswordMatch() {
  var password = document.getElementById("password").value;
  var repassword = document.getElementById("repassword").value;
  var error = document.getElementById("passwordMatchError");
  if (password != repassword) {
    error.style.display = "block";
    return false;
  } else {
    error.style.display = "none";
    return true;
  }
}

function togglePasswordVisibility(inputId, iconId) {
  var input = document.getElementById(inputId);
  var icon = document.getElementById(iconId);

  if (input.type === "password") {
    input.type = "text";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  } else {
    input.type = "password";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  }
}

function checkPasswordLength() {
  var password = document.getElementById("password").value;
  var error = document.getElementById("passwordLengthError");
  if (password.length < 8) {
    error.style.display = "block";
    return false;
  } else {
    error.style.display = "none";
    return true;
  }
}

function validatePassword() {
  if (checkPasswordLength() && checkPasswordMatch()) {
    return true;
  }
  return false;
}

function checkInputCorrect(inputId) {
  var input = document.getElementById(inputId);
  if (input.value.length === 0) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
  } else {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
  }
}

function checkInputRequired(inputId) {
  var input = document.getElementById(inputId);
  if (input.value.length === 0) {
    input.classList.add("is-invalid");
  } else {
    input.classList.remove("is-invalid");
  }
}