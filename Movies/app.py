from flask import Flask, render_template, request
import movies_sqlite as db
import os

app = Flask(__name__)



@app.route('/')
def index():
    db_path = os.path.join(os.path.dirname(__file__), 'databases\movies.db')
    conn = db.open_database(db_path)
    query = "SELECT * FROM movies ORDER BY release_date DESC LIMIT 5;"
    rows =db.retrieve_data_with_query(conn, query)
    db.close_database(conn)
    return render_template('index.html',rows=rows)

@app.route('/movies')
def movies():
    db_path = os.path.join(os.path.dirname(__file__), 'databases\movies.db')
    conn = db.open_database(db_path)
    query = "SELECT * FROM movies ORDER BY release_date DESC;"
    rows =db.retrieve_data_with_query(conn, query)
    db.close_database(conn)
    return render_template('movies.html',rows=rows)

@app.route('/movie_detail/<int:movie_id>')
def movie_detail(movie_id):
    db_path = os.path.join(os.path.dirname(__file__), 'databases\movies.db')
    conn = db.open_database(db_path)
    # Query to get the movie details
    query = f"SELECT * FROM movies WHERE id = {movie_id};"
    rows = db.retrieve_data_with_query(conn, query)

    # Stars query to get the stars associated with the movie
    query_stars = f"SELECT stars.*, connections.role FROM stars,movies,connections WHERE connections.movie_id = {movie_id} AND connections.star_id = stars.id AND connections.movie_id = movies.id;"
    stars = db.retrieve_data_with_query(conn, query_stars)
    print(f"Retrieved rows: {stars}")  # Debugging line
    db.close_database(conn)
    return render_template('movie_detail.html', rows=rows, stars=stars)

if __name__ == '__main__':
    app.run(debug=True)