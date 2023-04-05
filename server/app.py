# Importing Flask to be our HTTP server
import logging

from flask import Flask, send_from_directory
from flask_cors import CORS
from graphql_server.flask import GraphQLView

from schema import schema

# Importing this view so Flask can delegate to Graphene
app = Flask(__name__, static_url_path="", static_folder="client/dist")
CORS(app)  # TODO: comment this on deployment

# Adding another route for GraphQL at /graphql
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.route("/", defaults={"path": ""})
def serve(path):
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
