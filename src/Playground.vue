<template>
    <div>
        test

        {{ingredients}}
    </div>
</template>


<script>
import Vue from 'vue';
import queryString from 'query-string';
import { ApolloClient } from 'apollo-client'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import VueApollo from 'vue-apollo'

import QuerySample from './queries/query.graphql'

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
        men: {
            query: QuerySample,
            update: data => data,
            prefetch: true,
        },
    },
    computed: {
        ingredients() {
            return this.todo;
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
