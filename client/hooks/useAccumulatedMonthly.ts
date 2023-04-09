import { gql, useQuery } from '@apollo/client';
import { client } from '../lib/apolloClient';

const QUERY = gql`
  query GetMonthlyAccumulatedElectricityData($month: String!) {
    accumulatedMonthlyData(month: $month) {
      date
      accumulatedValue
    }
  }
`;

const month = "2023-04-01"

export default function useAccumulatedMonthly() {
  const { loading, error, data } = useQuery(QUERY, {
    variables: {
      month: month,
    },
    client: client,
  });

  return {
    loading,
    error,
    barMonthlyChartData: data?.accumulatedMonthlyData,
  };
}
