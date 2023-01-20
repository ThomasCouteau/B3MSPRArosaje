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
            v-model="text"
            label="Ecrire un message..."
            class="col"
          />
          <q-btn
            round
            color="primary"
            icon="send"
            class="q-ml-sm"
            :disable="!text"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "ChatMessage",
  props: {},
  setup() {
    const text = ref("");
    return { text };
  },
});
</script>
