import graphene

from mongo import electricity_collection
from utils import format_date


class Measurement(graphene.ObjectType):
    date = graphene.DateTime()
    hour = graphene.Int()
    invoiced = graphene.Boolean()
    typePM = graphene.String()
    valueDouble = graphene.Float()
    obtainingMethod = graphene.String()
    cups = graphene.String()
    real = graphene.Boolean()
    value = graphene.Float()


class Query(graphene.ObjectType):
    measurements = graphene.List(
        Measurement, start_date=graphene.String(), end_date=graphene.String()
    )

    def resolve_measurements(self, info, start_date=None, end_date=None):

        query = {}
        if start_date:
            start_date = format_date(start_date)
            query["date"] = {"$gte": start_date}
        if end_date:
            end_date = format_date(end_date)
            if "date" in query:
                query["date"]["$lte"] = end_date
            else:
                query["date"] = {"$lte": end_date}

        results = electricity_collection.find(query)

        measurements = []
        for result in results:
            for data in result["data"]:
                date = result["date"].replace(hour=data["hourCCH"] - 1)
                measurement = Measurement(
                    date=date, value=data["valueDouble"]
                )
                measurements.append(measurement)
        return measurements


schema = graphene.Schema(query=Query)
