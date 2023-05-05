import useMonthMeasures from "@/hooks/useMonthMeasures";
import { getCumulativeData } from "@/utils/getCumulativeData";
import { AreaChart, Card, Flex, Title } from "@tremor/react";
import { useState } from "react";
import { MonthlyPreviousButtons } from "./consumptionGraph";
import { MONTHLY_CONSUMPTION_LIMIT_IN_KWH } from "@/constants";

const today = new Date();

export default function AccumulatedConsumption() {
	const [month, setMonth] = useState(today);
	const { data } = useMonthMeasures(month);
	const { cumulativeData, expectedMonthlyConsumption } =
		getCumulativeData(data);

	// Split the data into two series, one for the under consumption
	// limit (blue) and one for the over consumption limit (red)
	const splitData = cumulativeData.map(({ date, value }) => ({
		date,
		consumo:
			cumulativeData.find(({ date }) => Math.max(0, date - 1))?.value <
			MONTHLY_CONSUMPTION_LIMIT_IN_KWH
				? value
				: null,
		exceso: value > MONTHLY_CONSUMPTION_LIMIT_IN_KWH ? value : null,
	}));

	return (
		<Card>
			<Flex>
				<Title>Tu consumo acumulado</Title>
				<MonthlyPreviousButtons month={month} setMonth={setMonth} />
			</Flex>
			<AreaChart
				className="pt-4"
				data={splitData}
				index="date"
				categories={["consumo", "exceso"]}
				valueFormatter={(value) => `${value.toFixed()} kWh`}
				colors={["blue", "red"]}
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
