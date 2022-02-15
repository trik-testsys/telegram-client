from flask import Flask, request

app = Flask(__name__)


@app.route('/user')
def echo():
    text = request.args.get('text')
    return text


if __name__ == "__main__":
    app.run(debug=True)
