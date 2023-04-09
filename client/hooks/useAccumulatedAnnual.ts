import { gql, useQuery } from '@apollo/client';
import { client } from '../lib/apolloClient';

const QUERY = gql`
  query GetYearAccumulatedElectricityData($year: Int!) {
    accumulatedData(year: $year) {
      date
      accumulatedValue
    }
  }
`;


const current_year = new Date().getFullYear()

export default function useAccumulatedAnnual() {
  const { loading, error, data } = useQuery(QUERY, {
    variables: {
      year: current_year,
    },
    client: client,
  });

  return {
    loading,
    error,
    barAnnualChartData: data?.accumulatedData,
  };
}
