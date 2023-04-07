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
        {/* <Link className="underline" href="#">
          Historial
        </Link> */}
      </Flex>
      <Text>
        Fuente:{" "}
        <a
          className="font-semibold text-blue-700 underline"
          href="https://www.esios.ree.es/es/pvpc"
        >
          REE
        </a>{" "}
        &bull; {formatDate(new Date())}
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
