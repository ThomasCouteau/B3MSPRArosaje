<script>
import { defineComponent, onMounted, onBeforeUnmount } from "vue";
import { useQuasar, QSpinnerIos } from "quasar";

export default defineComponent({
  name: "LoaderCustom",
  props: {
    isLoaded: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const $q = useQuasar();

    const showLoading = async () => {
      $q.loading.show({
        spinner: QSpinnerIos,
        spinnerSize: 140,
        spinnerColor: "primary",
        backgroundColor: "black",
      });

      let timer = setTimeout(() => {
        $q.loading.hide();
        timer = void 0;
      }, 3000);
    };

    onMounted(() => {
      showLoading();
    });

    onBeforeUnmount(() => {
      if (timer !== void 0) {
        clearTimeout(timer);
        $q.loading.hide();
      }
    });
  },
});
</script>
