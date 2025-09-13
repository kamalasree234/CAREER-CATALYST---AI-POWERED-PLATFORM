import os
import re
import subprocess
import threading
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
matplotlib.use('Agg') 

from turtle import pd
import requests
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory 
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, firestore




import google.generativeai as genai

app = Flask(__name__)
CORS(app)




generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_roadmap', methods=['POST'])
def get_roadmap():
    data = request.get_json()
    career_role = data.get('career')

    if not career_role:
        return jsonify({"error": "Career role is required"}), 400

    chat_session = model.start_chat(history=[])
    
    query = f"""Provide a complete career roadmap for {career_role}. 
Include the following details:
don't include * in the answers you give for my below questions.it must not look like ai generated.
generate career-related icons but don't mention the word icon anywhere ok.for all the below questions must be related with india.add an image which depicts the career
1. Qualifications: What degrees, certifications, or educational background are needed?
2. Skills: Essential technical and soft skills required for success.
3. Best Online Courses & Resources: List top free and paid courses, books, and learning platforms.
4. YouTube Channels: Suggest the best YouTube channels for learning and staying updated.mostly indian channels you can include others also.
5. Job Opportunities: What job roles are available, and what is the salary range for freshers and experienced professionals in india?
6. Latest Trends & Advancements: What are the new technologies or skills in demand for this field?
7. Inspiring message:End with an inspiring message to keep learners motivated in this career path.
8.Provide them a plan for each week to achieve their goal.
Make the response detailed, informative, and inspiring.
"""

    response = chat_session.send_message(query)

    clean1_response = re.sub(r"[^a-zA-Z0-9\s]", "", response.text)  
    roadmap_text = clean1_response if response and response.text else "No data received."

    return jsonify({"roadmap": roadmap_text})
@app.route('/compare_careers', methods=['POST'])
def compare_careers():
    data = request.get_json()
    career1 = data.get('career1')
    career2 = data.get('career2')

    if not career1 or not career2:
        return jsonify({"error": "Both career roles are required"}), 400

    chat_session = model.start_chat(history=[])
    
    query = f"""Compare the career paths of {career1} and {career2}. 
Highlight the differences in:
1. Educational qualifications required
2. Key skills needed
3. Job roles and salary range
4. Industry demand and future scope
5. Work-life balance and career growth
Provide a structured and easy-to-understand comparison."""
    
    response = chat_session.send_message(query)
    clean2_response = re.sub(r"[^a-zA-Z0-9\s]", "", response.text)  
    comparison_text = clean2_response if response and response.text else "No data received."

    return jsonify({"comparison": comparison_text})

@app.route('/career_data.json')
def get_json():
    return send_from_directory('static', 'career_data.json')

@app.route('/start_server', methods=['GET'])
def start_server():
    flask_url = "http://127.0.0.1:5000/"

    # ✅ Check if Flask is already running
    try:
        response = requests.get(flask_url)
        if response.status_code == 200:
            return jsonify({"message": "Flask App is already running!"})
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Flask App is not running! Start it manually."}), 500
    

@app.route('/search', methods=['POST'])
def store_search():
    data = request.json
    career = data.get("career")
    user_id = data.get("user_id")  # Received from frontend

    if not user_id or not career:
        return jsonify({"error": "Invalid data"}), 400

    db.collection('users').document(user_id).collection('history').add({"career": career})
    return jsonify({"message": "Search saved successfully!"}), 200

# Retrieve search history
@app.route('/history', methods=['GET'])
def get_history():
    data = request.json
    user_id = data.get("user_id")  # Received from frontend

    if not user_id:
        return jsonify({"error": "User not logged in"}), 400

    searches_ref = db.collection('users').document(user_id).collection('history')
    searches = searches_ref.stream()

    history = [{"career": search.to_dict()["career"]} for search in searches]
    return jsonify({"history": history}), 200
if __name__ == '__main__':
    app.run(debug=True,port=5000)

