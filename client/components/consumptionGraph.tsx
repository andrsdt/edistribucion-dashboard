import useLastMeasures from "@/hooks/useLastMeasures";
import {
  Card,
  Flex,
  LineChart,
  Title,
  Toggle,
  ToggleItem,
} from "@tremor/react";

export default function ConsumptionGraph() {
  const { loading, error, data } = useLastMeasures();

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <Card>
      <Flex>
        <Title>Tu consumo</Title>
        <Toggle defaultValue="1" onValueChange={(value) => console.log(value)}>
          <ToggleItem value="1" text="Diario" />
          <ToggleItem value="2" text="Mensual" />
          <ToggleItem value="3" text="Anual" />
        </Toggle>
      </Flex>
      <LineChart
        className="mt-3"
        data={data}
        index="hour"
        categories={["value"]}
        colors={["blue"]}
        yAxisWidth={30}
      />
    </Card>
  );
}
