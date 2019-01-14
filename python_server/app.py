from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from .common.my_database_meta_data import db_session
from .common.schema import schema, Department

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True #For having the GraphiQL interface
    )
)

CORS(app)

if __name__ == '__main__':
    app.run()