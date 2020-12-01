import sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/data')
def extract_data():
    column = request.args.get('measure')
    q = f"SELECT date,{column} FROM room WHERE room.date BETWEEN ? AND ?"
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    with sqlite3.connect('room') as con:
        c = con.cursor()
        c.execute(q, (start_date, end_date))
        data = c.fetchall()
    result = {}
    result['date'] = [x[0] for x in data]
    result[column] = [x[1] for x in data]
    return jsonify(result), 200


if __name__ == '__main__':
    app.run()
