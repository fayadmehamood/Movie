from flask import Flask, render_template, request, jsonify
import requests
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.genai import Client, types 
import os
import time

app = Flask(__name__)

# Kept exactly as provided
OMDB_API_KEY = "7194dc3b"
YOUTUBE_API_KEY = "AIzaSyDGxEw7cIHXZ8VPw1uN2jM40jcGqvi1Opc"
GEMINI_API_KEY = "AIzaSyAHtmsJklA4xlMvozQiIGiUVGkHsKMNZrM"

movie_cache = {}

def make_gemini_api_call(model, contents, config, max_retries=3):
    for attempt in range(max_retries):
        try:    
            response = gemini_client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise e

# Gemini Init
gemini_client = None
try:
    if GEMINI_API_KEY:
        gemini_client = Client(api_key=GEMINI_API_KEY)
        print("Gemini API configured successfully.")
except Exception as e:
    print(f"Gemini Init Error: {e}")

# YouTube Init
youtube = None
try:
    if YOUTUBE_API_KEY:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        print("YouTube API initialized successfully.")
except Exception as e:
    print(f"YouTube Init Error: {e}")

GENRES = ["Action", "Comedy", "Drama", "Horror", "Romance", 
          "Sci-Fi", "Thriller", "Animation", "Documentary"]

def get_movie_details_from_omdb(key):
    if key in movie_cache:
        return movie_cache[key]
    if not OMDB_API_KEY:
        return None
    try:
        is_imdb = key.startswith("tt")
        query = f"i={key}" if is_imdb else f"t={key}"
        res = requests.get(
            f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&{query}&plot=full"
        ).json()
        if res.get("Response") == "True":
            data = {
                "title": res.get("Title"),
                "year": res.get("Year"),
                "poster": res.get("Poster") if res.get("Poster") != "N/A" else "https://placehold.co/300x450",
                "rating": res.get("imdbRating"),
                "imdbID": res.get("imdbID"),
                "plot": res.get("Plot"),
                "cast": res.get("Actors")
            }
            movie_cache[key] = data
            return data
    except:
        return None
    return None

def get_movies(filter_type="popularity", genre=None):
    movies = []
    if filter_type == "popularity":
        titles = ["Inception", "The Dark Knight", "Pulp Fiction", "Interstellar"]
        for t in titles:
            d = get_movie_details_from_omdb(t)
            if d: movies.append(d)
    elif filter_type == "genre" and genre:
        res = requests.get(
            f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={genre}&type=movie"
        ).json()
        if res.get("Search"):
            for item in res["Search"][:10]:
                d = get_movie_details_from_omdb(item["imdbID"])
                if d: movies.append(d)
    return movies

def get_trailer_video_id(title, year=None):
    if not youtube:
        return None
    try:
        query = f"{title} {year} official trailer"
        res = youtube.search().list(
            q=query, part="id", type="video", maxResults=1
        ).execute()
        return res["items"][0]["id"]["videoId"] if res["items"] else None
    except:
        return None

def handle_omdb_search(q):
    movies = []
    res = requests.get(
        f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={q}&type=movie"
    ).json()
    if res.get("Search"):
        for item in res["Search"][:10]:
            d = get_movie_details_from_omdb(item["imdbID"])
            if d: movies.append(d)
    return movies

@app.route("/", methods=["GET", "POST"])
def index():
    movies = []
    selected_filter = "popularity"
    selected_genre = None
    search_query = None
    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        selected_filter = request.form.get("filter")
        selected_genre = request.form.get("genre")
        if search_query:
            movies = handle_omdb_search(search_query)
        elif selected_filter == "genre":
            movies = get_movies("genre", selected_genre)
        else:
            movies = get_movies("popularity")
    else:
        movies = get_movies("popularity")
    return render_template("index.html",
        genres=GENRES,
        movies=movies,
        selected_filter=selected_filter,
        selected_genre=selected_genre,
        search_query=search_query
    )

@app.route("/get_details/<imdb_id>")
def get_details(imdb_id):
    details = get_movie_details_from_omdb(imdb_id)
    if details:
        trailer = get_trailer_video_id(details["title"], details["year"])
        return jsonify({**details, "trailer_id": trailer})
    return jsonify({"error": "Not found"}), 404

@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.json.get("query")
    if not gemini_client:
        return jsonify({"error": "Gemini not initialized"}), 500

    # Switched to gemini-1.5-flash and removed tools for better quota management
    config = types.GenerateContentConfig(
        response_mime_type="application/json"
    )

    prompt = f"Recommend 3-5 real movies for: {user_input} in JSON format."

    try:
        res = make_gemini_api_call(
            model="gemini-1.5-flash", 
            contents=[prompt],
            config=config
        )
        data = json.loads(res.text)
        return jsonify({"recommendations": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)