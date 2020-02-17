from sqlalchemy import create_engine


def sql_to_json(obj, keys):
    jsonify = dict((x[0],dict(zip(keys[1:], x[1:]))) for x in obj )
    return jsonify


def create_session():
    return create_engine('sqlite:////home/taysai/app/db/data.sqlite', echo=False)