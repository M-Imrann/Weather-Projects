import os
import requests
import csv
import matplotlib.pyplot as plt
from arg_parser import parse_args


# -----------------------------------
# Fetch weather data from Open-Meteo
# -----------------------------------
def fetch_data(latitude, longitude):
    '''
    The function will fetch data from API and stores the data in JSON.

    Args:
    latitude: Latitude of the location
    longitude: Longitude of the location

    Return: Hourly weather data in Json
    '''
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&"\
          f"longitude={longitude}&hourly=temperature_2m,wind_speed_10m,"\
          f"soil_temperature_0cm"
    print(f"Requesting URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["hourly"]
    else:
        print("Failed to fetch data. Status code: ", response.status_code)
        return None


def extract_date(datetime_str):
    '''
    This function extract the date which help us to group the data by days.

    Args:
    datetime_str: Takes a string of date time like "2022-07-01T00:00"

    Return: It will return just date like "2022-07-01"
    '''
    return datetime_str.split("T")[0]


def group_by_date(data):
    '''
    This function will group the data by date.

    Args:
    data: Takes the data that we fetch.

    Return: Return the grouped data.
    '''
    grouped = {}
    for i in range(len(data["time"])):
        date = extract_date(data["time"][i])

        temp = data["temperature_2m"][i]

        wind = data["wind_speed_10m"][i]

        soil = data["soil_temperature_0cm"][i]

        if date not in grouped:
            grouped[date] = {"temp": [], "wind": [], "soil": []}

        grouped[date]["temp"].append(temp)
        grouped[date]["wind"].append(wind)
        grouped[date]["soil"].append(soil)

    return grouped


def calculate_stats(grouped_data):
    '''
    It will calculate the maximum, minimum and average temperature,
    wind speed and soil temperature.

    Args:
    grouped_data: Takes the data that is grouped by date.

    Return: Return the dictionary with maximum, minimum and
    average temperature, wind speed and soil temperature.

    '''
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "max_temp": max(values["temp"]),
            "min_temp": min(values["temp"]),
            "avg_temp": sum(values["temp"]) / len(values["temp"]),

            "max_wind": max(values["wind"]),
            "min_wind": min(values["wind"]),
            "avg_wind": sum(values["wind"]) / len(values["wind"]),

            "max_soil": max(values["soil"]),
            "min_soil": min(values["soil"]),
            "avg_soil": sum(values["soil"]) / len(values["soil"])
        }
    return stats


def write_to_csv(stats, filename="weather_data.csv"):
    '''
    It will export the data in CSV file.

    Args:
    Stats: The dictionary with maximum, minimum and
    average temperature, wind speed and soil temperature.

    filename: Name of the file where the data is storing.
    '''
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Date", "Max Temp", "Min Temp", "Avg Temp",
            "Max Wind", "Min Wind", "Avg Wind",
            "Max Soil", "Min Soil", "Avg Soil"
        ])
        for date, values in stats.items():
            writer.writerow([
                date,
                values["max_temp"], values["min_temp"], values["avg_temp"],
                values["max_wind"], values["min_wind"], values["avg_wind"],
                values["max_soil"], values["min_soil"], values["avg_soil"]
            ])
    print(f"CSV Exported: {filename}")


def extreme_dates(stats, key):
    '''
    Find the dates with maximum and minimum temperature,
    wind speed and soil temperature.

    Args:
    stats: The dictionary with maximum, minimum and
    average temperature, wind speed and soil temperature.

    key: Takes the value of which we want to find maximum and
    minimum values like, 'avg_temp', 'avg_wind'

    Return: Return the dates with maximum and minimum
    temperature, wind speed and soil temperature.
    '''
    max_date = max(stats, key=lambda d: stats[d][key])
    min_date = min(stats, key=lambda d: stats[d][key])
    return max_date, min_date


def plot_graph(stats, key, ylabel, title, filename):
    '''
    Plot the graphs of temperature, wind and soil

    Args:
    stats: The dictionary with maximum, minimum and
    average temperature, wind speed and soil temperature.

    key: Takes the value of which we want to plot the graph
    ylabel: Name of the label that we want on  y-axis
    title: Title of the graph
    filename: Name of the file
    '''
    dates = list(stats.keys())
    values = [stats[date][key] for date in dates]

    plt.figure(figsize=(10, 4))
    plt.plot(dates, values, marker='o')

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)

    plt.grid(True)

    os.makedirs("plots", exist_ok=True)
    plt.savefig(f"plots/{filename}")
    plt.close()


def main():
    args = parse_args()
    lat = args.lat
    lon = args.lon

    print("Fetching weather data...")
    raw_data = fetch_data(lat, lon)
    if not raw_data:
        return

    grouped_data = group_by_date(raw_data)
    stats = calculate_stats(grouped_data)
    write_to_csv(stats)

    temp_max, temp_min = extreme_dates(stats, "avg_temp")
    wind_max, wind_min = extreme_dates(stats, "avg_wind")
    soil_max, soil_min = extreme_dates(stats, "avg_soil")
    # Prints Maximum and Minimum Temperature
    print(f"Max Temp on: {temp_max}")
    print(f"Min Temp on: {temp_min}")
    # Prints Maximum and Minimum Wind Speed
    print(f"Max Wind on: {wind_max}")
    print(f"Min Wind on: {wind_min}")
    # Prints Maximum and Minimum Soil Temperature
    print(f"Max Soil Temp on: {soil_max}")
    print(f"Min Soil Temp on: {soil_min}")

    plot_graph(stats, "avg_temp", "Avg Temperature (°C)",
               "Average Temperature Over Time", "Temperature Graph")
    plot_graph(stats, "avg_wind", "Avg Wind Speed (km/h)",
               "Average Wind Speed Over Time", "Wind Graph")
    plot_graph(stats, "avg_soil", "Avg Soil Temperature (°C)",
               "Average Soil Temperature Over Time", "Soil Graph")


if __name__ == "__main__":
    main()
