import os
import requests
import csv
import matplotlib.pyplot as plt
from arg_parser import parse_args


# -----------------------------------
# Fetch weather data from Open-Meteo
# -----------------------------------
def fetch_data(latitude, longitude, start, end):
    '''
    The function will fetch data from API and stores the data in JSON.

    Args:
    latitude: Latitude of the location
    longitude: Longitude of the location

    Return: Hourly weather data in Json
    '''
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"start_date={start}&end_date={end}&"
        f"hourly=temperature_2m,wind_speed_10m,soil_temperature_0cm"
    )
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


def max_temperature(grouped_data):
    """
    It will find the Maximum Temperature.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of maximum temperature
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "max_temp": max(values["temp"])
        }
    return stats


def min_temperature(grouped_data):
    """
    It will find the Minimum Temperature.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of minimum temperature
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "min_temp": min(values["temp"])
        }
    return stats


def avg_temperature(grouped_data):
    """
    It will find the Average Temperature.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of average temperature
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "avg_temp": sum(values["temp"]) / len(values["temp"])
        }
    return stats


def max_wind(grouped_data):
    """
    It will find the Maximum Wind Speed.

    Args:
    grouped_data: Takes the grouped data according to date.

    Return: Return dictionary of maximum wind speed.
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "max_wind": max(values["wind"])
        }
    return stats


def min_wind(grouped_data):
    """
    It will find the Minimum Wind Speed.

    Args:
    grouped_data: Takes the grouped data according to date.

    Return: Return dictionary of minimum wind speed.
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "min_wind": min(values["wind"])
        }
    return stats


def avg_wind(grouped_data):
    """
    It will find the Average Wind Speed.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of average wind speed.
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "avg_wind": sum(values["wind"]) / len(values["wind"])
        }
    return stats


def max_soil_temperature(grouped_data):
    """
    It will find the Maximum Soil Temperature.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of maximum soil temperature
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "max_soil": max(values["soil"])
        }
    return stats


def min_soil_temperature(grouped_data):
    """
    It will find the Minimum Soil Temperature.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of minimum soil temperature
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "min_soil": min(values["soil"])
        }
    return stats


def avg_soil_temperature(grouped_data):
    """
    It will find the Average Soil Temperature.

    Args:
    grouped_data: Takes the grouped data according to date

    Return: Return dictionary of average soil temperature
    """
    stats = {}
    for date, values in grouped_data.items():
        stats[date] = {
            "avg_soil": sum(values["soil"]) / len(values["soil"])
        }
    return stats


def write_to_csv(stats, filename, key):
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
            "Date", key
        ])
        for date, values in stats.items():
            writer.writerow([
                date,
                values[key]
            ])
    print(f"CSV Exported: {filename}")
    plot_graph(stats, key, (key+".png")),


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
    print(f"Maximum {key} on :", max_date)
    print(f"Maximum {key} on :", min_date)


def plot_graph(stats, key, filename):
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

    plt.title(key)
    plt.xlabel("Date")
    plt.ylabel(key)
    plt.xticks(rotation=45)

    plt.grid(True)

    os.makedirs("plots", exist_ok=True)
    plt.savefig(f"plots/{filename}")
    plt.close()


action_map = {
    "max_temp": lambda g: write_to_csv(max_temperature(g), "max_temp.csv",
                                       "max_temp"),
    "min_temp": lambda g: write_to_csv(min_temperature(g), "min_temp.csv",
                                       "min_temp"),
    "avg_temp": lambda g: write_to_csv(avg_temperature(g), "avg_temp.csv",
                                       "avg_temp"),

    "max_wind": lambda g: write_to_csv(max_wind(g), "max_wind.csv",
                                       "max_wind"),
    "min_wind": lambda g: write_to_csv(min_wind(g), "min_wind.csv",
                                       "min_wind"),
    "avg_wind": lambda g: write_to_csv(avg_wind(g), "avg_wind.csv",
                                       "avg_wind"),

    "max_soil": lambda g: write_to_csv(max_soil_temperature(g), "max_soil.csv",
                                       "max_soil"),
    "min_soil": lambda g: write_to_csv(min_soil_temperature(g), "min_soil.csv",
                                       "min_soil"),
    "avg_soil": lambda g: write_to_csv(avg_soil_temperature(g), "avg_soil.csv",
                                       "avg_soil"),

    "extreme_temp_date": lambda g: extreme_dates(avg_temperature(g),
                                                 "avg_temp"),
    "extreme_wind_date": lambda g: extreme_dates(avg_wind(g), "avg_wind"),
    "extreme_soil_date": lambda g: extreme_dates(avg_soil_temperature(g),
                                                 "avg_soil"),
}


def main():
    args = parse_args()
    lat = args.lat
    lon = args.lon
    start = args.start_date
    end = args.end_date
    action = args.action

    print("Fetching weather data...")
    raw_data = fetch_data(lat, lon, start, end)
    if not raw_data:
        return

    grouped_data = group_by_date(raw_data)

    if action in action_map:
        action_map[action](grouped_data)
    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    main()
