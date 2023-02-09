<template>
  <q-page>
    <div class="text-h3 text-center q-ma-md">Créer un post</div>
    <div class="column items-center q-ma-md">
      <q-input
        stack-label
        clearable
        filled
        v-model="model.name"
        label="Nom de la plante"
        class="q-ma-md"
        style="width: 50vw"
      />
      <q-file
        filled
        v-model="model.picture"
        label="Photos de la plante"
        stack-label
        class="q-ma-md"
        style="width: 50vw"
        @update:model-value="
          async (val) => (fileToConvert = await convertFileToBase64(val))
        "
      />
      <!-- <q-input
        v-model="model.description"
        filled
        clearable
        type="textarea"
        stack-label
        label="Description"
        class="q-ma-md"
        style="width: 50vw"
      /> -->
      <q-btn
        class="q-ma-md"
        color="primary"
        label="Créer"
        @click="createPost"
      />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, onMounted, ref } from "vue";

export default defineComponent({
  name: "CreatePostPage",

  setup() {
    const model = ref({
      name: "",
      picture: null,
      // description: "",
      latitude: 0,
      longitude: 0,
    });

    let fileToConvert = null;

    //function to convert file to base64
    const convertFileToBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);

        fileReader.onload = () => {
          resolve(fileReader.result);
          fileToConvert = fileReader.result;
        };

        fileReader.onerror = (error) => {
          reject(error);
        };
      });
    };

    const getCurrentPosition = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          model.value.latitude = position.coords.latitude;
          model.value.longitude = position.coords.longitude;
          console.log(
            "latitude:",
            model.value.latitude,
            "longitude:",
            model.value.longitude
          );
        });
      } else {
        console.log("Geolocation is not supported by this browser.");
      }
    };

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
    };

    const createPost = async () => {
      model.value.picture = fileToConvert;
      let accessToken = { accessToken: localStorage.getItem("accessToken") };
      let body = {
        plante: {
          name: model.value.name,
          latitude: model.value.latitude,
          longitude: model.value.longitude,
          picture: model.value.picture,
        },
        token: accessToken,
      };
      body = JSON.stringify(body);
      console.log(body);
      const response = await fetch("http://127.0.0.1:8000/plante/add", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      const myJson = await response.json();
      console.log(myJson);
    };

    onMounted(() => {
      getCurrentUserDatas();
      getCurrentPosition();
    });

    return {
      model,
      createPost,
      convertFileToBase64,
    };
  },
});
</script>
