from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from gameRec.db import get_db
from gameRec import gameDataAccess

bp = Blueprint("gameRecQuestionnaire", __name__)

@bp.route("/questionnaire")
def fillQuestionnire():
    return render_template("questionnaire.html")

@bp.route("/recGameLst", methods=['POST'])
def recGameLst():
    if request.method == 'POST':
        #import pdb
        #pdb.set_trace();
        import json
        info =  json.loads(request.form['questionnaireJsonInfo'])
        #print(info)
        from recommendAlgo import CustomizedRecommendation as customRec
        recGameJson = customRec.CustomizedRecommendation().getRecommendation(get_db(), info['selPlatformSet'], info['selGenreSet'],16)
        recGameLst = json.loads(recGameJson)
        recGameImageNameLst =  gameDataAccess.getGameImageName([x['gameId'] for x in recGameLst])
        recGameLst = gameDataAccess.mergeRecGameLstAndImgInfo(recGameLst, recGameImageNameLst);
        selectionStr = ', '.join(info['selPlatformSet']) + ', ' + ', '.join(info['selGenreSet'])
        return render_template("recGameLst.html", recGameLst = recGameLst, selectionStr = selectionStr)
        #return str(recGameLst);
    else:
        abort(404, "Error")
