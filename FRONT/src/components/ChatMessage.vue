<template>
  <div>
    <q-toolbar class="bg-positive q-ma-none">
      <q-toolbar-title class="text-white">
        Conversation avec NOM
      </q-toolbar-title>
    </q-toolbar>
    <div class="column">
      <div class="col-10 q-pa-md">
        <div class="q-pa-md row justify-center">
          <div style="width: 100%; max-width: 50vw">
            <q-chat-message
              name="me"
              avatar="https://cdn.quasar.dev/img/avatar1.jpg"
              :text="['hey, how are you?']"
              stamp="7 minutes ago"
              sent
              bg-color="amber-7"
            />
            <q-chat-message
              name="Jane"
              avatar="https://cdn.quasar.dev/img/avatar5.jpg"
              :text="['doing fine, how r you?']"
              stamp="4 minutes ago"
              text-color="white"
              bg-color="primary"
            />
          </div>
        </div>
      </div>
      <div class="col-2 absolute-bottom">
        <div class="row items-center" style="max-width: 50vw; margin: auto">
          <q-input
            rounded
            outlined
            v-model="model.message"
            label="Ecrire un message..."
            class="col"
          />
          <q-btn
            round
            color="primary"
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

    const getMessage = async () => {
      let body = {
        message: {
          id: 12,
        },
        token: {
          accessToken: accessToken,
        },
      };
      body = JSON.stringify(body);
      const response = await fetch(
        "http://127.0.0.1:8000/conversation/GetMessage/",
        {
          method: "POST",
          body: body,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const myJson = await response.json();
      console.log("getMessage:", myJson);
    };

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
      await getMessage();
      //location.reload();
    };
    return { model, addMessage };
  },
});
</script>
