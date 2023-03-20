<template>
  <q-page class="q-ma-md">
    <div class="text-h5 text-center">Rechercher une plante à garder</div>
    <div class="column items-center justify-center q-ma-md">
      <div class="col">
        <SearchPlantMap />
      </div>
    </div>
  </q-page>
  <LoaderCustom />
</template>

<script>
import { defineComponent } from "vue";
import SearchPlantMap from "components/SearchPlantMap.vue";
import LoaderCustom from "src/components/LoaderCustom.vue";

export default defineComponent({
  name: "MapPage",
  components: { SearchPlantMap, LoaderCustom },
});
</script>

<style lang="scss">
body {
  overflow: hidden;
}
</style>
