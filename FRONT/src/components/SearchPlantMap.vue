<template>
  <q-page>
    <div id="map" style="width: 70vw; height: 85vh; z-index: 1"></div>
  </q-page>
</template>

<script setup>
import { onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

function initializeMapAndLocator() {
  var map = L.map("map").setView([48.856614, 2.3522219], 6);

  var greenIcon = L.icon({
    iconUrl: "helper/leaf-green.png",

    iconSize: [45, 45], // size of the icon
    iconAnchor: [22.5, 22.5], // point of the icon which will correspond to marker's location
    popupAnchor: [0, 0], // point from which the popup should open relative to the iconAnchor
  });

  L.marker([51.5, -0.09], { icon: greenIcon })
    .addTo(map)
    .bindPopup("I am a green leaf.");

  L.tileLayer(
    "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      maxZoom: 19,
      id: "streets-v12",
      tileSize: 512,
      zoomOffset: -1,
      accessToken:
        "pk.eyJ1IjoidG9tbXkxMyIsImEiOiJjbGQ0ZGJ0ankwY2xqM3BwcXFvNzhtb2piIn0.mWwDQRmv8JSwBeD10Uw7Vw",
      setView: true,
      watch: true,
      timeout: 60000,
    }
  ).addTo(map);
}

onMounted(() => {
  initializeMapAndLocator();
});
</script>
