<template>
  <q-page>
    <div class="profile-container q-ma-md">
      <div class="profile-picture">
        <q-avatar size="150px" class="fit-content">
          <q-img fit="cover" :src="model.picture" />
        </q-avatar>
      </div>
      <div class="profile-details">
        <div class="profile-name">{{ model.pseudo }}</div>
        <div class="profile-description">{{ model.role }}</div>
        <div class="profile-link">
          <a target="_blank" :href="API_URL + '/file/rgpd/'"
            >Traitement de mes données.</a
          >
        </div>
      </div>
    </div>
    <q-separator />
    <q-tabs
      v-model="tab"
      inline-label
      switch-indicator
      align="justify"
      indicator-color="primary"
    >
      <q-tab name="my-plants" icon="yard" label="Mes plantes" />
      <q-tab name="keep" icon="fire_extinguisher" label="Je garde" />
    </q-tabs>
    <div
      class="column q-ma-md"
      v-if="tab === 'my-plants' && allPlanteOfUser.length > 0"
    >
      <div
        class="col q-ma-md"
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
    <div class="column q-ma-md" v-if="tab === 'keep' && keepPlantes.length > 0">
      <div
        class="col q-ma-md"
        :key="index"
        v-for="(keepPlante, index) in keepPlantes"
      >
        <q-card class="my-card">
          <q-item>
            <q-item-section avatar>
              <q-avatar>
                <img :src="keepPlante.owner.picture" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-capitalize">{{
                keepPlante.owner.pseudo
              }}</q-item-label>
            </q-item-section>
          </q-item>

          <div v-if="keepPlante.picture">
            <q-img fit="cover" :src="keepPlante.picture" />
          </div>
          <img v-else src="/helper/leaf-green.png" />
          <q-card-section class="q-pt-none">
            <div class="text-h6 text-capitalize">{{ keepPlante.name }}</div>
            <q-separator />
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
  <LoaderCustom />
</template>

<script>
import { defineComponent, ref, onBeforeMount, onMounted } from "vue";
import { API_URL } from "../utils/utils.js";
import LoaderCustom from "src/components/LoaderCustom.vue";

export default defineComponent({
  name: "ProfilePage",
  components: {
    LoaderCustom,
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

    const allPlanteOfUser = ref([]);
    const keepPlantes = ref([]);

    let tab = ref("my-plants");

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
      allPlanteOfUser.value = await response.json();
      console.log(allPlanteOfUser.value);
    };

    const getKeepPlantesOfUser = async () => {
      let body = {
        searchSetting: {
          availablePlante: false, // Si la plante est disponible
          keptPlante: true, // Si la plante est gardée
          donePlante: false, // Si la plante est terminée
          ownerID: -1, // ID du propriétaire (-1 = tous)
          guardianID: userID, // ID du gardien (-1 = tous)
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
      keepPlantes.value = await response.json();
      console.log(keepPlantes.value);
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
      getAllPlanteOfUser();
      getKeepPlantesOfUser();
    });

    return {
      model,
      deletePlante,
      userID,
      API_URL,
      tab,
      allPlanteOfUser,
      keepPlantes,
    };
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
.my-datas {
  color: $info;
  text-decoration: none;
}

.profile-container {
  display: flex;
  align-items: center;
}

.profile-picture {
  margin-right: 32px;
}

.profile-details {
  flex: 1;
}

.profile-name {
  font-size: 24px;
  font-weight: bold;
}

.profile-description {
  font-size: 18px;
  color: #8e8e8e;
  margin-top: 4px;
}

.profile-link {
  margin-top: 16px;
}

.profile-link a {
  color: $info;
  text-decoration: none;
  font-size: 16px;
}

.profile-link a:hover {
  text-decoration: underline;
}
</style>
