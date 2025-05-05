from flask import Flask, render_template, request
from crawler import fetch_credit_info

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        password = request.form.get("password")

        success, result = fetch_credit_info(student_id, password)
        if success:
            return render_template("result.html", student_id=student_id, credits=result)
        else:
            return render_template("index.html", error=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
