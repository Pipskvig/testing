import Vue from "vue";
import { ApolloClient } from 'apollo-client'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import './plugins/vuetify'
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueApollo from "vue-apollo";

Vue.config.productionTip = false;

Vue.use(VueApollo)

// HTTP connexion to the API
const httpLink = new HttpLink({
    // You should use an absolute URL here
    uri: 'http://localhost:8000/graphql/',
})

// Cache implementation
const cache = new InMemoryCache()

// Create the apollo client
const apolloClient = new ApolloClient({
    link: httpLink,
    cache,
})

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
});

new Vue({
  el: '#app',
  router,
  store,
  apolloProvider,
  render: h => h(App)
}).$mount("#app");
