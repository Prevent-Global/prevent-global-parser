import sqlite3
from sqlite3 import Error


def create_db(db_file='prevent.db'):
    """ create a database specified by db_file
    :param db_file: database file
    :return:
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            print(f'db {db_file} created succesfully')
            conn.close()

def create_connection(db_file='prevent.db'):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_places_table(conn):
    """ create a places table
    :param conn: Connection object
    :return:
    """

    sql_create_places_table = """ CREATE TABLE IF NOT EXISTS places (
                                    id integer PRIMARY KEY,
                                    latE7 integer NOT NULL,
                                    lonE7 integer NOT NULL,
                                    address text
                                ); """

    create_table(conn, sql_create_places_table)

def create_visits_table(conn):
    """ create a visits table
    :param conn: Connection object
    :return:
    """

    sql_create_visits_table = """ CREATE TABLE IF NOT EXISTS visits (
                                    id integer PRIMARY KEY,
                                    place_id integer NOT NULL,
                                    beg integer NOT NULL,
                                    end integer NOT NULL,
                                    FOREIGN KEY (place_id) REFERENCES places (id)
                                ); """

    create_table(conn, sql_create_visits_table)

def setup(db_file='prevent.db'):
    """ create a database and add places and visits tables
    :param db_file: database file
    :return:
    """
    conn = create_connection(db_file)
    create_places_table(conn)
    create_visits_table(conn)

def add_place(conn, place):
    """
    Create a new place in the places table
    :param conn:
    :param place: a triple (latE7, lonE7, address)
    :return: place id
    """
    sql = ''' INSERT INTO places(latE7, lonE7, address) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, place)
    return cur.lastrowid

def add_visit(conn, visit):
    """
    Create a new visit in the visits table
    :param conn:
    :param visit: a triple(place_id, beg, end)
    :return: visit id
    """
    sql = ''' INSERT INTO visits(place_id, beg, end) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, visit)
    return cur.lastrowid

def delete_place(conn, id):
    """
    Delete a place by place id
    :param conn:  Connection to the SQLite database
    :param id: id of the place
    :return:
    """
    sql = 'DELETE FROM places WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_visit(conn, id):
    """
    Delete a visit by visit id
    :param conn:  Connection to the SQLite database
    :param id: id of the visits
    :return:
    """
    sql = 'DELETE FROM visits WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_all_places(conn):
    """
    Delete all rows in the places table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM places'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def delete_all_visits(conn):
    """
    Delete all rows in the visits table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM visits'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def select_place_by_coordinates(conn, coordinates):
    """
    Query places by coordinates
    :param conn: the Connection object
    :param coordinates: a tuple (latE7, lonE7) of (int, int)
    :return: a list of places
    """

    cur = conn.cursor()
    cur.execute("SELECT * FROM places WHERE latE7=? and lonE7=?", coordinates)

    return cur.fetchall()

def select_place_by_coordinates(conn, coordinates):
    """
    Query places by coordinates
    :param conn: the Connection object
    :param coordinates: a tuple (latE7, lonE7) of (int, int)
    :return: a list of places
    """

    cur = conn.cursor()
    cur.execute("SELECT * FROM places WHERE latE7=? and lonE7=?", coordinates)

    return cur.fetchall()

def find_place_id(conn, place):
    """
    Query places to find the place id
    :param conn:
    :param place: a triple (latE7, lonE7, address)
    :return: place id
    """

    cur = conn.cursor()
    cur.execute("SELECT * FROM places WHERE latE7=? and lonE7=? and address=?", place)

    places = cur.fetchall()
    if len(places):
        return places[0][0]

    return None

def select_all_places(conn):
    """
    Select all rows in the places table
    :param conn: Connection to the SQLite database
    :return: all rows in places table
    """

    sql = 'SELECT * FROM places'
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()

def select_all_visits(conn):
    """
    Select all rows in the visits table
    :param conn: Connection to the SQLite database
    :return: all rows in visits table
    """

    sql = 'SELECT * FROM visits'
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()
