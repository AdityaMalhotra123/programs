from flask import Flask, redirect, render_template, request, url_for
import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip('@')
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if len(tweets) > 100:
        tweets = helpers.get_user_timeline(screen_name, 100)

    if tweets == None:
        return redirect(url_for("index"))

    analyzer = Analyzer(positives, negatives)

    positive, negative, neutral = 0, 0, 0

    for tweet in tweets:
        score = analyzer.analyze(tweet)
        if score > 0.0:
            positive += score
        elif score < 0.0:
            negative += score
        else:
            neutral += score



    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
