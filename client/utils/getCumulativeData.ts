import dayjs from "@/lib/dayjs";

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
		return {
			cumulativeData: [],
			expectedMonthlyConsumption: 0,
		};
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
			date: Number.parseInt(dayjs(date).format("D")),
			value: cumulativeValue,
		});
	});

	const month =
		dailyMeasurements.length > 0 ? dayjs(dailyMeasurements[0].date) : dayjs();

	// Fill the rest of objects with null values until the last day of the month
	const numberOfDaysInMonth = month.endOf("month").date();
	const lastEntry = cumulativeData[cumulativeData.length - 1];
	const daysRemaining = numberOfDaysInMonth - cumulativeData.length;
	const averageDailyConsumption = lastEntry.value / cumulativeData.length;

	for (let i = 0; i < daysRemaining; i++) {
		cumulativeData.push({
			date: Number.parseInt(lastEntry.date) + i + 1,
			value: null,
		});
	}

	return {
		cumulativeData,
		expectedMonthlyConsumption: numberOfDaysInMonth * averageDailyConsumption,
	};
};
