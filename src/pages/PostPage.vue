<template>
  <q-page class="q-mt-md">
    <q-card class="my-card">
      <div class="text-center" v-if="model.picture != null">
        <q-img fit="cover" :src="model.picture" />
      </div>

      <img v-else src="/helper/leaf-green.png" />

      <q-card-section>
        <div class="text-h6 name">{{ model.name }}</div>
        <div class="text-subtitle2 text-capitalize">{{ model.owner }}</div>
      </q-card-section>
      <q-separator />

      <div v-if="userTypeID != 1">
        <q-card-actions align="right">
          <q-btn color="secondary" flat label="Garder" @click="keepPlante" />
        </q-card-actions>
      </div>
    </q-card>
    <div class="column items-center q-ma-lg">
      <q-btn color="secondary" label="Retour" href="/search" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { API_URL } from "../utils/utils.js";

export default defineComponent({
  name: "PostPage",
  components: {},
  setup() {
    const model = ref({
      name: "",
      picture: "",
      owner: "",
      id: null,
    });

    const route = useRoute();
    const router = useRouter();

    const accessToken = localStorage.getItem("accessToken");
    const userID = localStorage.getItem("userID");
    const userTypeID = localStorage.getItem("userTypeID");

    const getCurrentPlanteData = async () => {
      let body = {
        plante: { id: route.params.id },
        token: { accessToken: accessToken },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/plante/", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      const myJson = await response.json();
      console.log(myJson);
      model.value.name = myJson.name;
      model.value.picture = myJson.picture;
      model.value.owner = myJson.owner.pseudo;
      model.value.id = myJson.id;
    };

    const updateGuardian = async () => {
      let body = {
        plante: { id: model.value.id, guardian: { id: userID } },
        token: { accessToken: accessToken },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/plante/updateGuardian/", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
    };

    const keepPlante = async () => {
      await updateGuardian();
      let body = {
        plante: { id: model.value.id, status: 2 },
        token: { accessToken: accessToken },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/plante/updateStatus/", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      router.push("/home");
    };

    onMounted(() => {
      getCurrentPlanteData();
      const base64Image = model.value.picture;
      model.value.picture = `data:image/png;base64,${base64Image}`;
    });

    return { model, accessToken, keepPlante, userTypeID };
  },
});
</script>

<style lang="scss">
//mobile
@media screen and (max-width: 600px) {
  .my-card {
    width: 80vw;
    height: 100%;
    max-width: 400px;
    margin: auto;
  }
}

//desktop
@media screen and (min-width: 600px) {
  .my-card {
    width: 100%;
    height: 100%;
    max-width: 400px;
    margin: auto;
  }
}

.name {
  text-transform: capitalize;
}
</style>
