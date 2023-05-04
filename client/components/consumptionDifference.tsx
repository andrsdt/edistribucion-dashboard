import useConsumptionDifference from "@/hooks/useConsumptionDifference";
import { formatKwh } from "@/utils/formatKwh";
import {
	BadgeDelta,
	Card,
	Color,
	DeltaType,
	Flex,
	Metric,
	Text,
} from "@tremor/react";
import InformationModal from "./informationModal";
import { useState } from "react";
import { MonthlyPreviousButtons } from "./consumptionGraph";

const colors: { [key: string]: Color } = {
	increase: "rose",
	moderateIncrease: "rose",
	unchanged: "orange",
	moderateDecrease: "emerald",
	decrease: "emerald",
};

const today = new Date();
export default function ConsumptionDifference() {
	const [month, setMonth] = useState(today);
	const { data } = useConsumptionDifference(month);

	return (
		<Card className="h-full">
			<Flex className="mb-2">
				<Text className="whitespace-nowrap">Tu Consumo</Text>
				<Flex className="justify-end space-x-2">
					<MonthlyPreviousButtons month={month} setMonth={setMonth} />
					<InformationModal
						origin="top-right"
						text="Los datos pueden no corresponderse con la realidad ya que, para que la comparación sea justa, se hace con el último día del que haya datos disponibles al completo (24-48 horas en el pasado)"
					/>
				</Flex>
			</Flex>
			<Flex className="justify-start items-baseline truncate space-x-3">
				<Metric className="mb-2.5">
					{formatKwh(data.accumulativeData[0]["accumulatedValue"])}
				</Metric>
				<Text className="truncate">
					antes {formatKwh(data.accumulativeData[1]["accumulatedValue"])}
				</Text>
			</Flex>
			<Flex className="justify-start space-x-1 mt-4">
				<BadgeDelta
					deltaType={data.deltaType as DeltaType}
					isIncreasePositive={false}
				/>
				<Text color={colors[data.deltaType]}>{data.delta}</Text>
				<Text className="truncate"> al mismo periodo del mes anterior </Text>
			</Flex>
		</Card>
	);
}
