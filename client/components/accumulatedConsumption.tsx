import useMonthMeasures from "@/hooks/useMonthMeasures";
import { getCumulativeData } from "@/utils/getCumulativeData";
import { AreaChart, Card, Title } from "@tremor/react";

export default function AccumulatedConsumption() {
  const { loading, error, data } = useMonthMeasures();
  const accumulatedMeasures = getCumulativeData(data);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <Card>
      <Title>Tu consumo (Marzo 2023)</Title>
      <AreaChart
        data={accumulatedMeasures}
        index="date"
        categories={["value"]}
        colors={["blue"]}
        yAxisWidth={20}
        showLegend={false}
      />
    </Card>
  );
}
