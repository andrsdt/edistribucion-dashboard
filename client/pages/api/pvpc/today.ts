import { PVPC } from "@/interfaces/pvpc";
import axios from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default async function pvpcHandler(
	req: NextApiRequest,
	res: NextApiResponse<PVPC>
) {
	const { method } = req;
	if (method === "GET") {
		const response = await axios.get(
			"https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
		);
		const { data } = response;
		res.status(200).json(data);
	} else {
		res.setHeader("Allow", ["GET", "PUT"]);
		res.status(405).end(`Method ${method} Not Allowed`);
	}
}
