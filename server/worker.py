import itertools
import logging
from datetime import timedelta, datetime
import calendar

from Edistribucion import Edistribucion
from credentials import username, password
from mongo import electricity_collection, accumulated_monthly, accumulated_daily
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
accumulated_daily.create_index("date", unique=True)
edis = Edistribucion(debug_level=logging.DEBUG) if username and password else None


def get_electricity_data(date: str):
    # convert date to datetime
    date = format_date_dashes(date)

    # Find one where complete is True
    electricity_data = electricity_collection.find_one(
        {"date": date, "complete": True})

    if electricity_data:
        print(f"Found cached electricity data for date {date}")
    else:
        print(f"Fetching electricity data for date {date} from remote API")
        # We will get the data from an external API (here we use a local file for testing so we don't saturate the API)
        # We would use the functions provided in edistribucion.py
        if edis is not None:
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
    # end_date will be the min between the end_date_str and today
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
        dates_to_fetch = set([start_date + timedelta(days=x)
                             for x in range(0, days_in_interval)])
        dates_to_fetch = dates_to_fetch - dates_in_db

        # Fetch data for each day
        date_ranges_to_fetch = group_datetimes_by_consecutive_days(
            list(dates_to_fetch))
        # NOTE: NOW I HAVE A LIST OF DATE RANGES TO FETCH AND FOR EACH ONE OF THEM, I HAVE TO
        # SELECT THE FIRST AND LAST DAY AND FETCH THE DATA FOR THAT RANGE
        
        if edis is None:
            print("No credentials found, skipping fetching data from API")
            return electricity_collection.find({"date": {"$gte": start_date, "$lte": end_date}})
        cups = edis.get_active_cups()
        for date_range in date_ranges_to_fetch:
            first_date_str = date_range[0].strftime("%Y-%m-%d")
            end_date_str = date_range[1].strftime("%Y-%m-%d")

            # If it's trying to fetch data for today, don't fetch it because it's not gonna exist in the remote API
            if end_date_str == datetime.today().strftime("%Y-%m-%d"):
                break

            print(
                f"Fetching electricity data for date {start_date_str} - {end_date_str} from remote API")
            try:
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
                
                print(
                f"Cached electricity data for date {start_date_str} - {end_date_str}")
            except Exception:
                print(
                    f"ERROR FETCHING ELECTRICITY DATA for date {start_date_str} - {end_date_str} from remote API")

    return electricity_collection.find({"date": {"$gte": start_date, "$lte": end_date}})


def get_accumulated_electricity_data(date_str: str):
   # convert date to datetime
    date = format_date_dashes(date_str)

    # Check for the data in that date and if it is complete
    accumulated_monthly_data = accumulated_monthly.find_one({"date": date, "complete": True})

    if accumulated_monthly_data:
        print(f"Found cached accumulated electricity data for date {date}")
    else:
        print(f"Fetching electricity data for all the month in {date}")
        # First we get the number of days the month has
        num_days = calendar.monthrange(date.year, date.month)[1]
        
        # Then we ask for the data in all days of the month with get_electricity_data_interval(start_date_str: str, end_date_str: str)
        end_date_str = date.replace(day=num_days).strftime("%Y-%m-%d")
        electricity_data = get_electricity_data_interval(date_str, end_date_str)
    
        # With this data we calculate the accumulated value for the whole month
        pipeline = [
            {"$match": {"date": {"$gte": date, "$lte": date.replace(day=num_days)}}},
            {"$unwind": "$data"},
            {"$group": {"_id": None, "accumulatedValue": {"$sum": "$data.valueDouble"}}}
        ]

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
        accumulated_monthly.update_one(
            {"date": date},
            {"$set": {
                "complete": month_is_complete(electricity_data),
                "accumulatedValue": result[0]['accumulatedValue']
            }},
            upsert=True
        )
        print(f"Cached accumulated electricity data for date {date}")
        accumulated_monthly_data = accumulated_monthly.find_one({"date": date})

    return accumulated_monthly_data


