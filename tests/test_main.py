import unittest
from unittest.mock import patch, MagicMock
import os
import matplotlib.pyplot as plt
import tempfile
import csv
from main import (
    extract_date, group_by_date, calculate_stats,
    write_to_csv, extreme_dates, plot_graph, fetch_data
)


MOCK_WEATHER_DATA = {
    "time": ["2024-01-01T00:00", "2024-01-01T01:00", "2024-01-02T00:00"],
    "temperature_2m": [10.0, 12.0, 5.0],
    "wind_speed_10m": [2.0, 3.0, 1.0],
    "soil_temperature_0cm": [6.0, 7.0, 3.0]
}


class TestMainFunctions(unittest.TestCase):
    def test_extract_date(self):
        '''
        Test case to test the extract date function.
        '''
        result = extract_date("2024-01-01T12:00")
        self.assertEqual(result, "2024-01-01")

    def test_group_by_date(self):
        '''
        Test case to test the group by date function.
        '''
        grouped = group_by_date(MOCK_WEATHER_DATA)
        self.assertIn("2024-01-01", grouped)
        self.assertEqual(len(grouped["2024-01-01"]["temp"]), 2)
        self.assertEqual(grouped["2024-01-02"]["soil"], [3.0])

    def test_calculate_stats(self):
        '''
        Test case to test the calculate stats function.
        '''
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = calculate_stats(grouped)
        self.assertAlmostEqual(stats["2024-01-01"]["avg_temp"], 11.0)
        self.assertEqual(stats["2024-01-02"]["max_soil"], 3.0)

    def test_extreme_dates(self):
        '''
        Test case to test the extreme dates function.
        '''
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = calculate_stats(grouped)
        max_date, min_date = extreme_dates(stats, "avg_temp")
        self.assertEqual(max_date, "2024-01-01")
        self.assertEqual(min_date, "2024-01-02")

    def test_write_to_csv(self):
        '''
        Test case to test the write_to_csv function
        '''
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = calculate_stats(grouped)
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, "test.csv")
            write_to_csv(stats, file_path)
            with open(file_path, newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 3)  # header + 2 rows
                self.assertEqual(rows[0][0], "Date")
                self.assertEqual(rows[1][0], "2024-01-01")

    @patch("matplotlib.pyplot.savefig")
    def test_plot_graph(self, mock_savefig):
        '''
        Test case to test the plot graph function.
        '''
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = calculate_stats(grouped)
        plot_graph(stats, "avg_temp", "Temperature", "Temp Plot",
                   "temp_plot.png")
        mock_savefig.assert_called_once()
        plt.close("all")

    @patch("requests.get")
    def test_fetch_data_success(self, mock_get):
        '''
        Test case to test the fetch data function that successfully fetch data.
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"hourly": MOCK_WEATHER_DATA}
        mock_get.return_value = mock_response
        result = fetch_data(10.0, 20.0)
        self.assertIsNotNone(result)
        self.assertEqual(result["temperature_2m"], [10.0, 12.0, 5.0])

    @patch("requests.get")
    def test_fetch_data_failure(self, mock_get):
        '''
        Test case to test the fetch data function that fails to fetch the data.
        '''
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = fetch_data(10.0, 20.0)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
