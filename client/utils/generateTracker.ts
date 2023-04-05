import { Color } from "@tremor/react";
import { PVPC } from "@/interfaces/pvpc";
import { TrackerI } from "@/interfaces/tracker";
import { formatHour } from "./formatHour";
import formatPrice from "./formatPrice";

// Color will be red if price is higher than 150, yellow if between 100 and 150 and green if lower than 100
const getColor = (price: number): Color => {
  if (price > 150) {
    return "red";
  } else if (price > 100) {
    return "yellow";
  } else {
    return "green";
  }
};

export default function generateTracker(data: PVPC[]) {
  const tracker: TrackerI[] = [];

  Object.values(data).forEach((hourData) => {
    const { price, hour } = hourData;

    tracker.push({
      color: getColor(price),
      tooltip: `${formatHour(hour)} • ${formatPrice(price)}`,
    });
  });

  return tracker;
}
