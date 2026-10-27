from flask import Flask, render_template, request
import movies_sqlite as db
import os

app = Flask(__name__)



@app.route('/')
def index():
    db_path = os.path.join(os.path.dirname(__file__), 'databases\movies.db')
    conn = db.open_database(db_path)
    query = "SELECT * FROM movies ORDER BY release_date DESC;"
    rows =db.retrieve_data_with_query(conn, query)
    db.close_database(conn)
    return render_template('index.html',rows=rows)

if __name__ == '__main__':
    app.run(debug=True)