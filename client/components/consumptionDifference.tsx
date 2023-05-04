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

const colors: { [key: string]: Color } = {
	increase: "rose",
	moderateIncrease: "rose",
	unchanged: "orange",
	moderateDecrease: "emerald",
	decrease: "emerald",
};

export default function ConsumptionDifference() {
	const { data } = useConsumptionDifference();
	return (
		<Card className="h-full">
			<Flex className="mb-2">
				<Text>Tu Consumo (este mes)</Text>
				<InformationModal text="Los datos pueden no corresponderse con la realidad, ya que la comparación se hace para el último día del que haya datos disponibles al completo (24-48 horas en el pasado)" />
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
				<Text className="truncate"> al mismo periodo del último mes </Text>
			</Flex>
		</Card>
	);
}
