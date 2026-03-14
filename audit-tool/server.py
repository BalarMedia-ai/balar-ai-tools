from flask import Flask, render_template, request
from analyzer import analyze_website

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        report = analyze_website(url)
        score = 0
        if report["title"]:
            score += 20
        if report["meta_description"]:
            score += 20
        if report["h1"]:
            score += 20
        if report["images_missing_alt"] < 5:
            score += 20
        if report["word_count"] > 500:
            score += 20
        return render_template("result.html", report=report, score=score)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
