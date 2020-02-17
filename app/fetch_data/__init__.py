import sqlalchemy as db


def sql_to_json(obj, keys):
    jsonify = dict((x[0],dict(zip(keys[1:], x[1:]))) for x in obj )
    return jsonify


def create_session():
    return db.create_engine("mysql+pymysql://root:@localhost/python-galaxies"
                     .format(user="root",
                             pw="",
                             db="python-galaxies"))
