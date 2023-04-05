import useLastMeasures from "@/hooks/useLastMeasures";
import { getCumulativeData } from "@/utils/getCumulativeData";
import { AreaChart, Card, Title } from "@tremor/react";

export default function AccumulatedConsumption() {
  const measures = useLastMeasures();
  const accumulatedMeasures = getCumulativeData(measures);

  return (
    <Card>
      <Title>Tu consumo (Marzo 2023)</Title>
      <AreaChart
        data={accumulatedMeasures}
        index="hourCCH"
        categories={["valueDouble"]}
        colors={["blue"]}
        yAxisWidth={20}
        showLegend={false}
      />
    </Card>
  );
}
