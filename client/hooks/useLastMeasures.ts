import { gql, useQuery } from "@apollo/client";
import { client } from "../lib/apolloClient";

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

const latestDayStr = new Date().toISOString().split("T")[0];
// const latestDay = new Date();
// latestDay.setDate(latestDay.getDate() - 1);
// const latestDayStr = latestDay.toISOString().split('T')[0];

export default function useLastMeasures() {
  const { loading, error, data } = useQuery(QUERY, {
    variables: {
      startDate: latestDayStr,
      endDate: latestDayStr,
    },
    client: client,
  });

  return { loading, error, data: data?.dailyMeasurements[0].measurements };
}
