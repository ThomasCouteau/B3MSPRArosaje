<template>
  <q-page class="flex flex-center subscribe-bg">
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
              <q-radio
                v-model="model.userTypeID"
                val="3"
                label="Gardien/Utilisateur"
              />
            </div>
            <div class="row items-center">
              <q-checkbox class="col-4" v-model="accepted" />
              <span class="col-4 q-ma-sm text-no-wrap">
                Accepter la
                <a target="_blank" class="my-cgu" :href="API_URL + '/file/CGU/'"
                  >CGU</a
                >
              </span>
            </div>

            <q-btn
              :disable="!accepted"
              color="secondary"
              label="Créer"
              class="q-mt-md self-center"
              style="width: 150px"
              @click="createUser"
            />
          </q-form>
        </div>
      </q-card-section>
    </q-card>
    <div class="column self-end q-ma-md">
      <q-btn color="primary" label="Retour" href="/" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { API_URL } from "../utils/utils.js";

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

    let accepted = ref(false);

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
      const response = await fetch(API_URL + "/user/register", {
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
      accepted,
      API_URL,
    };
  },
});
</script>

<style lang="scss">
.my-card {
  max-width: 310px;
}
img {
  pointer-events: none;
}
.subscribe {
  text-decoration: none;
  color: $primary;
}

.my-cgu {
  color: $info;
  text-decoration: none;
}

//mobile
@media screen and (max-width: 600px) {
  .subscribe-bg {
    background-image: url("/helper/subscribe.svg");
    background-size: cover;
    background-position: top;
    background-repeat: no-repeat;
  }
}

//desktop
@media screen and (min-width: 600px) {
  .subscribe-bg {
    background-image: url("/helper/subscribe.svg");
    background-size: contain;
    background-position: right;
    background-repeat: no-repeat;
  }
}
</style>
