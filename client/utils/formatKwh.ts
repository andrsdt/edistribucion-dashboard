export const formatKwh = (kwh = 0.0) => {
	return `${Number.parseFloat(kwh.toFixed(2)).toLocaleString("es-ES")} kWh`;
};
