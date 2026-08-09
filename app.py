from flask import Flask, redirect, render_template, request, url_for
import requests
from tubescrape import YouTube, YouTubeError, RateLimitError, ProxyBlockedError


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
        podcasts = getPodcasts(topic)
        videos = getVideos(topic)

        return render_template("results.html", topic=topic, books=books, podcasts=podcasts, videos=videos)



def urlify(topic):
    urlTopic = topic.split()
    urlTopic = "+".join(urlTopic)
    return urlTopic



def getBooks(topic):
    urlTopic = urlify(topic)

    url = ''.join(["https://openlibrary.org/search.json?q=", urlTopic])

    response = requests.get(url)
    data = response.json()

    return data["docs"]



def getPodcasts(topic):
    urlTopic = urlify(topic)

    url = ''.join(["https://itunes.apple.com/search?term=", urlTopic, "&media=podcast"])

    response = requests.get(url)
    data = response.json()

    return data["results"]

def getVideos(topic):
    yt = YouTube()

    try:
        response = yt.search(query=topic, max_results=50, type="video")
    except RateLimitError:
        response = "Rate limited, use a proxy"
        return response
    except ProxyBlockedError:
        response = "Proxy blocked by firewall, use residential proxies"
        return response
    except YouTubeError as e:
        response = "YouTube error: {e}"
        return response
    
    return response.videos