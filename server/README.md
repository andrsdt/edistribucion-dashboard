# python-graphene-graphql

Sample app for making a GraphQL API using Graphene in a Django server

## What is here

| Files | Purpose |
|---|---|
| LICENSE | Everything needs a license, this uses APL 2.0 |
| README.md | This file |
| .gitignore | What files git should ignore during operations |
| requirements.txt | All the defined packages which this uses (on Rocky 8.5) |
| app.py | Flask based server that accepts requests and routes |
| schema.py | The actual GraphQL code using Graphene  |
| schema.gql | Schema that the code generates and responds to |

# Using this

These commands assume a version Python 3.9 binary is installed.

```
python3.9 -m venv python-graphene-graphql-ve
source python-graphene-graphql-ve/bin/activate
pip install -U pip
pip install -r requirements.txt
flask run --host 0.0.0.0
```
