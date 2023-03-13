<template>
  <q-page>
    <div class="text-h5 text-center q-ma-md">Votre profil</div>
    <q-card class="my-card">
      <div class="text-center" v-if="model.picture != null">
        <q-img fit="cover" :src="model.picture" />
      </div>

      <img v-else src="https://cdn.quasar.dev/img/mountains.jpg" />

      <q-card-section>
        <div class="text-h6 pseudo">{{ model.pseudo }}</div>
        <div class="text-subtitle2">{{ model.role }}</div>
      </q-card-section>
    </q-card>
    <div class="column q-ma-md">
      <div
        class="col q-mt-lg"
        :key="index"
        v-for="(planteUser, index) in allPlanteOfUser"
      >
        <q-card class="my-card">
          <q-item>
            <q-item-section avatar>
              <q-avatar>
                <img :src="planteUser.owner.picture" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-capitalize">{{
                planteUser.owner.pseudo
              }}</q-item-label>
            </q-item-section>
            <q-btn
              color="grey-7"
              round
              flat
              icon="more_vert"
              v-if="userTypeID == 2 || userID == planteUser.owner.id"
            >
              <q-menu cover auto-close>
                <q-list>
                  <q-item clickable @click="deletePlante(planteUser.id)">
                    <q-item-section>Supprimer la plante</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-item>

          <div v-if="planteUser.picture">
            <q-img fit="cover" :src="planteUser.picture" />
          </div>
          <img v-else src="/helper/leaf-green.png" />
          <q-card-section class="q-pt-none">
            <div class="text-h6 text-capitalize">{{ planteUser.name }}</div>
            <q-separator />
            <div class="text-subtitle2" v-if="planteUser.guardian">
              Gardée par {{ planteUser.guardian.pseudo }}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onBeforeMount, onMounted } from "vue";
import { API_URL } from "../utils/utils.js";

export default defineComponent({
  name: "ProfilePage",
  data() {
    return {
      allPlanteOfUser: [],
    };
  },
  setup() {
    const model = ref({
      pseudo: "",
      userTypeID: 0,
      picture: "",
      role: "",
    });
    const accessToken = localStorage.getItem("accessToken");
    const userID = localStorage.getItem("userID");

    const getCurrentUserDatas = async () => {
      let body = { accessToken: accessToken };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/user/me", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      const myJson = await response.json();
      console.log(myJson);
      model.value.pseudo = myJson.pseudo;
      if (myJson.userTypeID == 1) model.value.role = "Botaniste";
      else if (myJson.userTypeID == 2) model.value.role = "Administrateur";
      else if (myJson.userTypeID == 3) model.value.role = "Gardien";
      model.value.userTypeID = myJson.userTypeID;
      model.value.picture = myJson.picture;
    };

    const deletePlante = async (planteID) => {
      let body = {
        plante: {
          id: planteID,
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/plante/delete/", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      location.reload();
    };

    onBeforeMount(() => {
      getCurrentUserDatas();
      // const base64Image = model.value.picture;
      // model.value.picture = `data:image/png;base64,${base64Image}`;
    });

    return { model, deletePlante, userID };
  },
  mounted() {
    const userID = localStorage.getItem("userID");
    const accessToken = localStorage.getItem("accessToken");

    const getAllPlanteOfUser = async () => {
      let body = {
        searchSetting: {
          availablePlante: true, // Si la plante est disponible
          keptPlante: true, // Si la plante est gardée
          donePlante: true, // Si la plante est terminée
          ownerID: userID, // ID du propriétaire (-1 = tous)
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
      this.allPlanteOfUser = await response.json();
      console.log(this.allPlanteOfUser);
    };
    getAllPlanteOfUser();
  },
});
</script>

<style lang="scss">
//desktop
@media screen and (min-width: 600px) {
  .my-card {
    width: 100%;
    height: 100%;
    max-width: 400px;
    margin: auto;
  }
}

//mobile
@media screen and (max-width: 600px) {
  .my-card {
    width: 80vw;
    height: 100%;
    max-width: 400px;
    margin: auto;
  }
}

.pseudo {
  text-transform: capitalize;
}
</style>
