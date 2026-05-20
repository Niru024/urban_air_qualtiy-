import requests  # type: ignore
import pandas as pd  # type: ignore
import os
import time

API_KEY = "5ZfX1dRFclMZNP5g690ZebSTjmRBFd0OemGscq9p"

def get_air_quality(city):

    url = f"https://api.api-ninjas.com/v1/airquality?city={city}"

    headers = {
        "X-Api-Key": API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("❌ API Error:", response.status_code, response.text)
        return None


def save_data(city):

    data = get_air_quality(city)

    if not data:
        return

    row = {
        "PM2.5": data.get("PM2.5", {}).get("concentration", 0),
        "PM10": data.get("PM10", {}).get("concentration", 0),
        "NO2": data.get("NO2", {}).get("concentration", 0),
        "SO2": data.get("SO2", {}).get("concentration", 0),
        "CO": data.get("CO", {}).get("concentration", 0),
        "O3": data.get("O3", {}).get("concentration", 0),
        "AQI": data.get("overall_aqi", 0)
    }

    df = pd.DataFrame([row])

    file = os.path.join(os.path.dirname(__file__), "aqi_dataset.csv")

    if os.path.exists(file):
        df.to_csv(file, mode='a', header=False, index=False)
    else:
        df.to_csv(file, index=False)

    print("✅ Data saved")


if __name__ == "__main__":
    save_data("pune")