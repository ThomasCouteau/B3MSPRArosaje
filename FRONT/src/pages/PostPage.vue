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

      <div v-if="userIDType != 1">
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
    const userIDType = localStorage.getItem("userIDType");

    const getCurrentPlanteData = async () => {
      let body = {
        plante: { id: route.params.id },
        token: { accessToken: accessToken },
      };
      body = JSON.stringify(body);
      const response = await fetch("http://127.0.0.1:8000/plante/", {
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
      const response = await fetch(
        "http://127.0.0.1:8000/plante/updateGuardian/",
        {
          method: "POST",
          body: body,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
    };

    const keepPlante = async () => {
      await updateGuardian();
      let body = {
        plante: { id: model.value.id, status: 2 },
        token: { accessToken: accessToken },
      };
      body = JSON.stringify(body);
      const response = await fetch(
        "http://127.0.0.1:8000/plante/updateStatus/",
        {
          method: "POST",
          body: body,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      router.push("/home");
    };

    onMounted(() => {
      getCurrentPlanteData();
      const base64Image = model.value.picture;
      model.value.picture = `data:image/png;base64,${base64Image}`;
    });

    return { model, accessToken, keepPlante, userIDType };
  },
});
</script>

<style lang="scss">
.my-card {
  width: 100%;
  height: 100%;
  max-width: 400px;
  margin: auto;
}

.name {
  text-transform: capitalize;
}
</style>
