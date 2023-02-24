<template>
  <div>
    <q-toolbar class="bg-secondary q-ma-none">
      <q-toolbar-title class="text-white"> Conversation </q-toolbar-title>
    </q-toolbar>
    <div class="column">
      <div class="col-10 q-ma-md">
        <div class="q-pa-md column">
          <div
            :key="index"
            v-for="(message, index) in allMessages.slice().reverse()"
            class="col"
          >
            <div v-if="message.sender.id == userID" class="column items-end">
              <q-chat-message
                :name="message.sender.pseudo"
                :avatar="message.sender.picture"
                :text="[message.message]"
                sent
                bg-color="positive"
                class="col"
              />
              <template v-if="message.picture">
                <img :src="message.picture" class="col chat-img" />
              </template>
            </div>
            <div v-if="message.sender.id != userID" class="column items-start">
              <q-chat-message
                :name="message.sender.pseudo"
                :avatar="message.sender.picture"
                :text="[message.message]"
                text-color="white"
                bg-color="primary"
                class="col"
              />
              <template v-if="message.picture">
                <img :src="message.picture" class="col chat-img" />
              </template>
            </div>
          </div>
        </div>
      </div>
      <div class="col-2">
        <div class="row items-center">
          <q-file
            rounded
            outlined
            v-model="model.picture"
            class="my-file q-mr-sm"
            @update:model-value="
              async (val) => (fileToConvert = await convertFileToBase64(val))
            "
            label="Img"
          />

          <q-input
            rounded
            outlined
            v-model="model.message"
            label="Ecrire un message..."
            class="col"
          />
          <q-btn
            round
            color="secondary"
            icon="send"
            class="q-ml-sm"
            :disable="!model.message"
            @click="addMessage"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useRoute } from "vue-router";
import { API_URL } from "../utils/utils.js";

export default defineComponent({
  name: "ChatMessage",
  props: {},
  data() {
    return {
      allMessages: [],
    };
  },
  mounted() {
    const accessToken = localStorage.getItem("accessToken");

    const getAllMessages = async () => {
      let body = {
        conversation: {
          id: this.$route.params.id,
        },

        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(API_URL + "/conversation/Get/", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      this.allMessages = await response.json();
      console.log("messages:", this.allMessages);
    };
    getAllMessages();
  },
  setup() {
    const model = ref({
      message: "",
      picture: null,
    });

    const accessToken = localStorage.getItem("accessToken");
    const route = useRoute();
    const userID = localStorage.getItem("userID");

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

    const addMessage = async () => {
      model.value.picture = fileToConvert;
      let body = {
        message: {
          message: model.value.message,
          picture: model.value.picture,
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      console.log("body:", body);
      const response = await fetch(
        API_URL + "/conversation/" + route.params.id + "/add/",
        {
          method: "POST",
          body: body,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const myJson = await response.json();
      console.log("addmessage:", myJson);
      location.reload();
    };
    return { model, addMessage, userID, convertFileToBase64 };
  },
});
</script>

<style lang="scss">
.my-file {
  width: 100%;
  max-width: 55px;
}
//mobile
@media screen and (max-width: 600px) {
  .chat-img {
    width: 100%;
    max-width: 50vw;
    border-radius: 24px;
  }
}
//desktop
@media screen and (min-width: 600px) {
  .chat-img {
    width: 100%;
    max-width: 20vw;
    border-radius: 24px;
  }
}
</style>
