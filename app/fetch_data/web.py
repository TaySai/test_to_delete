import sqlalchemy as db
import app.fetch_data as fd

def get_data(galaxy, messier):
    engine = fd.create_session()
    connection = engine.connect()
    metadata = db.MetaData()
    con_table = db.Table('data_galaxies', metadata, autoload=True, autoload_with=engine)
    if galaxy is None:
        query = db.select([con_table]).where(con_table.columns.messier_name.like('%'+messier+'%'))
    elif messier is None:
        query = db.select([con_table]).where(con_table.columns.galaxy_name.like('%'+galaxy+'%'))
    else:
        query = db.select([con_table]).where(
            db.and_(con_table.columns.messier_name.like('%'+messier+'%'), con_table.columns.galaxy_name.like('%'+galaxy+'%')))
    res = connection.execute(query)
    cols = res.keys()
    return fd.sql_to_json(res, cols)

def get_galaxies():
    engine = fd.create_session()
    connection = engine.connect()
    metadata = db.MetaData()
    con_table = db.Table('data_galaxies', metadata, autoload=True, autoload_with=engine)

    query = db.select([con_table.columns.galaxy_name])
    res = connection.execute(query)
    res = fd.sql_to_json(res, res.keys())
    return list(res.keys())


def get_messiers():
    engine = fd.create_session()
    connection = engine.connect()
    metadata = db.MetaData()
    con_table = db.Table('data_galaxies', metadata, autoload=True, autoload_with=engine)

    query = db.select([con_table.columns.messier_name])
    res = connection.execute(query)
    res = fd.sql_to_json(res, res.keys())
    return list(res.keys())

def get_endpoint_web_galaxy(val):
    engine = fd.create_session()
    connection = engine.connect()
    metadata = db.MetaData()
    con_table = db.Table('data_galaxies', metadata, autoload=True, autoload_with=engine)
    query = db.select([con_table]).where(con_table.columns.galaxy_name == val)
    res = connection.execute(query)
    cols = res.keys()
    return fd.sql_to_json(res, cols)

def get_endpoint_web_messier(val):
    engine = fd.create_session()
    connection = engine.connect()
    metadata = db.MetaData()
    con_table = db.Table('data_galaxies', metadata, autoload=True, autoload_with=engine)
    query = db.select([con_table]).where(con_table.columns.messier_name == val)
    res = connection.execute(query)
    cols = res.keys()
    return fd.sql_to_json(res, cols)