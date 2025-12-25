import requests
import math
from datetime import datetime

def calculate_dew_point(temp_f, humidity):
    temp_c = (temp_f - 32) * 5/9
    a, b = 17.625, 243.04
    alpha = math.log(humidity / 100.0) + (a * temp_c) / (b + temp_c)
    dp_c = (b * alpha) / (a - alpha)
    return round((dp_c * 9/5) + 32, 2)

def get_weather():
    # Vienna, VA Coordinates
    url = "https://api.open-meteo.com/v1/forecast?latitude=38.9012&longitude=-77.2653&current=temperature_2m,relative_humidity_2m&temperature_unit=fahrenheit&timezone=America/New_York"
    data = requests.get(url).json()
    temp = data['current']['temperature_2m']
    hum = data['current']['relative_humidity_2m']
    dp = calculate_dew_point(temp, hum)
    return temp, hum, dp

if __name__ == "__main__":
    t, h, d = get_weather()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | Temp: {t}°F | Hum: {h}% | Dew Point: {d}°F\n"
    
    with open("weather_log.md", "a") as f:
        f.write(log_entry)
    print(f"Logged: {log_entry}")
