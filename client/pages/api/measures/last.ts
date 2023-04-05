import { MeasureI } from "@/interfaces/measure";
import axios from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default async function measureHandler(
  req: NextApiRequest,
  res: NextApiResponse<MeasureI[]>
) {
  const { method } = req;
  if (method === "GET") {
    const response = await axios.get(
      // TODO: fetch from our cache backend in production
      "http://localhost:3000/data/yesterday.json"
    );
    const { data } = response;
    res.status(200).json(data);
  } else {
    res.setHeader("Allow", ["GET", "PUT"]);
    res.status(405).end(`Method ${method} Not Allowed`);
  }
}
