import { gql, useQuery } from "@apollo/client";
import { client } from "../lib/apolloClient";
import dayjs from "dayjs";

const QUERY = gql`
	query GetElectricityData($startDate: String!, $endDate: String!) {
		dailyMeasurements(startDate: $startDate, endDate: $endDate) {
			date
			measurements {
				hour
				value
			}
		}
	}
`;

export default function useDailyMeasures(date: Date) {
	const dateStr = dayjs(date).format("YYYY-MM-DD");
	const { loading, error, data } = useQuery(QUERY, {
		variables: {
			startDate: dateStr,
			endDate: dateStr,
		},
		client: client,
	});

	const hasData = data?.dailyMeasurements.length > 0;

	return {
		loadingDaily: loading,
		errorDaily: error,
		dataDaily: hasData ? data.dailyMeasurements[0].measurements : {},
	};
}
