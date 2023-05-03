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

const colors: { [key: string]: Color } = {
	increase: "rose",
	moderateIncrease: "rose",
	unchanged: "orange",
	moderateDecrease: "emerald",
	decrease: "emerald",
};

const now = new Date();

export default function ConsumptionDifference() {
	const { data } = useConsumptionDifference();
	return (
		<Card className="h-full">
			<Flex className="mb-2">
				<Text>Consumo (este mes)</Text>
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
