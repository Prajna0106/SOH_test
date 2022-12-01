// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;
var lat,lng;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 15,
  });
  infoWindow = new google.maps.InfoWindow();

  const locationButton = document.createElement("button");
  var la=20.2776174 
  var ln=85.7777318

  locationButton.textContent = " Click for Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      setInterval(()=>{
        navigator.geolocation.getCurrentPosition(
          (position) => {
            var pos = {
              lat:la,//position.coords.latitude,
              lng:ln//position.coords.longitude,
            };
            la+=0.0001
            ln+=0.0001
  
            infoWindow.setPosition(pos);
            infoWindow.setContent("Garbage Truck location");
            infoWindow.open(map);
            map.setCenter(pos);
            console.log(pos)
          },
          () => {
            handleLocationError(true, infoWindow, map.getCenter());
          }
        )
        
      },800)
      
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });
}
//const beachMarker = new google.maps.Marker({
  //position: { lat: -33.89, lng: 151.274 },
  //map,
  //icon: <img src="truck.png" alt=""/>,
//});

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

window.initMap = initMap;