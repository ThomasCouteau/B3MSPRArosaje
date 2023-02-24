<template>
  <q-page class="">
    <ChatMessage />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import ChatMessage from "src/components/ChatMessage.vue";

export default defineComponent({
  name: "ConvPage",
  components: {
    ChatMessage,
  },
});
</script>
