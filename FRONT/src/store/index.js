import Vue from "vue";
import Vuex from "vuex";

export default new Vuex.Store({
  state: {
    accessToken: "",
    refreshToken: "",
  },
  mutations: {
    SET_ACCESS_TOKEN(state, accessToken) {
      state.accessToken = accessToken;
    },
    SET_REFRESH_TOKEN(state, refreshToken) {
      state.refreshToken = refreshToken;
    },
  },
  actions: {
    setAccessToken({ commit }, accessToken) {
      commit("SET_ACCESS_TOKEN", accessToken);
    },
    setRefreshToken({ commit }, refreshToken) {
      commit("SET_REFRESH_TOKEN", refreshToken);
    },
  },
});
