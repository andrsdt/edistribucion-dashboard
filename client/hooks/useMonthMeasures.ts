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

// NOTE: Used for "Tu consumo acumulado" in the sidebar
export default function useMonthMeasures(date: Date) {
	const firstDayOfMonth = dayjs(date).startOf("month").format("YYYY-MM-DD");
	const lastDayOfMonth = dayjs(date).endOf("month").format("YYYY-MM-DD");
	const { loading, error, data } = useQuery(QUERY, {
		variables: {
			startDate: firstDayOfMonth,
			endDate: lastDayOfMonth,
		},
		client: client,
	});

	return { loading, error, data: data };
}
