from flask import Flask, redirect, render_template, request, url_for
import requests
from tubescrape import YouTube, YouTubeError, RateLimitError, ProxyBlockedError
import feedparser
import re

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

TEACHING_IDEA_FEEDS = {
    "Cult of Pedagogy": "https://www.cultofpedagogy.com/feed/",
    "MiddleWeb": "https://www.middleweb.com/feed/",
    "TeachThought": "https://www.teachthought.com/feed/",
    "WeAreTeachers": "https://www.weareteachers.com/feed/",
}

# How many matching posts to keep per source, and how many seconds to wait
# on a single feed before giving up on it. Acts as a good failsafe! 
# Note that this idea came from the assistance of AI.
MAX_IDEAS_PER_SOURCE = 10
FEED_TIMEOUT_SECONDS = 8


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
        books = getBooks(topic)
        podcasts = getPodcasts(topic)
        videos = getVideos(topic)
        researchPapers = getResearchPapers(topic)
        wikiArticles = getWikiArticles(topic)
        teachingIdeas = getTeachingIdeas(topic)

        return render_template(
            "results.html",
            topic=topic,
            books=books,
            podcasts=podcasts,
            videos=videos,
            researchPapers=researchPapers,
            wikiArticles=wikiArticles,
            teachingIdeas=teachingIdeas
        )



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



def getResearchPapers(topic):
    urlTopic = urlify(topic)

    url = f"http://export.arxiv.org/api/query?search_query=all:{urlTopic}&start=0&max_results=50"
    feed = feedparser.parse(url)

    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "link": entry.id,
            "summary": entry.summary,
            "authors": [author.name for author in entry.authors],
            "published": entry.published
        })
    return papers



import requests

def getWikiArticles(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "namespace": 0,
        "search": topic,
        "limit": 25,
        "format": "json",
        "warningsaserror": True
    }

    headers = {
        "User-Agent": "TheFellow (https://github.com/StealthBanana/The-Fellow)"
    }

    response = requests.get(url=url, params=params, headers=headers)
    data = response.json()

    if "error" in data:
        return [{"title": f"API error: {data['error']['info']}", "link": "#"}]

    # Zips titles and links together using zip. 
    # Remember, zip returns tuples that you can use! 
    articles = [{"title": t, "link": l} for t, l in zip(data[1], data[3])]
    return articles



def stripHtml(rawHtml):
    text = re.sub(r"<[^>]+>", " ", rawHtml)
    text = re.sub(r"\s+", " ", text).strip()
    return text



def getTeachingIdeas(topic, maxPerSource=MAX_IDEAS_PER_SOURCE):
    topicWords = [word.lower() for word in topic.split() if len(word) > 2]

    ideasBySource = {}

    headers = {
        "User-Agent": "TheFellow (https://github.com/StealthBanana/The-Fellow)"
    }

    for sourceName, feedUrl in TEACHING_IDEA_FEEDS.items():
        try:
            response = requests.get(feedUrl, headers=headers, timeout=FEED_TIMEOUT_SECONDS)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            ideasBySource[sourceName] = {"error": f"{sourceName} took too long to respond. Try again later."}
            continue
        except requests.exceptions.RequestException as e:
            ideasBySource[sourceName] = {"error": f"Could not reach {sourceName} right now ({e})."}
            continue

        feed = feedparser.parse(response.content)

        if feed.bozo and not feed.entries:
            ideasBySource[sourceName] = {"error": f"{sourceName}'s feed could not be read right now."}
            continue

        matches = []
        for entry in feed.entries:
            title = entry.get("title", "")
            summaryRaw = entry.get("summary", "")
            summary = stripHtml(summaryRaw)

            haystack = f"{title} {summary}".lower()

            if any(word in haystack for word in topicWords):
                matches.append({
                    "title": title,
                    "link": entry.get("link", "#"),
                    "summary": (summary[:300] + "...") if len(summary) > 300 else summary,
                    "published": entry.get("published", "")
                })

            if len(matches) >= maxPerSource:
                break

        ideasBySource[sourceName] = {"entries": matches}

    return ideasBySource