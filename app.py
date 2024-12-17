# Imports
from flask import Flask, render_template
app = Flask(__name__,template_folder="./templates")





@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reports")
def reports():
     return render_template("reports.html")

@app.route("/settings")
def settings():
     return render_template("settings.html")

if __name__ in "__main__":
    app.run(debug=True)