from flask import Flask
from flask_cors import CORS
from graphql_server.flask import GraphQLView

from schema import schema

# Importing this view so Flask can delegate to Graphene
app = Flask(__name__)
CORS(app)

# Adding another route for GraphQL at /graphql
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=False)
