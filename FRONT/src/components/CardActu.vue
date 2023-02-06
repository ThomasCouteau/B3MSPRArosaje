<template>
  <q-card class="my-card">
    <q-item>
      <q-item-section avatar>
        <q-avatar>
          <img src="https://cdn.quasar.dev/img/avatar2.jpg" />
        </q-avatar>
      </q-item-section>

      <q-item-section>
        <q-item-label>Propriétaire</q-item-label>
      </q-item-section>
    </q-item>
    <img src="https://cdn.quasar.dev/img/mountains.jpg" />

    <q-card-section class="q-pt-none">
      <div class="text-h6">Nom plante</div>
      <p class="text-body1">
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nemo eligendi
        iste culpa fuga mollitia quibusdam voluptatem delectus consequatur
        dolorum inventore. In maxime blanditiis accusantium iure? Vero veritatis
        esse dolorem temporibus?
      </p>
      <q-separator />
      <div class="row items-center">
        <div class="col-10">
          <q-input v-model="text" borderless label="Commentaires" />
        </div>
        <div class="col-2">
          <q-btn flat rounded color="primary" label="Publier" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "CardActu",
  props: {},
});
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  height: 100%
  max-height: 120vh
  max-width: 50vw
</style>
