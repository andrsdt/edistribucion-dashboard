import usePvpcPrices from "@/hooks/usePvpcPrices";
import { formatDate } from "@/utils/formatDate";
import { formatHour } from "@/utils/formatHour";
import formatPrice from "@/utils/formatPrice";
import generateTracker from "@/utils/generateTracker";
import { Card, Flex, Text, Title, Tracker } from "@tremor/react";
import Link from "next/link";

export default function PvpcPriceTracker() {
	const { prices, maxPrice, minPrice } = usePvpcPrices();

	return (
		<Card className="mx-auto">
			<Flex justifyContent="between">
				<Title>PVPC - Precio de hoy</Title>
			</Flex>
			<Text>
				Fuente: <Link href="https://www.esios.ree.es/es/pvpc">REE</Link> &bull;{" "}
				{formatDate(new Date())}
			</Text>
			<Flex flexDirection="col" alignItems="end" className="mt-4">
				<Text>
					Mínimo: {formatPrice(minPrice?.price)} ({formatHour(minPrice?.hour)})
				</Text>
				<Text>
					Máximo: {formatPrice(maxPrice?.price)} ({formatHour(maxPrice?.hour)})
				</Text>
			</Flex>
			<Tracker data={generateTracker(prices)} className="mt-2" />
		</Card>
	);
}
