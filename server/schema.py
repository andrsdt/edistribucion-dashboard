from datetime import timedelta, datetime
import graphene
from dateutil.relativedelta import relativedelta

from worker import get_electricity_data_interval, get_year_accumulated_electricity_data, get_accumulated_electricity_data

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


# TODO: At the moment is not the difference to the same period of the previous month
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

    def resolve_daily_measurements(self, info, start_date=None, end_date=None):

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

        return daily_measurements
    
    def resolve_accumulated_data(self, info, year=None):

        data = get_year_accumulated_electricity_data(year)

        accumulated_data = []
        num_months = 0
        while num_months < 12:
            if num_months < len(data):
                accumulated_data.append(
                    AccumulatedData(
                        date=data[num_months]["date"].strftime("%Y-%m"),
                        accumulatedValue=data[num_months]["accumulatedValue"]
                    )
                )
            else:
                accumulated_data.append(
                    AccumulatedData(
                        date=datetime(year=year, month=num_months+1, day=1).strftime("%Y-%m"),
                        accumulatedValue=0
                    )
                )
            num_months += 1

        return accumulated_data
    
    def resolve_accumulated_monthly_data(self, info, month=None):

        result = get_accumulated_electricity_data(month)

        accumulated_monthly_data = []
        accumulated_monthly_data.append(AccumulatedData(
            date=result["date"].strftime("%Y-%m"),
            accumulatedValue=result["accumulatedValue"]
        ))

        return accumulated_monthly_data
    
    def resolve_consumption_difference(self, info, month=None):
 
        result = get_accumulated_electricity_data(month)

        consumption_difference = []
        consumption_difference.append(AccumulatedData(
            date=result["date"].strftime("%Y-%m"),
            accumulatedValue=result["accumulatedValue"]
        ))

        actual_value = result["accumulatedValue"]

        month_obj = datetime.strptime(month, "%Y-%m-%d")
        previous_month_obj = month_obj - relativedelta(months=1)
        previous_month_str = previous_month_obj.strftime("%Y-%m-%d")
        
        result = get_accumulated_electricity_data(previous_month_str)

        consumption_difference.append(AccumulatedData(
            date=result["date"].strftime("%Y-%m"),
            accumulatedValue=result["accumulatedValue"]
        ))

        prev_value = result["accumulatedValue"]

        delta = round((actual_value - prev_value) / prev_value * 100, 2)
        delta_type = ""
        if delta > 0:
            delta_type = "increase"
        else:
            delta_type = "decrease"

        return ConsumptionDifference(
            accumulativeData=consumption_difference,
            delta=str(delta)+'%',
            deltaType=delta_type
        )


schema = graphene.Schema(query=Query)