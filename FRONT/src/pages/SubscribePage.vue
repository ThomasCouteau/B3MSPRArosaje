<template>
  <q-page class="flex flex-center">
    <q-card flat bordered class="my-card" style="width: 310px">
      <q-card-section>
        <div class="text-center">
          <img src="/helper/leaf-green.png" alt="" width="100" height="100" />
          <div class="text-h6">Création de compte</div>
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="q-mt-md">
          <q-form class="column">
            <q-input
              v-model="model.pseudo"
              label="Login"
              filled
              stack-label
              :rules="[
                (val) => (val && val.length > 0) || 'Veuillez entrer un login',
              ]"
            />
            <q-input
              v-model="model.password"
              label="Mot de passe"
              filled
              stack-label
              type="password"
              :rules="[
                (val) =>
                  (val && val.length > 0) || 'Veuillez entrer un mot de passe',
              ]"
            />
            <q-file
              filled
              v-model="model.picture"
              label="Photo de profil"
              stack-label
              @update:model-value="
                async (val) => (fileToConvert = await convertFileToBase64(val))
              "
            />
            <div class="q-gutter-sm">
              <q-radio v-model="model.userTypeID" val="1" label="Botaniste" />
              <q-radio v-model="model.userTypeID" val="3" label="Gardien" />
            </div>
            <q-btn
              color="primary"
              label="Créer"
              class="q-mt-md self-center"
              style="width: 150px"
              @click="createUser"
            />
          </q-form>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "SubscribePage",
  components: {},
  setup() {
    const route = useRouter();
    const model = ref({
      pseudo: "",
      password: "",
      userTypeID: "",
      picture: null,
    });

    let fileToConvert = null;

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

    const createUser = async () => {
      model.value.picture = fileToConvert;
      let body = {
        pseudo: model.value.pseudo,
        password: model.value.password,
        userTypeID: model.value.userTypeID,
        picture: model.value.picture,
      };
      body = JSON.stringify(body);
      console.log(body);
      const response = await fetch("http://127.0.0.1:8000/user/register", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      route.push("/");
    };

    return {
      model,
      createUser,
      convertFileToBase64,
    };
  },
});
</script>

<style lang="scss">
.my-card {
  max-width: 310px;
  margin: auto;
}
img {
  pointer-events: none;
}
.subscribe {
  text-decoration: none;
  color: $primary;
}
</style>
