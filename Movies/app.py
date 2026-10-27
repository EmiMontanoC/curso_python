from flask import Flask, render_template, request
import movies_sqlite as db
import os

app = Flask(__name__)



@app.route('/')
def index():
    db_path = os.path.join(os.path.dirname(__file__), 'databases\movies.db')
    conn = db.open_database(db_path)
    rows =db.retrieve_data_with_query(conn, "SELECT * FROM movies;")
    return render_template('Movies\index.html',rows=rows)

if __name__ == '__main__':
    app.run(debug=True)