<template>
  <div>
    <q-toolbar class="bg-positive q-ma-none">
      <q-toolbar-title class="text-white"> Messagerie </q-toolbar-title>
    </q-toolbar>
    <div class="" style="max-width: 100%">
      <q-list bordered>
        <q-item clickable v-ripple to="/conversation/:id">
          <q-item-section avatar>
            <q-avatar>
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
            </q-avatar>
          </q-item-section>
          <q-item-section>Nom</q-item-section>
          <q-item-section side>Nb MSG</q-item-section>
        </q-item>
        <q-separator />
      </q-list>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "MessagesBoxComponent",
  props: {},
  setup() {
    return {};
  },
});
</script>
