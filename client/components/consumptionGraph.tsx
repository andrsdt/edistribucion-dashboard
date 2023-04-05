import useLastMeasures from "@/hooks/useLastMeasures";
import { CalendarDaysIcon, CalendarIcon } from "@heroicons/react/24/outline";
import {
  Card,
  Flex,
  LineChart,
  Title,
  Toggle,
  ToggleItem,
} from "@tremor/react";

export default function ConsumptionGraph() {
  const measures = useLastMeasures();

  return (
    <Card>
      <Flex>
        <Title>Tu consumo</Title>
        <Toggle defaultValue="1" onValueChange={(value) => console.log(value)}>
          <ToggleItem value="1" text="Hoy" />
          <ToggleItem value="2" text="Abril" />
          <ToggleItem value="3" text="2023" />
        </Toggle>
      </Flex>
      <LineChart
        className="mt-3"
        data={measures}
        index="hourCCH"
        categories={["valueDouble"]}
        colors={["blue"]}
        yAxisWidth={30}
      />
    </Card>
  );
}
