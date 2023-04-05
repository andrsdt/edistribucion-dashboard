type DailyMeasurementI = {
  date: string;
  measurements: {
    hour: number;
    value: number;
  }[];
};
// Returns cumulative data by summing the values of all previous data points.
// Example: [1, 2, 3] becomes [1, 3, 6].
export const getCumulativeData = (seriesData: any) => {
  if (!seriesData?.dailyMeasurements) {
    return [];
  }
  const dailyMeasurements = seriesData.dailyMeasurements as DailyMeasurementI[];
  const cumulativeData: any[] = [];
  let cumulativeValue = 0;

  dailyMeasurements.forEach((dailyMeasurement) => {
    const { date, measurements } = dailyMeasurement;

    measurements.forEach((measurement) => {
      cumulativeValue += measurement.value;
    });

    cumulativeData.push({
      date,
      value: cumulativeValue,
    });
  });

  return cumulativeData;
};
