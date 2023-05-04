import useMonthMeasures from "@/hooks/useMonthMeasures";
import { getCumulativeData } from "@/utils/getCumulativeData";
import { AreaChart, Card, Flex, Title } from "@tremor/react";
import { useState } from "react";
import { MonthlyPreviousButtons } from "./consumptionGraph";

const today = new Date();

export default function AccumulatedConsumption() {
	const [month, setMonth] = useState(today);
	const { data } = useMonthMeasures(month);
	const { cumulativeData, expectedMonthlyConsumption } =
		getCumulativeData(data);

	return (
		<Card>
			<Flex>
				<Title>Tu consumo acumulado</Title>
				<MonthlyPreviousButtons month={month} setMonth={setMonth} />
			</Flex>
			<AreaChart
				className="pt-4"
				data={cumulativeData}
				index="date"
				categories={["value"]}
				valueFormatter={(value) => `${value.toFixed()} kWh`}
				colors={["blue"]}
				autoMinValue={true}
				showXAxis={true}
				showLegend={false}
				curveType="natural"
				maxValue={expectedMonthlyConsumption}
				yAxisWidth={60}
			/>
		</Card>
	);
}
