import os
import webbrowser
import time

# Start Flask API
flask_app_path = r"D:\career catalyst\flask app1"
os.system(f'start cmd /k "cd /d \"{flask_app_path}\" && python app.py --port=5000"')

# Wait for Flask to start
time.sleep(3)  

# Open HTML file

webbrowser.open("http://127.0.0.1:5000")
time.sleep(4)
webbrowser.open(r"D:\career catalyst\index.html")
