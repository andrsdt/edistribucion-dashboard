import useMonthMeasures from "@/hooks/useMonthMeasures";
import { getCumulativeData } from "@/utils/getCumulativeData";
import { AreaChart, Card, Title } from "@tremor/react";

const today = new Date();

export default function AccumulatedConsumption() {
	const { data } = useMonthMeasures(today);
	const accumulatedMeasures = getCumulativeData(data);
	const thisMonth = new Date()
		.toLocaleDateString("es-ES", {
			month: "long",
			year: "numeric",
		})
		.replace(" de ", " ");

	return (
		<Card>
			<Title>Tu consumo acumulado ({thisMonth})</Title>
			<AreaChart
				className="pt-4"
				data={accumulatedMeasures}
				index="date"
				categories={["value"]}
				valueFormatter={(value) => `${value.toFixed()} kWh`}
				colors={["blue"]}
				autoMinValue={true}
				showXAxis={false}
				showLegend={false}
				yAxisWidth={60}
			/>
		</Card>
	);
}
