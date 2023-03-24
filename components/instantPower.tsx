import { Card, CategoryBar, Flex, Metric, Text } from "@tremor/react";
import InformationModal from "./informationModal";

export default function InstantPower() {
  return (
    <Card className="h-full flex flex-col justify-between">
      <Flex>
        <Text>Potencia actual</Text>
        <InformationModal text="Esta es la potencia que estás consumiendo en este momento. Sobrepasarla puede hacer saltar los plomos." />
      </Flex>
      <Metric className="mb-3">3,5 kWh</Metric>
      <CategoryBar
        categoryPercentageValues={[40, 30, 20, 10]}
        colors={["emerald", "yellow", "orange", "rose"]}
        percentageValue={62}
      />
    </Card>
  );
}
