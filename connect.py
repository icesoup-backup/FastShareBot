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
    Create a new entry in the Users table
    :param conn: Connection object
    :param user: [username,guildName,inviteLink]
    :return: user id
    """
    sql = ''' INSERT INTO Users(username,guildName,inviteLink)
              VALUES(?,?,?) '''
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


def getSubLevel(conn, data):
    """
    returns the subLevel of a user
    :param conn: connection object
    :param data: Username
    :return: subLevel
    """
    sql = ''' SELECT subLevel
              FROM Users
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    subLevel = cur.fetchone()
    return subLevel


def getGuild(conn, data):
    """
    returns the guildName of a user
    :param conn
    :param data
    :return: guildName
    """
    sql = ''' SELECT guildName
              FROM Users
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    guildName = cur.fetchone()
    return guildName


def updateTime(conn, data):
    """
    update the lastShareTime of a user
    :param conn:
    :param data:
    """
    sql = ''' UPDATE Users
              SET lastShareTime = datetime('now')
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()


def getTime(conn, data):
    """
    returns the lastShareTime of a user
    :param conn
    :param data
    :return: Hours since last share
    """
    sql = ''' SELECT (strftime('%s','now') - strftime('%s',lastShareTime))
              FROM Users
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    hoursSinceShare = cur.fetchone()
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


def getAutoMsgData(conn):
    """
    get data to display in a message
    :param conn:
    :return: data of users with subLvl >= 2
    """
    sql = ''' SELECT guildName, inviteLink, description FROM Users
              WHERE subLevel >= 2 '''
    cur = conn.cursor()
    cur.execute(sql)
    msgData = cur.fetchall()
    return msgData


# def main():
#     database = r"bot"

#     # create a database connection
#     conn = createConnection(database)
#     # create a new project
#     # user = ('Admin', '3', 'google.com',"","9:19:52")
#     # userID = createUser(conn, user)
#     # test = getTime(conn, ["Sadeed"])[0]
#     # test = getData(conn)
#     # print(str(datetime.timedelta(seconds=test)).split(":"))
#     test = getAutoMsgData(conn)
#     print(test[0][0])


# if __name__ == '__main__':
#     main()
