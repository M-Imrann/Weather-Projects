import argparse


def parse_args(args=None):
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Weather Analyzer "
                                     "using Open-Meteo API")

    parser.add_argument("--lat", type=float, default=52.52,
                        help="Latitude of the location")
    parser.add_argument("--lon", type=float, default=13.41,
                        help="Longitude of the location")
    parser.add_argument("--start-date", type=str, required=True,
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, required=True,
                        help="End date (YYYY-MM-DD)")

    parser.add_argument(
        "--action", type=str, required=True,
        choices=[
            "max_temp", "min_temp", "avg_temp",
            "max_wind", "min_wind", "avg_wind",
            "max_soil", "min_soil", "avg_soil",
            "extreme_temp_date", "extreme_wind_date", "extreme_soil_date"
        ],
        help="Action to perform"
    )

    return parser.parse_args(args)
