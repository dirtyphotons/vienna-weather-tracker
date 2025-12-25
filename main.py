import requests
import json
import math
import os

# --- Calculation Logic ---
def calculate_dew_point(temp_f, humidity):
    temp_c = (temp_f - 32) * 5/9
    a, b = 17.625, 243.04
    alpha = math.log(humidity / 100.0) + (a * temp_c) / (b + temp_c)
    dp_c = (b * alpha) / (a - alpha)
    return round((dp_c * 9/5) + 32, 1)

# --- Update Gist Logic ---
def update_gist(dp_value):
    gist_id = "a7c9e2448514b41a06d383f9befac8af"
    token = os.getenv("GIST_TOKEN") # We will set this in GitHub Secrets
    
    color = "orange" if dp_value > 65 else "blue"
    
    payload = {
        "files": {
            "weather.json": {
                "content": json.dumps({
                    "schemaVersion": 1,
                    "label": "Vienna Dew Point",
                    "message": f"{dp_value}°F",
                    "color": color
                })
            }
        }
    }
    
    requests.patch(f"https://api.github.com/gists/{gist_id}", 
                   headers={"Authorization": f"token {token}"}, 
                   data=json.dumps(payload))

if __name__ == "__main__":
    # Fetch Vienna weather
    url = "https://api.open-meteo.com/v1/forecast?latitude=38.9012&longitude=-77.2653&current=temperature_2m,relative_humidity_2m&temperature_unit=fahrenheit"
    data = requests.get(url).json()
    
    temp = data['current']['temperature_2m']
    hum = data['current']['relative_humidity_2m']
    dp = calculate_dew_point(temp, hum)
    
    # Update the badge
    update_gist(dp)
    print(f"Badge updated to {dp}°F")

