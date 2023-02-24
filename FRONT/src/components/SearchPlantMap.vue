<template>
  <q-page>
    <div id="map"></div>
  </q-page>
</template>

<script>
import { defineComponent, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { API_URL } from "../utils/utils.js";

export default defineComponent({
  name: "SearchPlantMap",
  data() {
    return {
      allAvailablePlante: [],
    };
  },
  mounted() {
    const accessToken = localStorage.getItem("accessToken");

    const getAllAvailablePlante = async () => {
      let body = {
        searchSetting: {
          availablePlante: true, // Si la plante est disponible
          keptPlante: false, // Si la plante est gardée
          donePlante: false, // Si la plante est terminée
          ownerID: -1, // ID du propriétaire (-1 = tous)
          guardianID: -1, // ID du gardien (-1 = tous)
          latitude: -1, // Latitude du centre de la zone de recherche (-1 = tous)
          longitude: -1, // Longitude du centre de la zone de recherche (-1 = tous)
          radius: -1, // Rayon de la zone de recherche (-1 = tous)
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/plante/search", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      this.allAvailablePlante = await response.json();
      console.log(this.allAvailablePlante);
    };

    const initializeMapAndLocator = async () => {
      await getAllAvailablePlante();
      var map = L.map("map").setView([48.856614, 2.3522219], 6);

      var greenIcon = L.icon({
        iconUrl: "helper/leaf-green.png",

        iconSize: [45, 45], // size of the icon
        iconAnchor: [22.5, 22.5], // point of the icon which will correspond to marker's location
        popupAnchor: [0, 0], // point from which the popup should open relative to the iconAnchor
      });

      for (let index = 0; index < this.allAvailablePlante.length; index++) {
        L.marker(
          [
            this.allAvailablePlante[index].latitude,
            this.allAvailablePlante[index].longitude,
          ],
          { icon: greenIcon }
        )
          .addTo(map)
          .bindPopup(
            this.allAvailablePlante[index].name +
              "<br><a href='/post/" +
              this.allAvailablePlante[index].id +
              "'>Voir</a>"
          );
      }

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
    };

    initializeMapAndLocator();
  },
});
</script>

<style lang="scss">
@media screen and (max-width: 600px) {
  #map {
    height: 85vh;
    width: 85vw;
    z-index: 1;
  }
}
@media screen and (min-width: 600px) {
  #map {
    height: 85vh;
    width: 70vw;
    z-index: 1;
  }
}
</style>
