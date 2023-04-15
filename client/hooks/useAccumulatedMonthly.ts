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

const currentDate = new Date();
currentDate.setDate(1);
const month = currentDate.toISOString().slice(0, 10);

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
