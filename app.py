from flask import Flask, redirect, render_template, request, url_for
import requests

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def input():
    if request.method == "POST":
        
        topic = request.form.get("inputTopic")
        topic = topic.title()

        if not topic:
            return redirect("/")

        return redirect(url_for(('results'), topic=topic))

    else:           
        return render_template("index.html")

@app.route("/results/<topic>")
def results(topic):
        #TODO: Get all info from all sites, change to correct format
        # and then pass info to results.html.
        books = getBooks(topic)

        return render_template("results.html", topic=topic, books=books)


def getBooks(topic):
    url = "https://openlibrary.org/search.json?q=the+lord+of+the+rings"

    response = requests.get(url)
    data = response.json()

    return data