from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify

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
        print(info)
        return str(info);


    else:
        abort(404, "Error")
