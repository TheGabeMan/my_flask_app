# Imports
from flask import Flask, render_template, request, redirect


app = Flask(__name__,template_folder="./templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reports", methods=["GET","POST"])
def reports():
     if request.method == "POST":
          period = request.form.get('month-year')
          return render_template("reports.html", period=period)
     else:
          return render_template("reports.html")

if __name__ in "__main__":
    app.run(debug=True)