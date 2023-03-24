// {
//   "00-01": {
//   "date": "20-03-2023",
//   "hour": "00-01",
//   "is-cheap": false,
//   "is-under-avg": true,
//   "market": "PVPC",
//   "price": 172.56,
//   "units": "€/Mwh"
//   },
//   "01-02": {
//    ...
//   },
// }

export type PVPC = {
  date: string;
  hour: string;
  isCheap: boolean;
  isUnderAvg: boolean;
  market: string;
  price: number;
  units: string;
};
