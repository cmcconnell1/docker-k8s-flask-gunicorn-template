from flask import Flask, jsonify

app = Flask(__name__)
# pull in the config (i.e. vars from `services/web/project/config.py` on init)

# define your app/service routes here
@app.route("/")
def hello_world():
    return jsonify(hello="world")

# Liveliness check--should at least have '/alive' and 'readiness' dummy routes in your apps:
@app.route("/alive")
def alive():
    return 'OK'

# Mock readiness check
@app.route("/ready")
def ready():
    return jsonify(
        backend='ready',
        db='ready',
        queue='ready'
    )

if __name__ == "__main__":
  # Only for debugging while developing
  app.run(debug=True, port=5000)
