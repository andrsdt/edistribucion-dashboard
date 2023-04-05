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

// NOTE: using March 19, 2023 as the date for testing purposes,
// since the API doesn't have data for the current date.
const today = new Date(2023, 2, 19);
const HOUR_OFFSET = 2;

const firstDayOfMonth = new Date(
  today.getFullYear(),
  today.getMonth(),
  1,
  HOUR_OFFSET
)
  .toISOString()
  .split("T")[0];

// YYYY-mm-dd format (korean locale)
const lastDayOfMonth = new Date(
  today.getFullYear(),
  today.getMonth() + 1,
  0,
  HOUR_OFFSET
)
  .toISOString()
  .split("T")[0];

export default function useMonthMeasures() {
  const { loading, error, data } = useQuery(QUERY, {
    variables: {
      startDate: firstDayOfMonth,
      endDate: lastDayOfMonth,
    },
    client: client,
  });

  return { loading, error, data };
}
