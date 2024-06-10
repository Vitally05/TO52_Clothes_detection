import mysql.connector
import pandas as pd

def create_connection_bdd():
    cnx = mysql.connector.connect(user='root', password='TO52',
                                  host='localhost',
                                  database='clothes_detection')
    return cnx
def construct_query(cat, brand, size):
    query = "SELECT absolute_path FROM clothes NATURAL JOIN category "
    where_category = f"WHERE category = '{cat}' "
    where_brand = ""
    where_size = ""
    first = True

    if brand != 'all':
        query = query + "NATURAL JOIN brand "
        for bd in brand:
            if first:
                where_brand = f"AND (brand = '{bd}' "
                first = False
            else:
                where_brand = where_brand + f"OR brand = '{bd}' "
        if len(brand) > 0:
            where_brand = where_brand + ") "

    first = True
    if size != 'all':
        query = query + "NATURAL JOIN size "
        for sz in size:
            if first:
                where_size = f"AND (size = '{sz}' "
                first = False
            else:
                where_size = where_size + f"OR size = '{sz}' "
        if len(size) > 0:
            where_size = where_size + ") "

    query = query + where_category + where_brand + where_size + "LIMIT 10"

    return query

def get_images_bdd(cat, brand, size):

    cnx = create_connection_bdd()
    query = construct_query(cat, brand, size)
    print(query)

    cursor = cnx.cursor()

    cursor.execute(query)

    df = pd.DataFrame(cursor.fetchall())
    df.columns = cursor.column_names

    cnx.close()
    return df