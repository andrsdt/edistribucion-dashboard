import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";

// configure Day.js to use the UTC and timezone plugins
dayjs.extend(utc);
dayjs.extend(timezone);

// set the timezone to GMT+2
dayjs.tz.setDefault("Europe/Madrid");

export default dayjs;
