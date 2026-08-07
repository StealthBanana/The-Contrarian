from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def belief():
    if request.method == "POST":

        #TODO:  Write Python code to take a claim string, search for it via DuckDuckGo/Google Books/Podcast Index/YouTube, 
            # fetch results, and collect titles and links. Print out a rough list of findings
        
        belief = request.form.get("belief")

        if not belief:
            return redirect("/")

        return redirect("/results") 

    else:           
        return render_template("index.html")

@app.route("/results")
def results():

        #TODO Print to the books section of the results page.
        
        url = "https://openlibrary.org/search.json?q=climate+change"

        response = requests.get(url)     
        response.json()

        return render_template("results.html")