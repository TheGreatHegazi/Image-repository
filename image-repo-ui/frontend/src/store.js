import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
  token: null,
  isLoggedIn: false, 
  user: null,
};

  const mutations = {
  
    setToken(state, token) {
      state.token = token;
    },
    setUser(state, user) {
        state.user = user;
      },
    setIsLoggedIn(state, isLoggedIn) {
        state.isLoggedIn = isLoggedIn;
      },
  };
  const actions = {
    setToken({ commit }, token) {
      commit("setToken", token);
    },
    setUser({ commit }, user) {
        commit("setUser", user);
      },
    setIsLoggedIn({ commit }, isLoggedIn) {
        commit("setIsLoggedIn", isLoggedIn);
      },
  };
  
export default new Vuex.Store({
  state, 
  mutations, 
  actions
});
