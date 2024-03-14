"""Tests the calculator"""

import subprocess
import unittest

class File_based_application(unittest.TestCase):
    def test_set1(self):
        result = subprocess.check_output(f"python -m src.run ../test.txt").decode("utf-8")
        assert int(result) == 90

    def test_set2(self):
        result = subprocess.check_output(f"python -m src.run ../test2.txt").decode("utf-8")
        assert [5,3,6] == [int(x) for x in result.strip().split()]

    def test_set3(self):
        result = subprocess.check_output(f"python -m src.run ../test3.txt").decode("utf-8")
        assert int(result) == 11
