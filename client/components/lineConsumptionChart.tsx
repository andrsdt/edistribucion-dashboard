import { LineChart } from "@tremor/react";

interface LineConsumptionChartProps {
	data: any;
}

export default function LineConsumptionChart({
	data,
}: LineConsumptionChartProps) {
	const existsData = data?.length > 0 && data[0].value !== null;

	if (!existsData)
		return (
			<div className="flex w-full rounded-md border border-dashed border-gray-300 my-1.5 justify-center items-center text-center h-80 text-xl font-thin italic text-gray-400">
				Aún no tenemos datos para este día.
				<br />
				Vuelve a intentarlo más tarde.
			</div>
		);

	return (
		<LineChart
			className="mt-3"
			data={data}
			index="hour"
			categories={["value"]}
			valueFormatter={(value) => `${value.toPrecision(2)} kWh`}
			colors={["blue"]}
			showLegend={false}
			connectNulls={true}
			curveType={"natural"}
			yAxisWidth={30}
		/>
	);
}
