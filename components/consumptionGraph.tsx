import useLastMeasures from "@/hooks/useLastMeasures";
import {
  CheckIcon,
  CircleStackIcon,
  ReceiptRefundIcon,
} from "@heroicons/react/24/outline";
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
          <ToggleItem value="1" text="Diario" icon={CheckIcon} />
          <ToggleItem value="2" text="Mensual" icon={CircleStackIcon} />
          <ToggleItem value="3" text="Anual" icon={ReceiptRefundIcon} />
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
