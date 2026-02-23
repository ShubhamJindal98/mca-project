from flask import Flask, render_template, request
import pandas as pd

# Create Flask app FIRST
app = Flask(__name__)

# Load dataset
movies = pd.read_csv("movies.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    recommended = None
    searched_movie = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "recommend":
            genre = request.form.get("genre")
            if genre:
                recommended = movies[
                    movies["genre"].str.lower() == genre.lower()
                ].sort_values(by="rating", ascending=False)

        elif action == "search":
            search = request.form.get("search")
            if search:
                searched_movie = movies[
                    movies["title"].str.lower() == search.lower()
                ]

    return render_template("index.html",
                           movies=recommended,
                           searched=searched_movie)


if __name__ == "__main__":
    app.run(debug=True)