import sqlite3
from sqlite3 import Error


def createConnection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def createUser(conn, user):
    """
    Create a new project into the Users table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' INSERT INTO Users(username,subLevel,inviteLink,description,lastShareTime)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def getData(conn):
    """
    Query all enities in the Users table
    :param conn: the Connection object
    :return: rows
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")

    rows = cur.fetchall()
    return rows


def updateTime(conn, data):
    """
    update the lastShareTime of a user
    :param conn:
    :param data:
    """
    sql = ''' UPDATE Users
              SET lastShareTime = ?
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()


def getTime(conn, data):
    """
    return the lastShareTime of a user
    :param conn
    :param data
    :return: Hours since last share
    """
    sql = ''' SELECT (strftime('%s','now') - strftime('%s',lastShareTime)) / 3600
              FROM Users
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    hoursSinceShare = cur.fetchall()
    conn.commit()
    return hoursSinceShare


def updateDescription(conn, data):
    """
    update description of a server
    :param conn:
    :param data:
    :return: project id
    """
    sql = ''' UPDATE Users
              SET description = ?
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()


def main():
    database = r"bot"

    # create a database connection
    conn = createConnection(database)
    # create a new project
    # user = ('Admin', '3', 'google.com',"","9:19:52")
    # userID = createUser(conn, user)
    test = getTime(conn, ["Sadeed"])
    # test = getData(conn)
    print(test)


if __name__ == '__main__':
    main()
