import { MONTHLY_CONSUMPTION_LIMIT_IN_KWH } from "@/constants";
import { BarChart } from "@tremor/react";

interface BarConsumptionChartProps {
	data: any;
}

export default function BarConsumptionChart({
	data,
}: BarConsumptionChartProps) {
	// Split the data into two series, one for the under consumption
	// limit (blue) and one for the over consumption limit (red)
	const limit = MONTHLY_CONSUMPTION_LIMIT_IN_KWH;
	const splitData =
		data?.map(({ date, accumulatedValue }: any) => ({
			date,
			consumo: Math.min(accumulatedValue, limit),
			exceso: Math.max(0, accumulatedValue - limit),
		})) ?? [];

	return (
		<BarChart
			className="mt-3"
			data={splitData}
			index="date"
			colors={["blue", "red"]}
			valueFormatter={(value) => `${value.toFixed()} kWh`}
			showLegend={false}
			yAxisWidth={30}
			stack={true}
			categories={["consumo", "exceso"]}
		/>
	);
}
