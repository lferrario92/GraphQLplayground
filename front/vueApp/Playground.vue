<style scoped>
.container {
  font-family: 'Quicksand' !important;
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

ul {
  display: flex;
  list-style-type: none;
  padding: 0;
  max-width: 100%;
  flex-wrap: wrap;
}

.formContainer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.IdMen {
  position: absolute;
  top: -1px;
  left: -1px;
  color: white;
  background: red;
  border: solid 1px #ddd;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
}

.deleteItem {
  position: absolute;
  top: -8px;
  right: -8px;
  cursor: pointer;
  color: #464646;
  background: #ddd;
  border: solid 1px #464646;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
}

li {
  display: flex;
  position: relative;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  align-items: center;
  width: 90px;
  padding: 10px;
  border: solid 1px #ddd;
  margin: 5px;
}

p {
  margin: 0;
}

.labelMen {
  width: 100%;
  max-width: 220px;
}

.labelMen > input {
  border-radius: 4px;
  border:  solid 1px #ddd;
  padding: 5px;
  height: 30px;
  margin-bottom: 10px;
}

.labelMen > select {
  margin-bottom: 10px;
  border-radius: 4px;
  border:  solid 1px #ddd;
  padding: 5px;
  width: 100%;
  max-width: 220px;
  height: 30px;
  background: white;
}

.submenButton {
  background: red;
  color: white;
  border-radius: 4px;
  height: 30px;
  font-size: 14px;
  border: none;
  width: 100%;
  max-width: 220px;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>

<template>
  <section>
  <h1>Playground</h1>
  <div class="container">
    <div class="formContainer">
      <h2>Add ingredient</h2>
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
        <button class="submenButton" type="submit">Submit</button>
      </form>
    </div>
  </div>
  <div class="container">
    <div class="list-container">
      <h2>Ingredients</h2>
      <ul>
        <li v-for="ingredient in ingredients" :key="ingredient.id">
          <p class="IdMen">
            {{ ingredient.id }}
          </p>
          <span class="bold">{{ ingredient.name }}</span>
          <span style="color: blue">
            ({{ ingredient.category.name }})
          </span>
          <div 
            class="deleteItem"
            @click="deleteMe(ingredient.id, ingredient.name)"
            >
            X
          </div>
        </li>
      </ul>
    </div>
    <div class="list-container">
      <h2>Categories</h2>
      <ul>
        <li v-for="category in categories" :key="category.id">
          <p class="IdMen" style="background: blue">
            {{ category.id }}
          </p>
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
import DeleteIngredientMutation from './mutations/DeleteIngredientMutation.graphql'

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
      update: (store, { data: { createIngredient: { ingredient } } }) => {
        if (ingredient) {
          const data = store.readQuery({ query: QuerySample });
          data.ingredients.push(ingredient);
          store.writeQuery({ query: QuerySample, data })
        }
      },
      optimisticResponse: {
        createIngredient: {
          ok: true,
          errors: null,
          ingredient: {
            id: '-1',
            name: form_data.ingredient_name,
            __typename: 'IngredientType',
            category: form_data.category,
          },
          __typename: 'CreateIngredientMutation',
        }
      }
    });
   },
   deleteMe: function(id) {
    this.$apollo.mutate({
      mutation: DeleteIngredientMutation,
      variables: {
        ingredientId: id,
      }
    });
   }
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
