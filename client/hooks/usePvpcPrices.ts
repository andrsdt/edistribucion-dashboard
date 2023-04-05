import { PVPC } from "@/interfaces/pvpc";
import axios from "axios";
import { useState, useEffect } from "react";

export default function usePvpcPrices() {
  const [prices, setPrices] = useState<PVPC[]>([]);
  const [maxPrice, setMaxPrice] = useState<PVPC>();
  const [minPrice, setMinPrice] = useState<PVPC>();

  useEffect(() => {
    const fetchPrices = async () => {
      const response = await axios.get("/api/pvpc/today");
      const { data } = response;

      setPrices(data);
      setMaxPrice(
        Object.values(data).reduce((prev: any, current: any) =>
          prev.price > current.price ? prev : current
        ) as PVPC
      );
      setMinPrice(
        Object.values(data).reduce((prev: any, current: any) =>
          prev.price < current.price ? prev : current
        ) as PVPC
      );
    };

    fetchPrices();
  }, []);

  return { prices, maxPrice, minPrice };
}
