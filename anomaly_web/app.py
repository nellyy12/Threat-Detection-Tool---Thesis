# app.py

from flask import Flask, render_template
from utils.detection import get_anomaly_results

app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>Visit <a href='/dashboard'>/dashboard</a> to view anomaly detection results.</h2>"

@app.route("/dashboard")
def dashboard():
    try:
        logs = get_anomaly_results()
    except Exception as e:
        logs = []
        print("Error loading results:", e)

    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
