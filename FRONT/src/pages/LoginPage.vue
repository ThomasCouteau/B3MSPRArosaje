<template>
  <q-page class="flex flex-center login">
    <q-card flat bordered class="my-card">
      <q-card-section>
        <div class="text-center">
          <img src="/helper/leaf-green.png" alt="" width="100" height="100" />
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="q-mt-md">
          <q-form class="column">
            <q-input
              v-model="model.pseudo"
              label="Login"
              filled
              :rules="[
                (val) =>
                  (val && val.length > 0) || 'Veuillez entrer votre login',
              ]"
            />
            <q-input
              v-model="model.password"
              label="Mot de passe"
              filled
              type="password"
              :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Veuillez entrer votre mot de passe',
              ]"
            />
            <q-btn
              color="secondary"
              label="Se connecter"
              class="q-mt-md self-center"
              style="width: 150px"
              @click="loginUser"
            />
          </q-form>
        </div>
      </q-card-section>

      <q-separator inset />

      <q-card-section>
        Vous n'avez pas de compte ?
        <a class="subscribe text-subtitle2" href="/subscribe">Inscrivez-vous</a>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { API_URL } from "../utils/utils.js";
import { useQuasar } from "quasar";
import { Dialog } from "quasar";

export default defineComponent({
  name: "LoginPage",
  components: {},
  setup() {
    const route = useRouter();
    const $q = useQuasar();
    const model = ref({
      pseudo: "",
      password: "",
    });

    const cookiesIsAccepted = localStorage.getItem("cookiesIsAccepted");

    const confirmCookies = () => {
      if (cookiesIsAccepted) {
        return;
      }
      if (!cookiesIsAccepted) {
        $q.dialog({
          title: "Confirmer l'utilisation des cookies",
          message:
            "En poursuivant votre navigation sur ce site, vous acceptez l'utilisation de cookies pour vous proposer des services adaptés à vos centres d'intérêts.",
          cancel: false,
          persistent: true,
        })
          .onOk(() => {
            let cookies = localStorage.setItem("cookiesIsAccepted", true);
          })
          .onOk(() => {})
          .onDismiss(() => {});
      }
    };

    const loginUser = async () => {
      let logs = {
        pseudo: model.value.pseudo,
        password: model.value.password,
      };
      logs = JSON.stringify(logs);
      const response = await fetch(API_URL + "/user/login", {
        method: "POST",
        body: logs,
        headers: {
          "Content-Type": "application/json",
        },
      });
      const myResponse = await response;

      if (response.status == "200") {
        const myJson = await myResponse.json();
        console.log(myJson);
        localStorage.setItem("accessToken", myJson.accessToken);
        localStorage.setItem("refreshToken", myJson.refreshToken);
        localStorage.setItem("userID", myJson.userID);
        localStorage.setItem("userTypeID", myJson.userTypeID);
        route.push("/home");
      }
      if (response.status == "401") {
        alert("Mauvais login ou mot de passe");
      }
    };

    onMounted(() => {
      confirmCookies();
    });

    return {
      model,
      loginUser,
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

//mobile
@media screen and (max-width: 600px) {
  .login {
    background-image: url("/helper/blooming.svg");
    background-size: cover;
    background-position: top;
    background-repeat: no-repeat;
  }
}

//desktop
@media screen and (min-width: 600px) {
  .login {
    background-image: url("/helper/blooming.svg");
    background-size: contain;
    background-position: right;
    background-repeat: no-repeat;
  }
}
</style>
