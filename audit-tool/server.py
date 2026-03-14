from flask import Flask, render_template, request
from analyzer import analyze_website

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"].strip()
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

        # Colour class for score circle
        if score >= 80:
            score_class = "score-green"
        elif score >= 40:
            score_class = "score-amber"
        else:
            score_class = "score-red"

        return render_template(
            "result.html",
            report=report,
            score=score,
            score_class=score_class,
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
