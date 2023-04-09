import graphene

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
        for result in data:
            accumulated_data.append(
                AccumulatedData(
                    date=result["date"].strftime("%Y-%m"),
                    accumulatedValue=result["accumulatedValue"]
                )
            )

        return accumulated_data
    
    def resolve_accumulated_monthly_data(self, info, month=None):

        result = get_accumulated_electricity_data(month)

        accumulated_monthly_data = []
        accumulated_monthly_data.append(AccumulatedData(
            date=result["date"].strftime("%Y-%m"),
            accumulatedValue=result["accumulatedValue"]
        ))

        return accumulated_monthly_data


schema = graphene.Schema(query=Query)