import { BarChart } from "@tremor/react";
import dayjs from "dayjs";

interface BarConsumptionChartProps {
	data: any;
}

export default function BarConsumptionChart({
	data,
}: BarConsumptionChartProps) {
	return (
		<BarChart
			className="mt-3"
			data={data}
			index="date"
			colors={["blue"]}
			valueFormatter={(value) => `${value.toFixed()} kWh`}
			showLegend={false}
			yAxisWidth={30}
			categories={["accumulatedValue"]}
		/>
	);
}
