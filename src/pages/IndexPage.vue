<template>
  <q-page class="q-ma-md">
    <div class="text-h5 text-center">Fil d'actualité</div>
    <div class="column items-center justify-center q-ma-md">
      <div
        class="col q-mt-lg"
        :key="index"
        v-for="(plantesActu, index) in allKeepPlante"
      >
        <q-card class="my-card">
          <q-item>
            <q-item-section avatar>
              <q-avatar>
                <img :src="plantesActu.owner.picture" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-capitalize">{{
                plantesActu.owner.pseudo
              }}</q-item-label>
            </q-item-section>
            <q-btn
              color="grey-7"
              round
              flat
              icon="more_vert"
              v-if="userTypeID == 2 || userID == plantesActu.owner.id"
            >
              <q-menu cover auto-close>
                <q-list>
                  <q-item clickable @click="deletePlante(plantesActu.id)">
                    <q-item-section>Supprimer la plante</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-item>

          <div v-if="plantesActu.picture">
            <q-img fit="cover" :src="plantesActu.picture" />
          </div>
          <img v-else src="/helper/leaf-green.png" />

          <q-card-section class="q-pt-none">
            <div class="text-h6 text-capitalize">{{ plantesActu.name }}</div>
            <div v-if="plantesActu.comments.length != 0">
              <p
                v-for="(comment, index) in plantesActu.comments
                  .slice()
                  .reverse()"
                :key="index"
              >
                <span class="text-subtitle2">
                  {{ comment.author.pseudo }}:
                </span>
                {{ comment.message }}
              </p>
            </div>
            <div v-else>
              <p>Aucun commentaire pour le moment...</p>
            </div>

            <q-separator />
            <div class="row items-center justify-between">
              <div class="">
                <q-input
                  borderless
                  v-model="model.message"
                  label="Commentaire"
                />
              </div>
              <div class="float-right">
                <q-btn
                  flat
                  rounded
                  color="secondary"
                  label="Publier"
                  @click="addCommentToPlante(plantesActu.id)"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { API_URL } from "../utils/utils.js";

export default defineComponent({
  name: "IndexPage",
  components: {},
  data() {
    return {
      allKeepPlante: [],
    };
  },
  mounted() {
    const accessToken = localStorage.getItem("accessToken");

    const getAllKeepPlante = async () => {
      let body = {
        searchSetting: {
          availablePlante: false, // Si la plante est disponible
          keptPlante: true, // Si la plante est gardée
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
      this.allKeepPlante = await response.json();
      console.log(this.allKeepPlante);
    };

    getAllKeepPlante();
  },
  setup() {
    const model = {
      message: "",
    };
    const accessToken = localStorage.getItem("accessToken");
    const userTypeID = localStorage.getItem("userTypeID");
    const userID = localStorage.getItem("userID");

    const addCommentToPlante = async (planteID) => {
      let body = {
        comment: {
          message: model.message,
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(
        API_URL + "/commentaire/" + planteID + "/add/",
        {
          method: "POST",
          body: body,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const myJson = await response.json();
      console.log(myJson);
      location.reload();
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

    return {
      model,
      addCommentToPlante,
      userTypeID,
      userID,
      deletePlante,
    };
  },
});
</script>

<style lang="scss">
//mobile
@media screen and (max-width: 600px) {
  .my-card {
    width: 85vw;
  }
}

//desktop
@media screen and (min-width: 600px) {
  .my-card {
    width: 50vw;
  }
}
</style>
