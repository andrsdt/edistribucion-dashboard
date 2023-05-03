import { gql, useQuery } from "@apollo/client";
import { client } from "../lib/apolloClient";

const QUERY = gql`
	query GetYearAccumulatedElectricityData($year: Int!) {
		accumulatedData(year: $year) {
			date
			accumulatedValue
		}
	}
`;

export default function useAccumulatedAnnual(year: Date) {
	const { loading, error, data } = useQuery(QUERY, {
		variables: {
			year: year.getFullYear(),
		},
		client: client,
	});

	return {
		loadingYearly: loading,
		errorYearly: error,
		dataYearly: data?.accumulatedData,
	};
}
