from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from werkzeug.exceptions import abort
from gameRec import gameDataAccess
from gameRec.gameDataAccess import dataSingleton

bp = Blueprint("gameLibrary", __name__)

@bp.route("/testSelGameById")
def testSelGameById():
    return str(gameDataAccess.getGameInfo([10, 20]))
@bp.route("/testSearchGame")
def testSearchGame():
    retStr = ""
    games = gameDataAccess.getSearchGameList(page = 0, keyword = 'final')
    for x in games:
        retStr += x['title'] +", " + x['company'] + ", " + x['platform'] + ", " + x['genre']+  "<br>"
    return retStr

@bp.route("/testSearchGameCnt")
def testSearchGameCnt():
    cnt = gameDataAccess.getSearchGameCnt()
    return str(cnt)
@bp.route("/testGamePageDetail")
def testGamePageDetail():
    #retStr = ""
    retVal = gameDataAccess.getGamePageDetail(page = 0, keyword = 'final')

    return str(retVal)


@bp.route("/testGameImage")
def testGameImage():
    return str(gameDataAccess.getGameImageName([10, 20]))

@bp.route("/testCompanyLst")
def testCompanyLst():
    return str(dataSingleton.getCompanyLst())
@bp.route("/testPlatformLst")
def testPlatformLst():
    return str(dataSingleton.getPlatformLst())
@bp.route("/testGenreLst")
def testGenreLst():
    return str(dataSingleton.getGenreLst())





@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/gameDetail/<int:gameId>")
def gameDetail(gameId):
    gameDetail = gameDataAccess.getGameInfo([gameId])
    gameImageInfo = gameDataAccess.getGameImageName([gameId])
    if len(gameDetail) == 0 or len(gameImageInfo) == 0:
        abort(404, "game id {0} doesn't exist.".format(gameId))
    gameDetail = gameDetail[0]
    gameImageInfo = gameImageInfo[0]
    return render_template("gameDetail.html", gameDetail = gameDetail, gameImageInfo = gameImageInfo)

@bp.route("/search")
def searchGame():
    return render_template("gameLst.html")

@bp.route("/searchInitGameLst", methods=['POST'])
def initGameLstPage():
    if request.method == 'POST':
        keyword = request.form['keyword']
        return jsonify(gameDataAccess.getGamePageDetail(page = 0, keyword = keyword))
    else:
        abort(404, "Error")

@bp.route("/searchRefreshGameLst", methods=['POST'])
def searchRefreshGameLst():
    if request.method == 'POST':
        #import pdb
        #pdb.set_trace();
        import json
        genre =  json.loads(request.form['genre'])
        platform = json.loads(request.form['platform'])
        company = [] ## TODO:  add company filter
        #company = json.loads(request.form['company'])
        page = int(request.form['pageIndex'])
        keyword = request.form['keyword']
        print("Genre:\n")
        print(str(genre))
        print("\nPlatform:\n")
        print(str(platform))
        print("\ncompany\n")
        print(str(company))
        print("\nkeyword:" + keyword + "\npage:" + str(page))
        return jsonify(gameDataAccess.getGamePageDetail(page = page, keyword = keyword, genre =genre, company = company, platform = platform))
    else:
        abort(404, "Error")
