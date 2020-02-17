import sqlalchemy as db

import fetch_data as fd

def get_data(data):
    engine = create_session()
    connection = engine.connect()
    metadata = db.MetaData()
    con_table = db.Table('data_galaxies', metadata, autoload=True, autoload_with=engine)
    collection = []
    for item in data:
        if 'galaxy_name' in item or 'messier_name' in item:
            print(item.keys())
            if 'galaxy_name' in item and 'messier_name' in item:
                query = db.select([con_table]).where(con_table.columns.galaxy_name.like('%'+item['galaxy_name']+'%'), con_table.columns.messier_name.like('%'+item['messier_name']+'%'))
            elif 'messier_name' in item:
                query = db.select([con_table]).where(con_table.columns.messier_name.like('%'+item['messier_name']+'%'))
            else:
                query = db.select([con_table]).where(con_table.columns.galaxy_name.like('%'+item['galaxy_name']+'%'))
            res = connection.execute(query)
            cols = res.keys()
            collection.append(fd.sql_to_json(res, cols))
        else:
            collection.append({'error':'not good key'})
    return collection
