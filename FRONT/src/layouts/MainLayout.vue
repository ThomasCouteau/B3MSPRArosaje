<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer persistent show-if-above bordered>
      <q-list>
        <h6 class="text-h6 q-ml-lg" header>A'rosa-je</h6>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
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

const linksList = [
  {
    title: "Accueil",
    icon: "home",
    link: "/",
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
    return {
      essentialLinks: linksList,
    };
  },
});
</script>
