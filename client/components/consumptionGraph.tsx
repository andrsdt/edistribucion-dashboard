import useLastMeasures from "@/hooks/useLastMeasures";
import useAccumulatedAnnual from '@/hooks/useAccumulatedAnnual';
import useAccumulatedMonthly from '@/hooks/useAccumulatedMonthly';
import {
  Card,
  Flex,
  LineChart,
  BarChart,
  Title,
  Toggle,
  ToggleItem,
} from "@tremor/react";

import { useState } from 'react';


// TODO: get latest available data for the linear chart
// TODO: possibility to change the month/day/year data being displayed
export default function ConsumptionGraph() {
  const { loading, error, data } = useLastMeasures();
  const { barAnnualChartData } = useAccumulatedAnnual();

  // TODO: maybe change this chart for one that adds more value, or maybe get the data for each day of the month
  const { barMonthlyChartData } = useAccumulatedMonthly();
  
  const [chartType, setChartType] = useState('1');

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const renderChart = () => {
    switch (chartType) {
      case '1':
        return (
          <LineChart
            className="mt-3"
            data={data}
            index="hour"
            categories={['value']}
            colors={['blue']}
            yAxisWidth={30}
          />
        );
      case '2':
        return (
          <BarChart
            className="mt-3"
            data={barMonthlyChartData}
            index="date"
            colors={['blue']}
            yAxisWidth={30}
            categories={['accumulatedValue']}
          />
        );  
      case '3':
        return (
          <BarChart
            className="mt-3"
            data={barAnnualChartData}
            index="date"
            colors={['blue']}
            yAxisWidth={30}
            categories={['accumulatedValue']}
          />
        );
    }
  };

  return (
    <Card>
      <Flex>
        <Title>Tu consumo</Title>
        <Toggle defaultValue="1" onValueChange={(value) => setChartType(value)}>
          <ToggleItem value="1" text="Diario" />
          <ToggleItem value="2" text="Mensual" />
          <ToggleItem value="3" text="Anual" />
        </Toggle>
      </Flex>
      {renderChart()}
    </Card>
  );
}

