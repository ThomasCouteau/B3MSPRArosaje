<template>
  <q-page>
    <div class="text-h3 text-center q-ma-md">Votre profil</div>
    <q-card class="my-card">
      <q-card class="my-card" flat bordered>
        <q-card-section horizontal>
          <q-card-section>
            <q-avatar
              size="100px"
              font-size="52px"
              color="teal"
              text-color="white"
              icon="person"
            />
          </q-card-section>

          <q-separator vertical />

          <q-card-section>
            <div class="text-h6">Nom Prénom</div>
            <div class="text-subtitle2">Email</div>
            <div class="text-subtitle2">Rôle</div>
          </q-card-section>
        </q-card-section>
      </q-card>
    </q-card>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "ProfilePage",
});
</script>

<style lang="scss">
.my-card {
  width: 100%;
  height: 100%;
  max-height: 120vh;
  max-width: 50vw;
  margin: auto;
}
</style>
