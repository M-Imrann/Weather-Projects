import argparse


def parse_args(args=None):
    '''
    parse_args function to parse the arguments
    '''
    parser = argparse.ArgumentParser(description="Weather Analyzer"
                                     "using Open-Meteo API")

    parser.add_argument("--lat", type=float, default=52.52,
                        help="Latitude of the Location")
    parser.add_argument("--lon", type=float, default=13.41,
                        help="Longitude of the Location")

    return parser.parse_args(args)
