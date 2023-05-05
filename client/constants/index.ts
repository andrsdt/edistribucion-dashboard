export const MONTHLY_CONSUMPTION_LIMIT_IN_KWH = Number.parseInt(
	process.env.NEXT_PUBLIC_MONTHLY_CONSUMPTION_LIMIT_IN_KWH || "300"
);

export const BACKEND_URL =
	process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:5000";
