<template>
  <q-page class="q-ma-md">
    <div class="text-h4 text-center">Fil d'actualité</div>
    <div class="column items-center justify-center q-ma-md">
      <div class="col">
        <CardActu />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import CardActu from "components/CardActu.vue";

export default defineComponent({
  name: "IndexPage",
  components: {
    CardActu,
  },
});
</script>
