import unittest
from arg_parser import parse_args


class TestArgParser(unittest.TestCase):
    def test_default_arguments(self):
        args = parse_args([])
        self.assertEqual(args.lat, 52.52)
        self.assertEqual(args.lon, 13.41)

    def test_custom_arguments(self):
        args = parse_args(["--lat", "40.0", "--lon", "70.0"])
        self.assertEqual(args.lat, 40.0)
        self.assertEqual(args.lon, 70.0)

    def test_partial_arguments(self):
        args = parse_args(["--lat", "25.5"])
        self.assertEqual(args.lat, 25.5)
        self.assertEqual(args.lon, 13.41)  # default lon


if __name__ == '__main__':
    unittest.main()
