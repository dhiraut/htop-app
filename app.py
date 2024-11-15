from flask import Flask
import os
import psutil
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask App. Go to /htop to see system information."

@app.route('/htop')
def htop():
    name = "Dhiraj Kumar Raut" 
    username = os.getenv("USER") or os.getenv("USERNAME")  
    server_time = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')  
    top_output = get_top_output()  

    return f"""
    <html>
    <body>
        <h1>System Information</h1>
        <p>Name: {name}</p>
        <p>Username: {username}</p>
        <p>Server Time (IST): {server_time}</p>
        <h2>Top Output</h2>
        <pre>{top_output}</pre>
    </body>
    </html>
    """

def get_top_output():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        try:
            processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU: {proc.info['cpu_percent']}%, Memory: {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  
    return "\n".join(processes[:10]) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
