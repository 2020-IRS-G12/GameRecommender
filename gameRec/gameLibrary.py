from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from gameRec import gameDataAccess

bp = Blueprint("gameLibrary", __name__)

@bp.route("/testSelGameById")
def testSelGameById():
    return str(gameDataAccess.getGameInfo([10, 20]))
@bp.route("/testSearchGame")
def testSearchGame():
    retStr = ""
    games = gameDataAccess.getGameList(page = 0, keyword = 'final')
    for x in games:
        retStr += x['title'] +", " + x['company'] + ", " + x['platform'] + ", " + x['genre']+  "<br>"
    return retStr

@bp.route("/testGameImage")
def testGameImage():
    return str(gameDataAccess.getGameImageName([10, 20]))
