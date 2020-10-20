from flask import g
from gameRec.db import get_db
from flask import url_for
import numpy

import pdb

ITEM_ONE_PAGE = 8


class DataSingleton(object):
    companyList = None;
    genreList = None;
    platformList = None;
    def getCompanyLst(self):
        if self.companyList == None:
            self.companyList = getCompanyLst()
        return self.companyList

    def getPlatformLst(self):
        if self.platformList == None:
            self.platformList = getPlatformLst()
        return self.platformList

    def getGenreLst(self):
        if self.genreList == None:
            self.genreList = getGenreLst()
        return self.genreList

dataSingleton = DataSingleton()


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

def getSearchGameCnt(genre = [], company = [], platform = [], keyword = ""):
    db = get_db()
    sqlCommand = ""
    if len(company) > 0:
        sqlCommand += """
            SELECT gameId FROM GameDetail WHERE company IN (%s)
            INTERSECT """ % (','.join([("'"+c+"'") for c in company]))
    if len(platform) > 0:
        sqlCommand +="""
            SELECT gameId FROM GameDetail WHERE platform IN (%s)
            INTERSECT """ % (','.join([("'"+p+"'") for p in platform]))
    if keyword != "":
        sqlCommand +="""
            SELECT gameId FROM searchGameTable WHERE title MATCH ('%s')
            OR genre MATCH ('%s')
            OR description MATCH ('%s')
            INTERSECT """ % (keyword, keyword, keyword)

    sqlCommand += """SELECT d.gameId FROM
        GameDetail AS d INNER JOIN GenreStat AS s WHERE
        d.gameId = s.gameId """
    for i in genre:
        sqlCommand += (" AND s.[%s] = 1 "%(i))

    sqlCommand = '(' + sqlCommand + ')'
    sqlCommand = "SELECT COUNT(*) FROM GameDetail WHERE gameId IN " + sqlCommand;

    #if keyword != "":
    #    sqlCommand += " AND title LIKE '%" + keyword + "%' "

    #print(sqlCommand)
    result = db.execute(sqlCommand)
    result = result.fetchone()['count(*)']
    #pdb.set_trace()
    return int(result)

def getSearchGameList(page, genre = [], company = [], platform = [], keyword = ""):
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
    if keyword != "":
        sqlCommand +="""
            SELECT gameId FROM searchGameTable WHERE title MATCH ('%s')
            OR genre MATCH ('%s')
            OR description MATCH ('%s')
            INTERSECT """ % (keyword, keyword, keyword)        

    sqlCommand += """SELECT d.gameId FROM
        GameDetail AS d INNER JOIN GenreStat AS s WHERE
        d.gameId = s.gameId """
    for i in genre:
        sqlCommand += (" AND s.[%s] = 1 "%(i))

    sqlCommand = '(' + sqlCommand + ')'
    sqlCommand = "SELECT * FROM GameDetail WHERE gameId IN " + sqlCommand;
    # if keyword != "":
    #     sqlCommand += " AND title LIKE '%" + keyword + "%' "

    sqlCommand += " ORDER BY score DESC "
    sqlCommand += " LIMIT " + str(ITEM_ONE_PAGE) + " OFFSET " + str(ITEM_ONE_PAGE * page)
    #print(sqlCommand)
    result = db.execute(sqlCommand)
    result = result.fetchall()

    #d = {x:x*10 for x in range(3)}
    retVal = list()
    for x in result:
        retVal.append(dict(x))
    return retVal

def getCompanyLst():
    db = get_db()
    result = db.execute('SELECT company FROM GameDetail')
    allCompanyLst = []
    tempSet = set()
    for i in result:
        tempSet.add(i['company'])
    for j in tempSet:
        allCompanyLst.append(j)
    return allCompanyLst;

def getPlatformLst():
    db = get_db()
    result = db.execute('SELECT platform FROM GameDetail')
    allPlatformLst = []
    tempSet = set()
    for i in result:
        tempSet.add(i['platform'])
    for j in tempSet:
        allPlatformLst.append(j)
    return allPlatformLst;

def getGenreLst():
    db = get_db()
    result = db.execute('PRAGMA table_info(GenreStat)')
    allGenreLst = []
    for i in result:
        if i['name'] != "gameId" and i['name'] != "title":
            allGenreLst.append(i['name'])
    return allGenreLst;

def getGamePageDetail(page, keyword="", genre=[], platform=[], company=[]):
    retVal = {}
    retVal['keyword'] = keyword
    retVal['selectedGenre'] = genre
    retVal['selectedPlatform'] = platform
    retVal['selectedCompany'] = company
    retVal['allGenre'] = dataSingleton.getGenreLst()
    retVal['allPlatform'] = dataSingleton.getPlatformLst()
    retVal['allCompany'] = dataSingleton.getCompanyLst()
    retVal['currentPageLst'] = getSearchGameList(page=page, genre=genre, platform=platform, company=company, keyword=keyword)
    retVal['currentPageIndex'] = page
    retVal['pageCnt'] = int(numpy.ceil(float(getSearchGameCnt(keyword=keyword, genre=genre, company=company, platform=platform)) / float(ITEM_ONE_PAGE)))

    for i in retVal['currentPageLst']:
        i['imageUrl'] = ''
        imgName = getGameImageName([i["gameId"]]);
        if len(imgName) > 0:
            imgName = imgName[0]['imageFileName']
            i['imageUrl'] = url_for('static', filename = 'image/gameImageSmall/' + imgName)
        url = url_for('gameLibrary.gameDetail', gameId=i["gameId"])
        i['gameUrl'] = url


    return retVal

def mergeRecGameLstAndImgInfo(gamelst, imglsts):
    for i in gamelst:
        for j  in imglsts:
            if i['gameId']==j['gameId']:
                i['imageFileName'] = j['imageFileName']
    return gamelst
