<template>
  <q-page>
    <div class="text-h3 text-center q-ma-md">Créer un post</div>
    <div class="column items-center q-ma-md">
      <q-input
        stack-label
        clearable
        filled
        v-model="model.name"
        label="Nom de la plante"
        class="q-ma-md"
        style="width: 50vw"
      />
      <!--
        Due to browser security policy,
        we can only read the value, but not
        write to it, so we only have an @update:model-value listener
      -->

      <q-input
        @update:model-value="
          (val) => {
            fileToConvert = val[0];
          }
        "
        filled
        stack-label
        label="Photos de la plante"
        type="file"
        class="q-ma-md"
        style="width: 50vw"
      />
      <q-input
        v-model="model.description"
        filled
        clearable
        type="textarea"
        stack-label
        label="Description"
        class="q-ma-md"
        style="width: 50vw"
      />
      <q-btn
        class="q-ma-md"
        color="primary"
        label="Créer"
        @click="createPost"
      />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "CreatePostPage",

  setup() {
    const model = ref({
      name: "",
      file: null,
      description: "",
    });
    const fileToConvert = ref(null);
    const blob = new Blob([fileToConvert], { type: "image/png" });
    const convertImageToBase64 = (toConvert) => {
      const reader = new FileReader();
      reader.readAsDataURL(toConvert);
      reader.onload = () => {
        console.log(reader.result);
        model.value.file = reader.result;
      };
      reader.onerror = (error) => {
        console.log("Error: ", error);
      };
    };

    const createPost = () => {
      convertImageToBase64(blob);
      console.log(model.value);
    };
    return {
      model,
      fileToConvert,
      convertImageToBase64,
      createPost,
    };
  },
});
</script>
