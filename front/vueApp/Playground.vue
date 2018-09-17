<style scoped>
.container {
  display: flex;
  flex-direction: row;
}
.list-container {
  max-width: 50%;
  width: 100%;
}
.bold {
  font-weight: 600;
}

.labelMen > input {
  border-radius: 4px;
  border:  solid 1px #ddd;
  padding: 5px;
}

.labelMen > select {
  border-radius: 4px;
  border:  solid 1px #ddd;
  padding: 5px;
}

</style>

<template>
  <section>
  <h1>Playground</h1>
  <div class="container">
    <div>
      <h2>Add ingredient Men</h2>
      <form v-on:submit.prevent="createIngredientMutation">
        <label class="labelMen">
          <input 
            placeholder="Name" 
            type="text"
            v-model="ingredient_name"
            >
        </label>
        <label class="labelMen">
          <input 
            placeholder="Notes" 
            type="text"
            v-model="notes"
            >
        </label>
        <label class="labelMen">
          <select v-model="category">
            <option 
              v-for="cat in categories"
              :value="cat"
              >{{ cat.name }}</option>
          </select>
        </label>
        <button type="submit">subMen</button>
      </form>
    </div>
  </div>
  <div class="container">
    <div class="list-container">
      <h2>Ingredients</h2>
      <ul>
        <li v-for="ingredient in ingredients" :key="ingredient.id">
          {{ ingredient.id }} -
          <span class="bold">{{ ingredient.name }}</span>
          ({{ ingredient.category.name }})
        </li>
      </ul>
    </div>
    <div class="list-container">
      <h2>Categories</h2>
      <ul>
        <li v-for="category in categories" :key="category.id">
          {{ category.id }} -
          <span class="bold">{{ category.name }}</span>
        </li>
      </ul>
    </div>
  </div>
  </section>
</template>


<script>
import Vue from 'vue';
import queryString from 'query-string';
import { ApolloClient } from 'apollo-client'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import VueApollo from 'vue-apollo'

import QuerySample from './queries/query.graphql'
import CreateIngredientMutation from './mutations/CreateIngredientMutation.graphql'

Vue.use(VueApollo)

const httpLink = new HttpLink({
    // You should use an absolute URL here
    uri: '/graphql',
    fetch: customFetchWithCsrfToken,
})

const apolloClient = new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
    connectToDevTools: true,
})

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
})

export default {
  apolloProvider,
  apollo: {
      ingredients: QuerySample,
      categories: QuerySample,
  },
  data: {
    form_data: {},
    ingredient_name: null,
    notes: null,
    category: Number,
  },
  methods: {
   createIngredientMutation: function() {
    if(!this.ingredient_name || !this.notes) {
      alert('no men');
      return false;
    }
    const form_data = {
      ingredient_name: this.ingredient_name,
      notes: this.notes,
      category: this.category,
    };
    this.$apollo.mutate({
      mutation: CreateIngredientMutation,
      variables: {
        name: form_data.ingredient_name,
        notes: form_data.notes,
        category: form_data.category.id,
      },
    });
   },
  },
};

function customFetchWithCsrfToken(uri, options) {
    options.headers['X-CSRFToken'] = readCookie('csrftoken');
    return customFetch(uri, options);
}

function customFetch(uri, options) {
  const gqlParams = JSON.parse(options.body);
  const queryParams = {
    operationName: gqlParams.operationName,
  };
  if (gqlParams.query.startsWith('query ')) {
    options.method = 'GET';
    queryParams.query = gqlParams.query;
    queryParams.variables = JSON.stringify(gqlParams.variables);
    delete options.body;
    delete options.headers['content-type'];
  }
  uri += `?${queryString.stringify(queryParams)}`;
  return fetch(uri, options);
}

function readCookie(key) {
  const r = RegExp(`(^|; )${encodeURIComponent(key)}=([^;]*)`).exec(document.cookie);
  return r ? r[2] : null;
}
</script>
