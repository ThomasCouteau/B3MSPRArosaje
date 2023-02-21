<template>
  <q-page>
    <div class="text-h3 text-center q-ma-md">Votre profil</div>
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
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  name: "ProfilePage",
  setup() {
    const model = ref({
      pseudo: "",
      userTypeID: 0,
      picture: "",
      role: "",
    });

    const getCurrentUserDatas = async () => {
      let accessToken = { accessToken: localStorage.getItem("accessToken") };
      accessToken = JSON.stringify(accessToken);
      const response = await fetch("http://127.0.0.1:8000/user/me", {
        method: "POST",
        body: accessToken,
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

    onMounted(() => {
      getCurrentUserDatas();
      const base64Image = model.value.picture;
      model.value.picture = `data:image/png;base64,${base64Image}`;
    });

    return { model };
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

.pseudo {
  text-transform: capitalize;
}
</style>
