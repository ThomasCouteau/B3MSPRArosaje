<template>
  <q-page>
    <ChatMessage />
  </q-page>
  <LoaderCustom />
</template>

<script>
import { defineComponent, onMounted } from "vue";
import ChatMessage from "src/components/ChatMessage.vue";
import LoaderCustom from "src/components/LoaderCustom.vue";
import { useQuasar } from "quasar";
import { Dialog } from "quasar";

export default defineComponent({
  name: "ConvPage",
  components: {
    ChatMessage,
    LoaderCustom,
  },
  setup() {
    const $q = useQuasar();
    const privateMessages = localStorage.getItem("privateMessages");

    const confirmMsg = () => {
      if (privateMessages) {
        return;
      }
      if (!privateMessages) {
        $q.dialog({
          title: "Informations personnelles",
          message: "Veuillez ne partager que les informations nécessaires.",
          cancel: false,
          persistent: true,
        })
          .onOk(() => {
            let msg = localStorage.setItem("privateMessages", true);
          })
          .onOk(() => {})
          .onDismiss(() => {});
      }
    };

    onMounted(() => {
      confirmMsg();
    });
  },
});
</script>
