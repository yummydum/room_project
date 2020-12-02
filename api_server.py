import logging
import sqlite3
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
date_format = '%Y-%m-%d'


@app.route('/data')
def extract_data():
    column = request.args.get('measure')
    q = f"SELECT date,{column} FROM room WHERE room.date BETWEEN ? AND ?"
    start_date = datetime.strptime(request.args.get('start_date'), date_format)
    end_date = datetime.strptime(request.args.get('end_date'), date_format)
    with sqlite3.connect('room') as con:
        con.set_trace_callback(logging.info)
        c = con.cursor()
        c.execute(q, (start_date, end_date))
        data = c.fetchall()
    result = {}
    result['date'] = [x[0] for x in data]
    result[column] = [x[1] for x in data]
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
