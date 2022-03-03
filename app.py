from crypt import methods
from distutils.log import debug
from http.client import responses
from random import choice
from surveys import satisfaction_survey as survey
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

RESPONSE_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "unknown"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def survey_homepage():
    """Displays the Survey Homepage"""
    return render_template("survey_homepage.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_page():
    """Empty Session of Responses"""
    session[RESPONSE_KEY] = []
    return redirect("questions/0")

@app.route("/answer", methods=["POST"])
def answer_page():
    choice = request.form["answer"]
    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses
    if (len(responses) == len(survey.questions)):
        return redirect("/completed")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def questions_page(qid):
    responses = session.get(RESPONSE_KEY)
    if responses is None:
        return redirect("/")
    elif len(responses) == len(survey.questions):
        return redirect("/completed")
    elif len(responses) != qid:
        flash(f"Invalid Question ID: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    else:
        question = survey.questions[qid]
        return render_template("questions.html", question_num=qid, question=question)

@app.route("/completed")
def completed_page():
    return render_template("completed.html")