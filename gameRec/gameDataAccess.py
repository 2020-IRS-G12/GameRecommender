from flask import g
from gameRec.db import get_db

ITEM_ONE_PAGE = 10
def getGameInfo(idArr):
    db = get_db()
    idStrArr = list(map(str, idArr))
    result = db.execute('SELECT * FROM GameDetail WHERE gameId IN (%s)' %
                           ','.join('?'*len(idStrArr)), idStrArr)
    result = result.fetchall()
    retVal = list()
    for i in result:
        retVal.append(dict(i))
    return retVal

def getGameImageName(idArr):
    db = get_db()
    idStrArr = list(map(str, idArr))
    result = db.execute('SELECT * FROM GameImages WHERE gameId IN (%s)' %
                           ','.join('?'*len(idStrArr)), idStrArr)
    result = result.fetchall()
    retVal = [dict(x) for x in result]
    return retVal

def searchGameList(page, genre = [], company = [], platform = [], keyword = ""):
    db = get_db()

    #Select * From Account Limit 9 Offset 10;
    sqlCommand = ""
    if len(company) > 0:
        sqlCommand += """
            SELECT gameId FROM GameDetail WHERE company IN (%s)
            INTERSECT """ % (','.join([("'"+c+"'") for c in company]))
    if len(platform) > 0:
        sqlCommand +="""
            SELECT gameId FROM GameDetail WHERE platform IN (%s)
            INTERSECT """ % (','.join([("'"+p+"'") for p in platform]))

    sqlCommand += """SELECT d.gameId FROM
        GameDetail AS d INNER JOIN GenreStat AS s WHERE
        d.gameId = s.gameId """
    for i in genre:
        sqlCommand += (" AND s.%s = 1 "%(i))

    sqlCommand = '(' + sqlCommand + ')'
    sqlCommand = "SELECT * FROM GameDetail WHERE gameId IN " + sqlCommand;
    if keyword != "":
        sqlCommand += " AND title LIKE '%" + keyword + "%' "

    sqlCommand += " ORDER BY score DESC "
    sqlCommand += " LIMIT " + str(ITEM_ONE_PAGE) + " OFFSET " + str(ITEM_ONE_PAGE * page)
    print(sqlCommand)
    result = db.execute(sqlCommand)
    result = result.fetchall()

    #d = {x:x*10 for x in range(3)}
    retVal = list()
    for x in result:
        retVal.append(dict(x))
    return retVal
