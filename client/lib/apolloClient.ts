import { ApolloClient, InMemoryCache } from "@apollo/client";

export const client = new ApolloClient({
  uri: `${process.env.NEXT_PUBLIC_BACKEND_URL}/graphql`, // Replace with the URL of your GraphQL server
  cache: new InMemoryCache(),
});
