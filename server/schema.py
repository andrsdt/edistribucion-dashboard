from datetime import timedelta, datetime
import graphene
from dateutil.relativedelta import relativedelta
import calendar
from utils import get_end_and_previous_date

from worker import get_electricity_data_interval, get_year_accumulated_electricity_data, get_day_accumulated_electricity_data

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

    def resolve_daily_measurements(self, info, start_date=None, end_date=None):
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
        except:
            daily_measurements = []
            measurements = [{"hour": h, "value": 0} for h in range(24)]
            daily_measurements.append(DailyMeasurements(
                date=datetime.strptime(start_date, "%Y-%m-%d"),
                measurements=measurements
            ))

        print(daily_measurements)
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

        start_date = datetime.strptime(month, "%Y-%m-%d").date()

        accumulated_monthly_data = []
        num_days = calendar.monthrange(start_date.year, start_date.month)[1]
        for i in range(1, num_days+1):
            current_date = datetime(start_date.year, start_date.month, i)
            result = get_day_accumulated_electricity_data(current_date.strftime("%Y-%m-%d"))
            if result["accumulatedValue"]>0:
                accumulated_monthly_data.append(AccumulatedData(
                    date=result["date"].strftime("%Y-%m-%d"),
                    accumulatedValue=result["accumulatedValue"]
                ))   
            else:
                accumulated_monthly_data.append(AccumulatedData(
                    date=current_date.strftime("%Y-%m-%d"),
                    accumulatedValue=0
                ))

        return accumulated_monthly_data

    def resolve_consumption_difference(self, info, month=None):
        start_date = datetime.strptime(month, "%Y-%m-%d").date()
        current_date = datetime.today().date()
        (end_date, previous_month_obj, previous_end_date) = get_end_and_previous_date(start_date, current_date)

        iterator_date = start_date
        accumulated_data = 0
        while iterator_date <= end_date:
            result = get_day_accumulated_electricity_data(iterator_date.strftime("%Y-%m-%d"))
            if not result["complete"]:
                day_last_complete=result["date"].day
                break
            accumulated_data += result["accumulatedValue"]
            iterator_date += timedelta(days=1)

        consumption_difference = []
        consumption_difference.append(AccumulatedData(
            date=end_date.strftime("%Y-%m-%d"),
            accumulatedValue=round(accumulated_data, 3)
        ))

        current_value = accumulated_data

        iterator_date = previous_month_obj.date()
        accumulated_data = 0
        while iterator_date <= previous_end_date:
            if iterator_date.day == day_last_complete:
                break
            result = get_day_accumulated_electricity_data(iterator_date.strftime("%Y-%m-%d"))
            accumulated_data += result["accumulatedValue"]
            iterator_date += timedelta(days=1)
        

        consumption_difference.append(AccumulatedData(
            date=previous_end_date.strftime("%Y-%m-%d"),
            accumulatedValue=round(accumulated_data, 3)
        ))

        prev_value = accumulated_data

        delta = round((current_value - prev_value) / prev_value * 100, 2)
        delta_type = "increase" if delta > 0 else "decrease"

        return ConsumptionDifference(
            accumulativeData=consumption_difference,
            delta=str(delta)+'%',
            deltaType=delta_type
        )

schema = graphene.Schema(query=Query)