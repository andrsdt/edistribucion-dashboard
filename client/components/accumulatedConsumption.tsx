import useMonthMeasures from "@/hooks/useMonthMeasures";
import { getCumulativeData } from "@/utils/getCumulativeData";
import { AreaChart, Card, Title } from "@tremor/react";

export default function AccumulatedConsumption() {
  const { loading, error, data } = useMonthMeasures();
  const accumulatedMeasures = getCumulativeData(data);
  const currentDate = new Date();
  const month = currentDate.toLocaleDateString('es-ES', { month: 'long' });
  const formattedMonth = month.charAt(0).toUpperCase() + month.slice(1);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <Card>
      <Title>Tu consumo ({formattedMonth} 2023)</Title>
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
