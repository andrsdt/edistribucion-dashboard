from datetime import datetime, timedelta
import graphene
from utils import get_previous_date

from worker import get_electricity_data_interval, get_day_accumulated_interval, get_all_month_accumulated, get_all_year_accumulated

class Measurement(graphene.ObjectType):
    date = graphene.Date()
    hour = graphene.Int()
    invoiced = graphene.Boolean()
    typePM = graphene.String()
    valueDouble = graphene.Float()
    obtainingMethod = graphene.String()
    cups = graphene.String()
    real = graphene.Boolean()
    value = graphene.Float()

class DailyMeasurements(graphene.ObjectType):
    date = graphene.Date()
    measurements = graphene.List(Measurement)

class AccumulatedData(graphene.ObjectType):
    date = graphene.String()
    accumulatedValue = graphene.Float()


class ConsumptionDifference(graphene.ObjectType):
    accumulativeData = graphene.List(AccumulatedData)
    delta = graphene.String()
    deltaType = graphene.String()


class Query(graphene.ObjectType):
    daily_measurements = graphene.List(
        DailyMeasurements, start_date=graphene.String(), end_date=graphene.String()
    )

    accumulated_data = graphene.List(
        AccumulatedData, year=graphene.Int()
    )

    accumulated_monthly_data = graphene.List(
        AccumulatedData, month=graphene.String()
    )

    consumption_difference = graphene.Field(ConsumptionDifference, month=graphene.String())

    def resolve_daily_measurements(self, _, start_date=None, end_date=None):
        try:
            results = get_electricity_data_interval(start_date, end_date)
            daily_measurements = []
            for result in results:
                date = result["date"] # dd/mm/yyyy (str)
                measurements = [{
                        "hour": hourly_data["hourCCH"] - 1,
                        "value": hourly_data["valueDouble"] if "valueDouble" in hourly_data else None,
                    } for hourly_data in result["data"]]
                    
                daily_measurements.append(
                    DailyMeasurements(
                        date=date,
                        measurements=measurements
                    )
                )
        except Exception:
            daily_measurements = []
            measurements = [{"hour": h, "value": 0} for h in range(24)]
            daily_measurements.append(DailyMeasurements(
                date=datetime.strptime(start_date, "%Y-%m-%d"),
                measurements=measurements
            ))

        return daily_measurements
    
    def resolve_accumulated_data(self, _, year=None):
        accumulated_data = []
        try:
            results = get_all_year_accumulated(year)
            for result in results:
                accumulated_data.append(AccumulatedData(
                        date=result["date"],
                        accumulatedValue=result["accumulatedValue"]
                    ))  
        except Exception:
            pass

        return accumulated_data
    
    def resolve_accumulated_monthly_data(self, _, month=None):
        accumulated_monthly_data = []
        results = get_all_month_accumulated(month)
        for result in results:
            accumulated_monthly_data.append(AccumulatedData(
                    date=result["date"],
                    accumulatedValue=result["accumulatedValue"]
                ))  
        return accumulated_monthly_data

    def resolve_consumption_difference(self, info, month=None):
        start_date = datetime.strptime(month, "%Y-%m-%d").date()
        end_date = (start_date.replace(day=1, month=(start_date.month % 12) + 1)) - timedelta(days=1)
        if (start_date > end_date): # if month is december
            end_date = end_date.replace(year=end_date.year + 1)
        previous_month_obj = get_previous_date(end_date)
        accumulated_current_month = get_day_accumulated_interval(start_date.strftime("%Y-%m-%d"),end_date.strftime("%Y-%m-%d"))

        consumption_difference = []
        consumption_difference.append(AccumulatedData(
            date=accumulated_current_month["date"],
            accumulatedValue=accumulated_current_month["accumulatedValue"]
        ))

        current_value = accumulated_current_month["accumulatedValue"]

        number_of_days_in_previous_month = (end_date.replace(day=1) - timedelta(days=1)).day
        previous_end_date = datetime.strptime(accumulated_current_month["date"], "%Y-%m-%d")
        previous_end_date = previous_end_date.replace(year=previous_month_obj.year, month=previous_month_obj.month, day=min(previous_end_date.day, number_of_days_in_previous_month))
        accumulated_prev_month = get_day_accumulated_interval(previous_month_obj.date().strftime("%Y-%m-%d"),previous_end_date.date().strftime("%Y-%m-%d")) 

        consumption_difference.append(AccumulatedData(
            date=accumulated_prev_month["date"],
            accumulatedValue=accumulated_prev_month["accumulatedValue"]
        ))

        prev_value = accumulated_prev_month["accumulatedValue"]

        delta = round((current_value - prev_value) / prev_value * 100, 2)
        delta_type = "increase" if delta > 0 else "decrease"

        return ConsumptionDifference(
            accumulativeData=consumption_difference,
            delta=str(delta)+'%',
            deltaType=delta_type
        )

schema = graphene.Schema(query=Query)