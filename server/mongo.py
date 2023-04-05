import json
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

MONGO_USER = os.environ.get("MONGODB_USERNAME", "")
MONGO_PASSWORD = os.environ.get("MONGODB_PASSWORD", "")
MONGO_CLUSTER_URL = os.environ.get("MONGODB_CLUSTER_URL", "")
MONGO_AUTH = "DEFAULT"

MONGODB_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?authMechanism={MONGO_AUTH}"

client = MongoClient(MONGODB_URI)
db = client["mydatabase"]
electricity_collection = db["electricity"]

# Delete the collection to start from scratch
# electricity_collection.drop()

# create index to avoid duplicates by date
electricity_collection.create_index("date", unique=True)


def get_electricity_data(date):
    electricity_data = electricity_collection.find_one({"date": date})

    if electricity_data:
        print(f"Found cached electricity data for date {date}")
    else:
        print(f"Fetching electricity data for date {date} from remote API")
        # We will get the data from an external API (here we use a local file for testing so we don't saturate the API)
        # We would use the functions provided in edistribucion.py
        electricity_data = json.load(open("yesterday-from-api.json"))
        date = electricity_data[0]["date"]
        electricity_collection.insert_one(
            {"date": datetime.strptime(date, "%d/%m/%Y"), "data": electricity_data}
        )
        print(f"Cached electricity data for date {date}")

    return electricity_data


def get_electricity_data_interval(start_date, end_date):
    # convert dates to datetime
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")
    count_electricity_data = electricity_collection.count_documents(
        {"date": {"$gte": start_date, "$lte": end_date}}
    )

    days_in_interval = (end_date - start_date).days + 1
    if count_electricity_data >= days_in_interval:
        print(f"Found cached electricity data for date {start_date} - {end_date}")
        electricity_data = electricity_collection.find(
            {"date": {"$gte": start_date, "$lte": end_date}}
        )

    else:
        print(
            f"Fetching electricity data for date {start_date} - {end_date} from remote API"
        )
        # We will get the data from an external API (here we use a local file for testing so we don't saturate the API)
        # We would use the functions provided in edistribucion.py
        electricity_data = json.load(open("lastMonth-from-api.json"))

        # Agrupar los objetos por día
        for day_data in electricity_data:
            day_dict = {}
            for obj in day_data:
                date = datetime.strptime(obj["date"], "%d/%m/%Y")
                if date not in day_dict:
                    day_dict[date] = []
                day_dict[date].append(obj)

            # Insert grouped data in MongoDB
            # Add date to database if not present, otherwise update
            electricity_collection.update_many(
                update={"$set": {"date": date, "data": day_dict[date]}},
                filter={"date": date},
                upsert=True,
            )

        print(f"Cached electricity data for date {start_date} - {end_date}")

    return electricity_data


if __name__ == "__main__":
    # These functions will try to fetch data from MongoDB.
    # If not present, it will fetch from the external API and update the MongoDB cache
    get_electricity_data("22/02/2023")
    get_electricity_data_interval("03/02/2023", "06/02/2023")
