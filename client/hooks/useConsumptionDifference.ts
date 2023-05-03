import { gql, useQuery } from "@apollo/client";
import { client } from "../lib/apolloClient";

const QUERY = gql`
	query GetConsumptionDifference($month: String!) {
		consumptionDifference(month: $month) {
			accumulativeData {
				date
				accumulatedValue
			}
			delta
			deltaType
		}
	}
`;

// DefaultData used to show something when data is not loaded yet
const defaultData = {
	accumulativeData: [
		{
			date: "2021-01-01",
			accumulatedValue: 0,
		},
		{
			date: "2021-01-01",
			accumulatedValue: 0,
		},
	],
	delta: 0,
	deltaType: "unchanged",
};

const currentDate = new Date();
currentDate.setDate(1);
const month = currentDate.toISOString().slice(0, 10);

export default function useConsumptionDifference() {
	const { loading, error, data } = useQuery(QUERY, {
		variables: {
			month: month,
		},
		client: client,
	});

	return {
		loading,
		error,
		data: data?.consumptionDifference || defaultData,
	};
}
