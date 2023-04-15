import useConsumptionDifference from "@/hooks/useConsumptionDifference";
import { BanknotesIcon, LightBulbIcon } from "@heroicons/react/24/outline";
import {
  BadgeDelta,
  Card,
  Color,
  DeltaType,
  Flex,
  Metric,
  Text,
  Toggle,
  ToggleItem,
} from "@tremor/react";
import { useState } from "react";

const colors: { [key: string]: Color } = {
  increase: "rose",
  moderateIncrease: "rose",
  unchanged: "orange",
  moderateDecrease: "emerald",
  decrease: "emerald",
};

const categories: {
  title: string;
  metric: string;
  metricPrev: string;
  delta: string;
  deltaType: DeltaType;
}[] = [
  {
    title: "Sales",
    metric: "$ 12,699",
    metricPrev: "$ 9,456",
    delta: "34.3%",
    deltaType: "moderateIncrease",
  },
  {
    title: "Profit",
    metric: "$ 40,598",
    metricPrev: "$ 45,564",
    delta: "10.9%",
    deltaType: "moderateDecrease",
  },
  {
    title: "Customers",
    metric: "1,072",
    metricPrev: "856",
    delta: "25.3%",
    deltaType: "moderateIncrease",
  },
];

export default function ConsumptionDifference() {
  const { loading, error, data } = useConsumptionDifference();
  const [mode, setMode] = useState<"kwh" | "eur">("kwh");

  const kwhItem = {
    title: "Consumo",
    metric: "314,16 kWh",
    metricPrev: "284,31 kWh",
    delta: "10.5%",
    deltaType: "increase",
  };

  const eurItem = {
    title: "Coste",
    metric: "72,90 €",
    metricPrev: "60,72 €",
    delta: "16.7%",
    deltaType: "increase",
  };

  const item = mode === "kwh" ? kwhItem : eurItem;

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <Card key={item.title} className="h-full">
      <Flex justifyContent="between">
        <Text className="mb-2">Consumo</Text>
        <Toggle
          defaultValue={mode}
          onValueChange={(value) => setMode(value as 'kwh' | 'eur')}
          className="scale-90 origin-top-right"
        >
          <ToggleItem value="kwh" icon={LightBulbIcon} />
          {/* <ToggleItem value="eur" icon={BanknotesIcon} /> */}
        </Toggle>
      </Flex>
      <Flex
        justifyContent="start"
        alignItems="baseline"
        className="truncate space-x-3"
      >
        <Metric className="mb-2.5">
          {data.accumulativeData[0]['accumulatedValue']}
        </Metric>
        <Text className="truncate">
          antes {data.accumulativeData[1]['accumulatedValue']}
        </Text>
      </Flex>
      <Flex justifyContent="start" className="space-x-2 mt-4">
        <BadgeDelta
          deltaType={data.deltaType as DeltaType}
          isIncreasePositive={false}
        />
        <Flex justifyContent="start" className="space-x-1 truncate">
          <Text color={colors[data.deltaType]}>{data.delta}</Text>
          <Text className="truncate"> al mismo periodo del último mes </Text>
        </Flex>
      </Flex>
    </Card>
  );
}