def get_year_accumulated_electricity_data(year: int):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    electricity_data = list(accumulated_monthly.find(
        {"date": {"$gte": start_date, "$lte": end_date}, "complete": True}))

    # If the year asked is the current year this will always be False since the information wont't be complete
    if len(electricity_data) == 12:
        print(f"Found cached electricity data for year {year}")
    else:
        # Makes sure all the data available in the year is up in the cache
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        get_electricity_data_interval(start_date_str, end_date_str)


        # Gets the accumulated value of all the months available in the year
        # Also get if the month is complete or not
        # start_date = datetime(year, 1, 1)
        # end_date = start_date.replace(month=12,day=31)
        pipeline = [
            {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
            {"$project": {"year_month": {"$dateToString": {"format": "%Y-%m",
                                                           "date": "$date"}}, "complete": "$complete", "data": 1}},
            {"$unwind": "$data"},
            {"$group": {"_id": {"year_month": "$year_month", "complete": "$complete"},
                        "days": {"$sum": 1},
                        "total_value": {"$sum": "$data.valueDouble"}}},
            {"$group": {"_id": "$_id.year_month",
                        "complete": {"$sum": {"$cond": [{"$eq": ["$_id.complete", True]}, "$days", 0]}},
                        "total": {"$sum": "$days"},
                        "accumulatedValue": {"$sum": "$total_value"}}},
            {"$project": {"_id": 1, 
              "complete": {"$eq": ["$total", "$complete"]}, 
              "accumulatedValue": 1, 
              "total": {"$divide": ["$total", 24]}}},
            {"$sort": {"_id": 1}}
        ]
        result = list(electricity_collection.aggregate(pipeline))

        # Updates the documents in the collection
        # Insert the new data if it wasn't there
        for doc in result:
            date = datetime.strptime(doc['_id'], '%Y-%m')
            filter_query = {"date": date}
            if(doc["complete"] and round(doc["total"]) == calendar.monthrange(date.year, date.month)[1]):
                update_query = {"$set": {
                    "date": date, "complete": True, "accumulatedValue": doc["accumulatedValue"]}}
            else:
                update_query = {"$set": {
                    "date": date, "complete": False, "accumulatedValue": doc["accumulatedValue"]}}
            accumulated_monthly.update_one(
                    filter_query, update_query, upsert=True)


        print(f"Cached accumulated electricity data for year {year}")
        electricity_data = list(accumulated_monthly.find({"date": {"$gte": start_date, "$lt": end_date}}))

    return electricity_data


def get_day_accumulated_electricity_data(date_str: str):
   # convert date to datetime
    date = format_date_dashes(date_str)

    # Check for the data in that day and if it is complete
    accumulated_daily_data = accumulated_daily.find_one({"date": date, "complete": True})

    if accumulated_daily_data:
        print(f"Found cached accumulated daily electricity data for date {date}")
    else:
        print(f"Fetching day electricity data for {date}")
        
        try:
            electricity_data = list(get_electricity_data_interval(date_str,date_str))
            # With this data we calculate the accumulated value for the day
            pipeline = [
                {"$match": {"date": date}},
                {"$unwind": "$data"},
                {"$group": {"_id": None, "accumulatedValue": {"$sum": "$data.valueDouble"}}},
                {"$project": {"_id": 0, "accumulatedValue": {"$ifNull": ["$accumulatedValue", 0]}}}
            ]

            result = list(electricity_collection.aggregate(pipeline))

            accumulated_daily.update_one(
                {"date": date},
                {"$set": {
                    "complete": data_is_complete(list(electricity_data)[0]["data"]),
                    "accumulatedValue": result[0]['accumulatedValue']
                }},
                upsert=True
            )
        except:
            accumulated_daily.update_one(
                {"date": date},
                {"$set": {
                    "complete": False,
                    "accumulatedValue": 0
                }},
                upsert=True
            )
        

        print(f"Cached accumulated daily electricity data for date {date}")
        accumulated_daily_data = accumulated_daily.find_one({"date": date})

    return accumulated_daily_data

def get_day_accumulated_interval(start_date_str, end_date_str):
    start_date = format_date_dashes(start_date_str)
    end_date = format_date_dashes(end_date_str)

    count_accumulated_data = accumulated_daily.count_documents(
        {"date": {"$gte": start_date, "$lte": end_date}, "complete": True}
    )

    days_in_interval = (end_date - start_date).days + 1

    if count_accumulated_data >= days_in_interval:
        print(
            f"Found cached accumultaed electricity data for date {start_date_str} - {end_date_str}"
        )

    else:
        # First of all, try to get all the data in a single request just to cache it to our mongo
        try:
            get_electricity_data_interval(start_date_str, end_date_str)
        except Exception:
            iterator_date = start_date
            while iterator_date <= min(end_date, datetime.now()):
                get_day_accumulated_electricity_data(iterator_date)
                iterator_date = iterator_date + timedelta(days=1)

        pipeline = [
            {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
            {"$unwind": "$data"},
            {"$group": {"_id": {"date": "$date", "complete": "$complete"}, "total": {"$sum": 1}, "accumulatedValue": {"$sum": "$data.valueDouble"}}},
            {"$project": {"_id": 0, "date": "$_id.date", "complete": "$_id.complete", "accumulatedValue": 1}},
            {"$sort": {"date": 1}}
        ]
        result = list(electricity_collection.aggregate(pipeline))

        for doc in result:
            date = doc['date']
            filter_query = {"date": date}
            update_query = {"$set": {"date": date, "complete": doc["complete"], "accumulatedValue": doc["accumulatedValue"]}}
            accumulated_daily.update_one(filter_query, update_query, upsert=True)

    # Now that we have the data cached, we can query it
    result = list(accumulated_daily.aggregate([
        {
            "$match": {
                "date": {
                    "$gte": start_date,
                    "$lte": end_date
                },
                "complete": True
            }
        },
        {
            "$group": {
                "_id": None,
                "accumulated_data": {"$sum": "$accumulatedValue"},
                "last_complete": {"$last": "$date"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$last_complete"}},
                "accumulatedValue": {"$round": ["$accumulated_data", 3]}
            }
        }
    ]))
    return result[0]


def get_all_month_accumulated(month):

    start_date = datetime.strptime(month, "%Y-%m-%d")
    num_days = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date = datetime(year=start_date.year,
                        month=start_date.month, day=num_days)
    get_day_accumulated_interval(month, end_date.strftime("%Y-%m-%d"))
    pipeline = [
        {
            "$match": {
                "date": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": "$date",
                "accumulatedValue": {"$max": "$accumulatedValue"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$_id"}},
                "accumulatedValue": {"$ifNull": ["$accumulatedValue", 0]}
            }
        },
        {
            "$sort": {"date": 1}
        }
    ]

    result = list(accumulated_daily.aggregate(pipeline))
    return result


def get_all_year_accumulated(year):
    get_year_accumulated_electricity_data(year)
    start_date = datetime(year=year, month=1, day=1)
    end_date = datetime(year=year, month=12, day=1)

    pipeline = [
        {
            "$match": {
                "date": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"}
                },
                "accumulatedValue": {"$max": "$accumulatedValue"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": {"$dateToString": {"format": "%Y-%m", "date": {
                    "$dateFromParts": {
                        "year": "$_id.year",
                        "month": "$_id.month",
                    }
                }, }},
                "accumulatedValue": {"$ifNull": ["$accumulatedValue", 0]}
            }
        },
        {
            "$sort": {"date": 1}
        }
    ]
    result = list(accumulated_monthly.aggregate(pipeline))

    for i in range(len(result), 12):
        result.append({'date': str(year) + '-' +
                      str(i+1), 'accumulatedValue': 0})
    return result


if __name__ == "__main__":
    # These functions will try to fetch data from MongoDB.
    # If not present, it will fetch from the external API and update the MongoDB cache
    # get_electricity_data("22/02/2023")
    # get_electricity_data_interval("03/02/2023", "06/02/2023")
    # get_accumulated_electricity_data("2023-03-01")
    # get_year_accumulated_electricity_data(2023)
    # get_day_accumulated_electricity_data("2023-04-25")
    # get_day_accumulated_interval("2023-05-01", "2023-05-03")
    # get_all_year_accumulated(2023)
    get_all_month_accumulated('2023-05-01')
    pass
