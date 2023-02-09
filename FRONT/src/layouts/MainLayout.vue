<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer persistent show-if-above bordered>
      <q-list>
        <h6 class="text-h6 q-ml-lg" header>A'rosa-je</h6>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        >
          <div v-if="link.title == 'Déconnexion'" @click="logout"></div>
        </EssentialLink>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";
import EssentialLink from "components/EssentialLink.vue";
import { useRouter } from "vue-router";

const linksList = [
  {
    title: "Accueil",
    icon: "home",
    link: "/home",
  },
  {
    title: "Recherche",
    icon: "search",
    link: "/search",
  },
  {
    title: "Messages",
    icon: "send",
    link: "/box",
  },
  {
    title: "Créer",
    icon: "add_box",
    link: "/create-post",
  },
  {
    title: "Profil",
    icon: "person",
    link: "/profile",
  },
  {
    title: "Déconnexion",
    icon: "logout",
    link: "/",
  },
];

export default defineComponent({
  name: "MainLayout",

  components: {
    EssentialLink,
  },

  setup() {
    const route = useRouter();

    const logout = async () => {
      let tokens = {
        accessToken: localStorage.getItem("accessToken"),
        refreshToken: localStorage.getItem("refreshToken"),
      };
      tokens = JSON.stringify(tokens);
      const response = await fetch("http://127.0.0.1:8000/user/logout", {
        method: "POST",
        body: tokens,
        headers: {
          "Content-Type": "application/json",
        },
      });
      const myJson = await response.json();
      console.log(myJson);
      if (response.status == "200") {
        route.push("/");
      }
    };

    return {
      essentialLinks: linksList,
      logout,
    };
  },
});
</script>
