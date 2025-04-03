import time
import subprocess
import requests
import json

API_URL = "http://localhost:5000/openapi.json"

# Start FastAPI server if it's not running
try:
    response = requests.get(API_URL)
except requests.ConnectionError:
    print("FastAPI server not found. Starting the server...")
    subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"])
    time.sleep(3)  # Wait for the server to start

# Fetch API documentation
response = requests.get(API_URL)
if response.status_code == 200:
    api_data = response.json()
    
    with open("README.txt", "w") as f:
        f.write("API Endpoints:\n\n")
        
        for path, methods in api_data.get("paths", {}).items():
            f.write(f"Endpoint: {path}\n")
            for method, details in methods.items():
                f.write(f"  Method: {method.upper()}\n")
                if "parameters" in details: 
                    f.write("  Parameters:\n")
                    for param in details["parameters"]:
                        f.write(f"    - {param['name']} ({param['in']}): {param.get('description', 'No description')}\n")
                f.write("\n")
        
        f.write("\nFor full API documentation, visit: http://localhost:5000/docs\n")

    print("README.txt generated successfully!")
else:
    print("failed")