import requests
from datetime import date, timedelta

NASA_API_KEY = "DEMO_KEY"

def get_nasa_asteroids():

    today = date.today()
    end_date = today + timedelta(days=7)

    url = "https://api.nasa.gov/neo/rest/v1/feed"

    params = {
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "api_key": NASA_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    asteroid_list = []

    for date_key, asteroids in data["near_earth_objects"].items():

        for asteroid in asteroids:

            approach = asteroid["close_approach_data"][0]

            asteroid_list.append({
                "Name": asteroid["name"],
                "NASA ID": asteroid["id"],
                "Hazardous": asteroid["is_potentially_hazardous_asteroid"],
                "Absolute Magnitude": asteroid["absolute_magnitude_h"],
                "Diameter Min (km)": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                "Diameter Max (km)": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "Velocity (km/s)": float(
                    approach["relative_velocity"]["kilometers_per_second"]
                ),
                "Miss Distance (km)": float(
                    approach["miss_distance"]["kilometers"]
                ),
                "Close Approach Date": approach["close_approach_date"]
            })

    return pd.DataFrame(asteroid_list)