import { gql, useQuery } from "@apollo/client";
import { client } from "../lib/apolloClient";
import dayjs from "@/lib/dayjs";

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

export const defaultData = Array.from({ length: 24 }, (_, i) => ({
	hour: i,
	value: undefined,
}));

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
	const dataDaily = hasData ? data.dailyMeasurements[0].measurements : [];

	return {
		loadingDaily: loading,
		errorDaily: error,
		dataDaily: loading ? defaultData : dataDaily,
	};
}
