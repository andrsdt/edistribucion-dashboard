import { gql, useQuery } from "@apollo/client";
import { client } from "../lib/apolloClient";
import dayjs from "@/lib/dayjs";

const QUERY = gql`
	query GetMonthlyAccumulatedElectricityData($month: String!) {
		accumulatedMonthlyData(month: $month) {
			date
			accumulatedValue
		}
	}
`;

export default function useAccumulatedMonthly(date: Date) {
	const firstDayOfMonth = dayjs(date).startOf("month").format("YYYY-MM-DD");
	const { loading, error, data } = useQuery(QUERY, {
		variables: {
			month: firstDayOfMonth,
		},
		client: client,
	});

	// Format X axis as single days (1, 2, 3, ..., 31)
	const formattedData = data?.accumulatedMonthlyData.map((item: any) => {
		return {
			...item,
			date: dayjs(item.date).format("D"),
		};
	});

	return {
		loadingMonthly: loading,
		errorMonthly: error,
		dataMonthly: formattedData,
	};
}
