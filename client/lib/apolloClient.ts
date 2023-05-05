import { BACKEND_URL } from "@/constants";
import { ApolloClient, InMemoryCache } from "@apollo/client";

export const client = new ApolloClient({
	uri: `${BACKEND_URL}/graphql`, // Replace with the URL of your GraphQL server
	cache: new InMemoryCache(),
});
