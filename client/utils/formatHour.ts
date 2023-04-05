export const formatHour = (hour = "00-00") => {
  // 01-02 => 01:00 - 02:00
  const [start, end] = hour.split("-");
  return `${start}:00 - ${end}:00`;
};
