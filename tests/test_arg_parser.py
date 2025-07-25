import unittest
from arg_parser import parse_args


class TestArgParser(unittest.TestCase):
    def test_parse_args_valid(self):
        args = parse_args([
            '--lat', '30.5',
            '--lon', '70.2',
            '--start-date', '2024-07-01',
            '--end-date', '2024-07-03',
            '--action', 'avg_temp'
        ])
        self.assertEqual(args.lat, 30.5)
        self.assertEqual(args.lon, 70.2)
        self.assertEqual(args.start_date, '2024-07-01')
        self.assertEqual(args.end_date, '2024-07-03')
        self.assertEqual(args.action, 'avg_temp')
