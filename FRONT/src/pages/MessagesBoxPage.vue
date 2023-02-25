<template>
  <q-page class="q-ma-none">
    <div>
      <q-toolbar class="bg-positive q-ma-none">
        <q-toolbar-title class="text-white"> Messagerie </q-toolbar-title>
      </q-toolbar>
      <div v-if="allConversation.length != 0">
        <div
          :key="index"
          v-for="(conv, index) in allConversation.slice().reverse()"
          class=""
          style="max-width: 100%"
        >
          <q-list bordered>
            <q-item clickable v-ripple :to="'/conversation/' + conv.id">
              <q-item-section avatar>
                <q-avatar v-if="userID != conv.guardian.id">
                  <img :src="conv.guardian.picture" />
                </q-avatar>
                <q-avatar v-if="userID == conv.guardian.id">
                  <img :src="conv.owner.picture" />
                </q-avatar>
              </q-item-section>
              <q-item-section
                v-if="userID != conv.guardian.id"
                class="text-capitalize"
                >{{ conv.guardian.pseudo }}</q-item-section
              >
              <q-item-section
                v-if="userID == conv.guardian.id"
                class="text-capitalize"
                >{{ conv.owner.pseudo }}</q-item-section
              >
            </q-item>
            <q-separator />
          </q-list>
        </div>
      </div>
      <div v-else class="row justify-center">
        <div class="text-h6">Aucune conversation pour le moment...</div>
      </div>

      <div class="row justify-center">
        <select
          name="Gardien"
          v-model="model.selectedGardien"
          class="q-ma-md selected"
          :rules:="[(val) => !!val || 'Champ obligatoire']"
        >
          <option value="null" disabled>Choisir un gardien...</option>
          <option
            :value="gardien.id"
            :key="index"
            v-for="(gardien, index) in allGuardians"
          >
            {{ gardien.pseudo }}
          </option>
        </select>
      </div>
      <div class="row justify-center">
        <q-btn
          class="q-ma-md"
          color="secondary"
          label="Ecrire"
          @click="createConversationTo()"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { API_URL } from "../utils/utils.js";

export default defineComponent({
  name: "MessagesBoxPage",
  components: {},
  data() {
    return {
      allConversation: [],
      allBotanistes: [],
      allGuardians: [],
    };
  },
  mounted() {
    const accessToken = localStorage.getItem("accessToken");

    const getAllConversationOfUser = async () => {
      let body = {
        accessToken: accessToken,
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/conversation/", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      this.allConversation = await response.json();
      console.log("Conv", this.allConversation);
    };

    const getAllBotanistes = async () => {
      let body = {
        search: {
          isBotaniste: true, //si on veut les botanistes
          isGardien: false, //si on veut les gardiens
          isAdministrator: false, //si on veut les administrateurs
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/user/Search", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      this.allBotanistes = await response.json();
      console.log("allbotanistes", this.allBotanistes);
    };

    const getAllGardiens = async () => {
      let body = {
        search: {
          isBotaniste: false, //si on veut les botanistes
          isGardien: true, //si on veut les gardiens
          isAdministrator: false, //si on veut les administrateurs
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/user/Search", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      this.allGuardians = await response.json();
      console.log("allGardiens", this.allGuardians);
    };

    getAllConversationOfUser();
    getAllBotanistes();
    getAllGardiens();
  },
  setup() {
    const model = ref({
      selectedGardien: null,
    });

    const accessToken = localStorage.getItem("accessToken");
    const userID = localStorage.getItem("userID");

    const createConversationTo = async () => {
      let body = {
        conversation: {
          owner: {
            id: userID,
          },
          guardian: {
            id: model.value.selectedGardien,
          },
        },
        token: { accessToken: accessToken },
      };
      body = JSON.stringify(body);
      const response = await fetch(
        "https://arosaje-api.ibsolutions.cloud/conversation/add/",
        {
          method: "POST",
          body: body,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const myJson = await response.json();
      console.log(myJson);
      location.reload();
    };
    return { model, createConversationTo, userID };
  },
});
</script>

<style lang="scss">
.selected {
  width: 268px;
  height: 60px;
  background: #eeeeee;
  border-radius: 5px;
  border: none;
}
</style>
