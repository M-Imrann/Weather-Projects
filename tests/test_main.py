import unittest
from unittest.mock import patch, mock_open
from main import (
    fetch_data, extract_date, group_by_date, max_temperature,
    min_temperature, avg_temperature, max_wind, min_wind,
    avg_wind, max_soil_temperature, min_soil_temperature,
    avg_soil_temperature, write_to_csv, extreme_dates,
    plot_graph, main
    )


MOCK_WEATHER_DATA = {
    "time": ["2024-07-01T00:00", "2024-07-01T01:00"],
    "temperature_2m": [10, 20],
    "wind_speed_10m": [5, 10],
    "soil_temperature_0cm": [15, 25]
}


class TestMainFunctions(unittest.TestCase):

    def test_extract_date(self):
        """
        Test case to test the extract date function.
        """
        self.assertEqual(extract_date("2024-07-01T00:00"), "2024-07-01")

    def test_group_by_date(self):
        """
        Test case to test the group by date function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        self.assertIn("2024-07-01", grouped)
        self.assertEqual(len(grouped["2024-07-01"]["temp"]), 2)

    def test_max_temperature(self):
        """
        Test case to test the max temperature function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = max_temperature(grouped)
        self.assertEqual(result["2024-07-01"]["max_temp"], 20)

    def test_min_temperature(self):
        """
        Test case to test the min temperature function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = min_temperature(grouped)
        self.assertEqual(result["2024-07-01"]["min_temp"], 10)

    def test_avg_temperature(self):
        """
        Test case to test the avg temperature function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = avg_temperature(grouped)
        self.assertEqual(result["2024-07-01"]["avg_temp"], 15)

    def test_max_wind(self):
        """
        Test case to test the max wind function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = max_wind(grouped)
        self.assertEqual(result["2024-07-01"]["max_wind"], 10)

    def test_min_wind(self):
        """
        Test case to test the min wind function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = min_wind(grouped)
        self.assertEqual(result["2024-07-01"]["min_wind"], 5)

    def test_avg_wind(self):
        """
        Test case to test the avg wind function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = avg_wind(grouped)
        self.assertEqual(result["2024-07-01"]["avg_wind"], 7.5)

    def test_max_soil_temperature(self):
        """
        Test case to test the max soil temperature function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = max_soil_temperature(grouped)
        self.assertEqual(result["2024-07-01"]["max_soil"], 25)

    def test_min_soil_temperature(self):
        """
        Test case to test the min soil temperature function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = min_soil_temperature(grouped)
        self.assertEqual(result["2024-07-01"]["min_soil"], 15)

    def test_avg_soil_temperature(self):
        """
        Test case to test the avg soil temperature function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        result = avg_soil_temperature(grouped)
        self.assertEqual(result["2024-07-01"]["avg_soil"], 20)

    @patch("builtins.open", new_callable=mock_open)
    @patch("main.plot_graph")
    def test_write_to_csv(self, mock_plot, mock_file):
        """
        Test case to test the write to csv function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = avg_temperature(grouped)
        write_to_csv(stats, "avg_temp.csv", "avg_temp")
        mock_file.assert_called_once_with("avg_temp.csv", "w", newline="")
        mock_plot.assert_called_once()

    @patch("builtins.print")
    def test_extreme_dates(self, mock_print):
        """
        Test case to test the extreme dates function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = avg_temperature(grouped)
        extreme_dates(stats, "avg_temp")
        self.assertTrue(mock_print.called)

    @patch("main.plt.savefig")
    def test_plot_graph(self, mock_save):
        """
        Test case to test the plot graph function.
        """
        grouped = group_by_date(MOCK_WEATHER_DATA)
        stats = avg_temperature(grouped)
        plot_graph(stats, "avg_temp", "avg_temp.png")
        mock_save.assert_called_once()

    @patch("main.requests.get")
    def test_fetch_data_success(self, mock_get):
        """
        Test case to test the fetch data function with succeessfully
        fetching the data.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"hourly": MOCK_WEATHER_DATA}
        result = fetch_data(0, 0, "2024-07-01", "2024-07-03")
        self.assertEqual(result["temperature_2m"], [10, 20])

    @patch("main.requests.get")
    def test_fetch_data_failure(self, mock_get):
        """
        Test case to test the fetch data function with failed to fetch th data.
        """
        mock_get.return_value.status_code = 404
        result = fetch_data(0, 0, "2024-07-01", "2024-07-03")
        self.assertIsNone(result)


class TestMainFunctionEntry(unittest.TestCase):

    @patch("main.fetch_data", return_value=MOCK_WEATHER_DATA)
    @patch("main.plot_graph")
    @patch("builtins.open", new_callable=mock_open)
    @patch("main.parse_args")
    def test_main_valid_action(self, mock_args, mock_file, mock_plot,
                               mock_fetch):
        mock_args.return_value.lat = 33.0
        mock_args.return_value.lon = 73.0
        mock_args.return_value.start_date = "2024-07-01"
        mock_args.return_value.end_date = "2024-07-03"
        mock_args.return_value.action = "avg_temp"

        main()
        mock_plot.assert_called_once()

    @patch("main.fetch_data", return_value=None)
    @patch("main.parse_args")
    def test_main_api_failed(self, mock_args, mock_fetch):
        mock_args.return_value.lat = 33.0
        mock_args.return_value.lon = 73.0
        mock_args.return_value.start_date = "2024-07-01"
        mock_args.return_value.end_date = "2024-07-03"
        mock_args.return_value.action = "avg_temp"
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_called()

    @patch("main.fetch_data", return_value=MOCK_WEATHER_DATA)
    @patch("main.parse_args")
    def test_main_invalid_action(self, mock_args, mock_fetch):
        mock_args.return_value.lat = 33.0
        mock_args.return_value.lon = 73.0
        mock_args.return_value.start_date = "2024-07-01"
        mock_args.return_value.end_date = "2024-07-03"
        mock_args.return_value.action = "unknown_action"
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_called_with("Unknown action: unknown_action")
