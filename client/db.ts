import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

const username = encodeURIComponent(process.env.MONGODB_USERNAME || "");
const password = encodeURIComponent(process.env.MONGODB_PASSWORD || "");
const clusterUrl = process.env.MONGODB_CLUSTER_URL || "";
const authMechanism = "DEFAULT";

// Replace the following with your MongoDB deployment's connection string.
const MONGODB_URI = `mongodb+srv://${username}:${password}@${clusterUrl}/?authMechanism=${authMechanism}`;

mongoose
  .connect(MONGODB_URI)
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((err) => {
    console.log(err);
  });
