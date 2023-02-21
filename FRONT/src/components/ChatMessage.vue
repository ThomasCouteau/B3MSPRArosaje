<template>
  <div>
    <q-toolbar class="bg-secondary q-ma-none">
      <q-toolbar-title class="text-white"> Conversation </q-toolbar-title>
    </q-toolbar>
    <div class="column">
      <div class="col-10 q-pa-md">
        <div class="q-pa-md row justify-center">
          <div
            style="width: 100%; max-width: 50vw"
            :key="index"
            v-for="(message, index) in allMessages.slice().reverse()"
          >
            <div v-if="message.sender.id == userID">
              <q-chat-message
                :name="message.sender.pseudo"
                :avatar="message.sender.picture"
                :text="[message.message]"
                sent
                bg-color="positive"
              />
            </div>
            <div v-if="message.sender.id != userID">
              <q-chat-message
                :name="message.sender.pseudo"
                :avatar="message.sender.picture"
                :text="[message.message]"
                text-color="white"
                bg-color="primary"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="col-2">
        <div class="row items-center" style="max-width: 550px; margin: auto">
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
      const response = await fetch("http://127.0.0.1:8000/conversation/Get/", {
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
    });

    const accessToken = localStorage.getItem("accessToken");
    const route = useRoute();
    const userID = localStorage.getItem("userID");

    const addMessage = async () => {
      let body = {
        message: {
          message: model.value.message,
          image: "",
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(
        "http://127.0.0.1:8000/conversation/" + route.params.id + "/add/",
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
    return { model, addMessage, userID };
  },
});
</script>
