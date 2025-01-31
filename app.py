from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # すべてのオリジンを許可

@app.route("/data")
def get_data():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == "__main__":
    app.run(debug=True)