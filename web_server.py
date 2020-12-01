from flask import Flask, render_template

app = Flask(__name__,
            static_folder='../room_frontend/dist/static',
            template_folder='../room_frontend/dist')


@app.route('/')
@app.route('/index')
def show_index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
