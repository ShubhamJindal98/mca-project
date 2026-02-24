from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

movies = pd.read_csv("movies.csv")

# Similarity
vectorizer = CountVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movies["keywords"])
similarity = cosine_similarity(vectors)

def get_similar_movies(title):
    index = movies[movies["title"] == title].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    return movies.iloc[[i[0] for i in distances]]

@app.route("/")
def home():
    movie_name = request.args.get("movie")

    selected_movie = None
    recommendations = None

    if movie_name:
        selected_movie = movies[movies["title"] == movie_name]
        if not selected_movie.empty:
            recommendations = get_similar_movies(movie_name)

    return render_template("index.html",
                           movies=movies["title"].values,
                           selected=selected_movie,
                           recommendations=recommendations,
                           current_movie=movie_name)

if __name__ == "__main__":
    app.run(debug=True)