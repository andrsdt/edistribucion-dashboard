from datetime import timedelta, datetime
import graphene
from dateutil.relativedelta import relativedelta
from utils import format_date_dashes
import calendar

from worker import get_electricity_data_interval, get_year_accumulated_electricity_data, get_accumulated_electricity_data, get_day_accumulated_electricity_data

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
    
    # def resolve_accumulated_monthly_data(self, info, month=None):

    #     result = get_accumulated_electricity_data(month)

    #     accumulated_monthly_data = []
    #     accumulated_monthly_data.append(AccumulatedData(
    #         date=result["date"].strftime("%Y-%m"),
    #         accumulatedValue=result["accumulatedValue"]
    #     ))

    #     return accumulated_monthly_data
    

    ### TODO: ANOTHER WAY OF MAKING THE GRAPH JUST WITH THE AVAILABLE DATA
    # def resolve_accumulated_monthly_data(self, info, month=None):
    #     start_date = datetime.strptime(month, "%Y-%m-%d").date()

    #     current_date = datetime.today()
    #     if start_date.year == current_date.year and start_date.month == current_date.month:
    #         end_date_str = start_date.replace(day=current_date.day-1).strftime("%Y-%m-%d")
    #         end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    #     else:
    #         num_days = calendar.monthrange(start_date.year, start_date.month)[1]
    #         end_date_str = start_date.replace(day=num_days).strftime("%Y-%m-%d")
    #         end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    #     # Creamos un bucle que itere sobre los días intermedios
    #     current_date = start_date
    #     accumulated_monthly_data = []
    #     while current_date <= end_date:
    #         result = get_day_accumulated_electricity_data(current_date.strftime("%Y-%m-%d"))
    #         accumulated_monthly_data.append(AccumulatedData(
    #             date=result["date"].strftime("%Y-%m-%d"),
    #             accumulatedValue=result["accumulatedValue"]
    #         ))
    #         current_date += timedelta(days=1)

    #     return accumulated_monthly_data

    def resolve_accumulated_monthly_data(self, info, month=None):

        start_date = datetime.strptime(month, "%Y-%m-%d").date()

        accumulated_monthly_data = []
        num_days = calendar.monthrange(start_date.year, start_date.month)[1]
        for i in range(1, num_days+1):
            current_date = datetime(start_date.year, start_date.month, i)
            if current_date.date() < datetime.today().date():
                result = get_day_accumulated_electricity_data(current_date.strftime("%Y-%m-%d"))
                accumulated_monthly_data.append(AccumulatedData(
                    date=result["date"].strftime("%Y-%m-%d"),
                    accumulatedValue=result["accumulatedValue"]
                ))   
            else:
                accumulated_monthly_data.append(AccumulatedData(
                    date=current_date.strftime("%Y-%m-%d"),
                    accumulatedValue=0
                ))

        print(accumulated_monthly_data)
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