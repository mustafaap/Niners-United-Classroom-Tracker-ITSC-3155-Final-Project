function initMap() {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(position => {
      let currentLocation = { lat: position.coords.latitude, lng: position.coords.longitude };
      // let currentLocation = { lat: 35.30560154079038, lng: -80.73442849115179 };

      let map = new google.maps.Map(
        document.getElementById('map'), { center: currentLocation, zoom: 17 }
      );

      let marker = new google.maps.Marker(
        { position: currentLocation, map: map, title: "Current location" }
      );

      fetch('static/campus.json')
        .then(resp => resp.json())
        .then(data => {
          let buildings = data.buildings;
          let closestBuilding = null;
          let minDist = Number.MAX_VALUE;

          buildings.forEach(building => {
            building.coordinates.forEach(coord => {
              let dist = google.maps.geometry.spherical.computeDistanceBetween(
                new google.maps.LatLng(currentLocation),
                new google.maps.LatLng(coord.lat, coord.lng)
              );

              // let newMarker = new google.maps.Marker(
              //   { position: new google.maps.LatLng(coord.lat, coord.lng), map: map }
              // )

              console.log(`Distance to ${building.name} is ${dist}`);

              if (dist < minDist) {
                closestBuilding = building;
                minDist = dist;
              }
            });
          });

          document.querySelector('#closest').textContent = `The closest building to your location is: ${closestBuilding.name}.`;
        })
        .catch(error => console.log(error));
    });
  } else {
    alert('Please enable location to use the NUTT map.');
  }
}


function checkPasswordMatch() {
  var password = document.getElementById("password");
  var repassword = document.getElementById("repassword");
  var error = document.getElementById("passwordMatchError");
  if (password.value != repassword.value) {
    error.style.display = "block";
    repassword.classList.add("is-invalid");
    return false;
  } else {
    error.style.display = "none";
    repassword.classList.remove("is-invalid");
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
  var password = document.getElementById("password");
  var error = document.getElementById("passwordLengthError");
  if (password.value.length < 8) {
    error.style.display = "block";
    password.classList.add("is-invalid");
    return false;
  } else {
    error.style.display = "none";
    password.classList.remove("is-invalid");
    return true;
  }
}

function validatePassword() {
  if (checkPasswordLength() && checkPasswordMatch()) {
    return true;
  }
  return false;
}

function validateForm() {
  if (checkPasswordLength() && checkPasswordMatch() && checkUsernameLength()) {
    return true;
  }
  return false;
}

function validateEditForm() {
  if (checkUsernameLength()) {
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

function checkUsernameLength() {
  var input = document.getElementById('username');
  if (input.value.length < 8 || input.value.length > 32) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
    return true;
  }
}

function checkRestroomLength() {
  var input = document.getElementById('restroom');
  if (input.value.length > 32 || input.value.length === 0) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
    return true;
  }
}

function checkLocationLength() {
  var input = document.getElementById('location');
  if (input.value.length > 32 || input.value.length === 0) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
    return true;
  }
}

function checkFeedbackLength() {
  var input = document.getElementById('rating_body');
  if (input.value.length > 250) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else if(input.value.length === 0){
    input.classList.remove("is-valid");
    return true;
  }
  else {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
    return true;
  }
}

function validateCreateRestroomForm() {
  if (checkRestroomLength() && checkFeedbackLength()) {
    return true;
  }
  return false;
}

function validateIndexRestroomForm() {
  if (checkLocationLength() && checkFeedbackLength()) {
    return true;
  }
  return false;
}

function checkInputRequired(inputId) {
  var input = document.getElementById(inputId);
  if (input.value.length === 0) {
    input.classList.add("is-invalid");
  } else {
    input.classList.remove("is-invalid");
  }
}
