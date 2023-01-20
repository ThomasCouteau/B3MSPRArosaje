<template>
  <q-page class="q-ma-none">
    <MessagesBoxComponent />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import MessagesBoxComponent from "src/components/MessagesBoxComponent.vue";

export default defineComponent({
  name: "MessagesBoxPage",
  components: {
    MessagesBoxComponent,
  },
});
</script>
