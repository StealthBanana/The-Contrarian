from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":

#TODO:  Write Python code to take a claim string, search for it via DuckDuckGo/Google Books/Podcast Index/YouTube, 
        # fetch results, and collect titles and links. Print out a rough list of findings
        
        belief = request.form.get("belief")

        if not belief:
            return redirect("/")
# TODO: Redirect to different html page that has the results.
        return redirect("/") 

    else:
        return render_template("index.html")


