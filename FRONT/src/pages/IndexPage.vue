<template>
  <q-page class="q-ma-md">
    <div class="text-h4 text-center">Fil d'actualité</div>
    <div class="column items-center justify-center q-ma-md">
      <div
        class="col q-ma-md"
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
          </q-item>
          <img :src="plantesActu.picture" />

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
            <div class="row items-center">
              <div class="col-8">
                <q-input
                  borderless
                  v-model="model.message"
                  label="Commentaire"
                />
              </div>
              <div class="col-2">
                <q-btn
                  flat
                  rounded
                  color="primary"
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
import { defineComponent, ref } from "vue";

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
      const response = await fetch("http://127.0.0.1:8000/plante/search", {
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
        "http://127.0.0.1:8000/commentaire/" + planteID + "/add/",
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

    return {
      model,
      addCommentToPlante,
    };
  },
});
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  height: 100%
  max-height: 120vh
  max-width: 50vw
</style>
