# Imports
import sqlite3
import logging
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__,template_folder="./templates")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reports", methods=["GET","POST"])
def reports():
     if request.method == "POST":
          period = request.form.get('month-year')
          if not period:
               # Handle the case where 'month-year' is not provided
               return render_template("reports.html", error="Please provide a period.")
          else:
               report = get_report(period=period)
               app.logger.info(f"Report result: {report}")
               if not report:
                    return render_template("reports.html", error="No data available for the selected period.")
          return render_template("reports.html", report=report)
     else:
          return render_template("reports.html")

def get_report(period):
     # Connect to the SQLite database
     conn = sqlite3.connect('chargehistory.db')
     cursor = conn.cursor()

     # Convert the period to the format "YYYY-MM"
     period_date = datetime.strptime(period, "%Y-%m")

     start_timestamp = int(period_date.timestamp())
     end_timestamp = int((period_date.replace(day=28) + timedelta(days=4)).replace(day=1).timestamp())


     # Query to fetch the report data for the given period    
     query = """
     SELECT * FROM sessions
     WHERE startdatetime >= ? AND startdatetime < ?
     """
     cursor.execute(query, (start_timestamp, end_timestamp))

     # Fetch all rows and convert to dictionary
     rows = cursor.fetchall()
     report_data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in rows]

     # Close the connection
     conn.close()

     return report_data


if __name__ == "__main__":
    app.run(debug=True)