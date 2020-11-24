import unittest
from graham_scan import io_graham_scan, left_kink, Point


class TestGrahamScan(unittest.TestCase):
    def test(self):
        scan_input = """
0\t0
2\t0
1\t1
2\t4
0\t1
""".strip()
        correct = """
0\t0
0\t1
2\t4
2\t0
""".strip()
        output = io_graham_scan(scan_input)
        self.assertEqual(output, correct)

    def test_left_kink(self):
        tests = [
            ((0, 0), (1, 2), (1, 3), True),
            ((0, 0), (1, 2), (2, 2), False),
            ((0, 0), (1, 2), (2, 1), False),
            ((0, 0), (2, -2), (4, -3), True)
        ]

        for t in tests:
            (p1, p2, p3, exp) = t
            self.assertEqual(left_kink(Point(*p1),
                                       Point(*p2),
                                       Point(*p3)),
                             exp)
