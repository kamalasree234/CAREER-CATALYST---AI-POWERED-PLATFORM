from flask import Flask, render_template, request
import http.client
import json
import urllib.parse

app = Flask(__name__)

# Function to fetch jobs from API
def get_jobs(query):
    conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
    encoded_query = urllib.parse.quote(query) 
    headers = {
       
    }
    conn.request("GET", f"/search?query={encoded_query}&country=in", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jobs = json.loads(data.decode("utf-8"))
    
    return jobs.get("data", [])

@app.route("/", methods=["GET", "POST"])
def home():
    jobs = []
    if request.method == "POST":
        search_query = request.form["search"]
        jobs = get_jobs(search_query)
    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
     app.run( port=5001, debug=True)
