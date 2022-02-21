from flask import jsonify

from api.loader import app
import controller

if __name__ == "__main__":
    app.run(debug=True)
