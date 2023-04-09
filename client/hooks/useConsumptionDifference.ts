import { gql, useQuery } from '@apollo/client';
import { client } from '../lib/apolloClient';

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
    data: data?.consumptionDifference,
  };
}
