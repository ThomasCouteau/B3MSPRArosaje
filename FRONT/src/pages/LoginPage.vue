<template>
  <q-page class="flex flex-center">
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
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "LoginPage",
  components: {},
  setup() {
    const route = useRouter();
    const model = ref({
      pseudo: "",
      password: "",
    });

    const loginUser = async () => {
      let logs = {
        pseudo: model.value.pseudo,
        password: model.value.password,
      };
      logs = JSON.stringify(logs);
      const response = await fetch("http://127.0.0.1:8000/user/login", {
        method: "POST",
        body: logs,
        headers: {
          "Content-Type": "application/json",
        },
      });
      const myJson = await response.json();
      console.log(myJson);

      if (response.status == "200") {
        localStorage.setItem("accessToken", myJson.accessToken);
        localStorage.setItem("refreshToken", myJson.refreshToken);
        localStorage.setItem("userID", myJson.userID);
        route.push("/home");
      }
    };

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
</style>
