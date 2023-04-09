import itertools
import logging
from datetime import timedelta, datetime
import calendar

from Edistribucion import Edistribucion
from mongo import electricity_collection, accumulated_monthly
from utils import (
    data_is_complete,
    month_is_complete,
    format_date_dashes,
    format_date_slashes,
    group_datetimes_by_consecutive_days,
)

# Delete the collection to start from scratch
# electricity_collection.drop()

# create index to avoid duplicates by date
electricity_collection.create_index("date", unique=True)
accumulated_monthly.create_index("date", unique=True)
edis = Edistribucion(debug_level=logging.DEBUG)


def get_electricity_data(date: str):
    # convert date to datetime
    date = format_date_dashes(date)

    # Find one where complete is True
    electricity_data = electricity_collection.find_one({"date": date, "complete": True})

    if electricity_data:
        print(f"Found cached electricity data for date {date}")
    else:
        print(f"Fetching electricity data for date {date} from remote API")
        # We will get the data from an external API (here we use a local file for testing so we don't saturate the API)
        # We would use the functions provided in edistribucion.py
        cups = edis.get_active_cups()
        electricity_data = edis.get_meas_interval(cups["Id"], date, date)
        date = electricity_data[0]["date"]
        electricity_collection.insert_one(
            {
                "date": format_date_dashes(date),
                "complete": data_is_complete(electricity_data),
                "data": electricity_data,
            }
        )
        print(f"Cached electricity data for date {date}")
        electricity_data = electricity_collection.find_one({"date": date})

    return electricity_data


def get_electricity_data_interval(start_date_str: str, end_date_str: str):
    # convert date to datetime
    start_date = format_date_dashes(start_date_str)
    #end_date will be the min between the end_date_str and today
    end_date = min(format_date_dashes(end_date_str), datetime.today())
    end_date_str = end_date.strftime("%Y-%m-%d")

    count_electricity_data = electricity_collection.count_documents(
        {"date": {"$gte": start_date, "$lte": end_date}, "complete": True}
    )

    days_in_interval = (end_date - start_date).days + 1
    if count_electricity_data >= days_in_interval:
        print(
            f"Found cached electricity data for date {start_date_str} - {end_date_str}"
        )

    else:
        # Get dates already in database where complete is True
        dates_in_db = electricity_collection.find(
            {"date": {"$gte": start_date, "$lte": end_date}, "complete": True},
            {"date": 1, "_id": 0}
        )

        dates_in_db = {obj["date"] for obj in dates_in_db}
        
        # Get a list of all the datetimes for every day from start_date to end_date and remove the ones already in the database
        dates_to_fetch = set([start_date + timedelta(days=x) for x in range(0, days_in_interval)])
        dates_to_fetch = dates_to_fetch - dates_in_db

        # Fetch data for each day
        date_ranges_to_fetch = group_datetimes_by_consecutive_days(list(dates_to_fetch))
        # NOTE: NOW I HAVE A LIST OF DATE RANGES TO FETCH AND FOR EACH ONE OF THEM, I HAVE TO
        # SELECT THE FIRST AND LAST DAY AND FETCH THE DATA FOR THAT RANGE
        cups = edis.get_active_cups()
        for date_range in date_ranges_to_fetch:
            first_date_str = date_range[0].strftime("%Y-%m-%d")
            end_date_str = date_range[1].strftime("%Y-%m-%d")
            # Fetch data for the range
            print(f"Fetching electricity data for date {start_date_str} - {end_date_str} from remote API")
            electricity_data = edis.get_meas_interval(
                cups["Id"], first_date_str, end_date_str
            )

            # Group objects by day
            for day_data in electricity_data:
                day_dict = {}
                for obj in day_data:
                    date = format_date_slashes(obj["date"])
                    if date not in day_dict:
                        day_dict[date] = []
                    day_dict[date].append(obj)

                # Insert grouped data in MongoDB
                # Add date to database if not present, otherwise update
                data = day_dict[date]  # Data for the day
                electricity_collection.update_many(
                    update={
                        "$set": {
                            "date": date,
                            "complete": data_is_complete(data),
                            "data": data,
                        }
                    },
                    filter={"date": date},
                    upsert=True,
                )

            print(f"Cached electricity data for date {start_date_str} - {end_date_str}")

    return electricity_collection.find({"date": {"$gte": start_date, "$lte": end_date}})


def get_accumulated_electricity_data(date_str: str):
   # convert date to datetime
    date = format_date_dashes(date_str)

    # Find one for the date. It does not matter if it is not complete
    # A not complete montly accumulated value can be used for the "Consumo" board
    accumulated_monthly_data = accumulated_monthly.find_one({"date": date})

    if accumulated_monthly_data:
        print(f"Found cached accumulated electricity data for date {date}")
        print(accumulated_monthly_data)
    else:
        print(f"Fetching electricity data for all the month in {date}")
        # First we get the number of days the month has
        num_days = calendar.monthrange(date.year, date.month)[1]
        
        # Then we ask for the data in all days of the month with get_electricity_data_interval(start_date_str: str, end_date_str: str)
        end_date_str = date.replace(day=num_days).strftime("%Y-%m-%d")
        electricity_data = get_electricity_data_interval(date_str, end_date_str)
    
        # With this data we calculate the accumulated value for the whole month
        # Crea la lista de etapas de agregación
        pipeline = [
            {"$match": {"date": {"$gte": date, "$lte": date.replace(day=num_days)}}},
            {"$unwind": "$data"},
            {"$group": {"_id": None, "accumulatedValue": {"$sum": "$data.valueDouble"}}}
        ]

        # Ejecuta la agregación y devuelve el resultado
        result = list(electricity_collection.aggregate(pipeline))

        # This is another way for getting the accumulated value
        # This way uses the electricity_data received by the other method
        # The other way uses the data directly from MongoDB with a pipeline of operations
    #     accumulated_value = 0
    #     for data in electricity_data:
    #         # Obtain the objects representing the 24 hours in the day
    #         horas = data["data"]
    #         for hora in horas:
    #             # Add the value of the attribute valueDouble
    #             accumulated_value += hora["valueDouble"]

        # Finally we insert the new document in the collection
        accumulated_monthly.insert_one(
            {
                "date": date,
                "complete": month_is_complete(electricity_data),
                "accumulatedValue": result[0]['accumulatedValue'],
            }
        )
        print(f"Cached accumulated electricity data for date {date}")
        accumulated_monthly_data = accumulated_monthly.find_one({"date": date})

    return accumulated_monthly_data


if __name__ == "__main__":
    # These functions will try to fetch data from MongoDB.
    # If not present, it will fetch from the external API and update the MongoDB cache
    # get_electricity_data("22/02/2023")
    # get_electricity_data_interval("03/02/2023", "06/02/2023")
    # get_accumulated_electricity_data("2023-04-01")
    pass
