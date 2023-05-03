import { LineChart } from "@tremor/react";

interface LineConsumptionChartProps {
	data: any;
}

export default function LineConsumptionChart({
	data,
}: LineConsumptionChartProps) {
	return (
		<LineChart
			className="mt-3"
			data={data}
			index="hour"
			categories={["value"]}
			valueFormatter={(value) => `${value.toPrecision(2)} kWh`}
			colors={["blue"]}
			showLegend={false}
			yAxisWidth={30}
		/>
	);
}
