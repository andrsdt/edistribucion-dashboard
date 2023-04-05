import { MeasureI } from "@/interfaces/measure";
import axios from "axios";
import { useEffect, useState } from "react";

export default function useLastMeasures() {
  const [measures, setMeasures] = useState<MeasureI[]>([]);

  useEffect(() => {
    const fetchLastConsumption = async () => {
      const response = await axios.get("/api/measures/last");
      const { data } = response;

      setMeasures(data);
    };

    fetchLastConsumption();
  }, []);

  return measures;
}
