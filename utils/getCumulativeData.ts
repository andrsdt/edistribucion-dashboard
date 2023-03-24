import { MeasureI } from "@/interfaces/measure";

// Returns cumulative data by summing the values of all previous data points.
// Example: [1, 2, 3] becomes [1, 3, 6].
export const getCumulativeData = (seriesData: MeasureI[]) => {
  const cumulativeData: MeasureI[] = [];

  seriesData.forEach((entry: MeasureI, index: number) => {
    const accumulatedValue = seriesData
      .slice(0, index + 1)
      .reduce((acc, curr) => acc + curr.valueDouble, 0);
    cumulativeData.push({ ...entry, valueDouble: accumulatedValue });
  });

  return cumulativeData;
};
