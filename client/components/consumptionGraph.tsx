import useAccumulatedAnnual from "@/hooks/useAccumulatedAnnual";
import useAccumulatedMonthly from "@/hooks/useAccumulatedMonthly";
import useDailyMeasures from "@/hooks/useDailyMeasures";
import { Card, Flex, Title, Toggle, ToggleItem } from "@tremor/react";

import { useState } from "react";
import BarConsumptionChart from "./barConsumptionChart";
import LineConsumptionChart from "./lineConsumptionChart";
import dayjs from "@/lib/dayjs";
import InformationModal from "./informationModal";

const today = new Date();

const CHART_TYPES = {
	DAILY: "daily",
	MONTHLY: "monthly",
	YEARLY: "yearly",
};
const defaultChart = CHART_TYPES.DAILY;

export default function ConsumptionGraph() {
	const [dailyChartDay, setDailyChartDay] = useState(today);
	const [monthlyChartMonth, setMonthlyChartMonth] = useState(today);
	const [annualChartYear, setAnnualChartYear] = useState(today);

	const { dataDaily } = useDailyMeasures(dailyChartDay);
	const { dataYearly } = useAccumulatedAnnual(annualChartYear);
	const { dataMonthly } = useAccumulatedMonthly(monthlyChartMonth);

	const [chartType, setChartType] = useState(defaultChart);

	const navigators = {
		[CHART_TYPES.DAILY]: (
			<DailyNextPreviousButtons day={dailyChartDay} setDay={setDailyChartDay} />
		),
		[CHART_TYPES.MONTHLY]: (
			<MonthlyPreviousButtons
				month={monthlyChartMonth}
				setMonth={setMonthlyChartMonth}
			/>
		),
		[CHART_TYPES.YEARLY]: (
			<YearlyPreviousButtons
				year={annualChartYear}
				setYear={setAnnualChartYear}
			/>
		),
	};
	const charts = {
		[CHART_TYPES.DAILY]: <LineConsumptionChart data={dataDaily} />,
		[CHART_TYPES.MONTHLY]: <BarConsumptionChart data={dataMonthly} />,
		[CHART_TYPES.YEARLY]: <BarConsumptionChart data={dataYearly} />,
	};

	return (
		<Card>
			<Flex className="flex-col-reverse justify-center space-y-4 space-y-reverse md:space-y-0 md:flex-row md:justify-between">
				{navigators[chartType]}
				<Toggle
					defaultValue={defaultChart}
					onValueChange={(value) => setChartType(value)}
				>
					<ToggleItem value={CHART_TYPES.DAILY} text="Día" />
					<ToggleItem value={CHART_TYPES.MONTHLY} text="Mes" />
					<ToggleItem value={CHART_TYPES.YEARLY} text="Año" />
				</Toggle>
			</Flex>
			{charts[chartType]}
		</Card>
	);
}

const GenericNextPreviousButtons = ({
	date,
	setDate,
	onPrevious,
	onNext,
	text,
}: any) => {
	// Earliest available date is 2022-01-31.
	// There is no date before because I switched electricity companies
	const hasPrevious =
		onPrevious(date.getTime()) >= new Date(2022, 0, 31).getTime();
	const hasNext = onNext(date.getTime()) <= today.getTime();
	return (
		<Flex className="w-min justify-start items-center space-x-2">
			{hasPrevious ? (
				<button id="chevron-arrow-left" onClick={() => setDate(onPrevious)} />
			) : (
				<InformationModal
					origin="top-left"
					text="No hay datos disponibles anteriores a febrero de 2022"
				/>
			)}
			<Title className="whitespace-nowrap">{text}</Title>
			{hasNext && (
				<button id="chevron-arrow-right" onClick={() => setDate(onNext)} />
			)}
		</Flex>
	);
};

const DailyNextPreviousButtons = ({ day, setDay }: any) => {
	const text = day.toLocaleDateString("es-ES", {
		weekday: "long",
		day: "numeric",
		month: "long",
	});
	return (
		<GenericNextPreviousButtons
			date={day}
			setDate={setDay}
			onPrevious={() => dayjs(day).subtract(1, "day").startOf("day").toDate()}
			onNext={() => dayjs(day).add(1, "day").startOf("day").toDate()}
			text={text}
		/>
	);
};

// Also used in cumulative monthly data chart
export const MonthlyPreviousButtons = ({ month, setMonth }: any) => {
	const text = month.toLocaleDateString("es-ES", {
		month: "long",
		year: "numeric",
	});
	return (
		<GenericNextPreviousButtons
			date={month}
			setDate={setMonth}
			onPrevious={() =>
				dayjs(month).subtract(1, "month").startOf("month").toDate()
			}
			onNext={() => dayjs(month).add(1, "month").startOf("month").toDate()}
			text={text}
		/>
	);
};

const YearlyPreviousButtons = ({ year, setYear }: any) => {
	const text = year.toLocaleDateString("es-ES", { year: "numeric" });
	return (
		<GenericNextPreviousButtons
			date={year}
			setDate={setYear}
			onPrevious={() => dayjs(year).subtract(1, "year").endOf("year").toDate()}
			onNext={() => dayjs(year).add(1, "year").startOf("year").toDate()}
			text={text}
		/>
	);
};
