import unittest
import subprocess
import numpy as np
import pandas as pd
from io import StringIO
from unittest.mock import patch

from Flowers import parse_design_string, read_design, make_bouquets


test_design_string = "BL2a2b3"
test_parsed_design = ["B","L",np.array(["2a","2b"]), 3]


test_design_permutation = pd.read_csv("test/test_permutations.csv")

test_flower_stock = test_design_permutation.sum()
test_output_bouquets = "BL1a2b\nBL2a1b"

# Expected output from challenge example input
test_flowers_output = b"AS1a2b\nBL2a\nAS2a1b\n"

class TestExampleInput(unittest.TestCase):
    maxDiff = None

    def test_parse_design_string(self):
        test_output = list(parse_design_string(test_design_string))
        np.testing.assert_equal(test_parsed_design, test_output)


    def test_read_design(self):
        design_output = read_design(test_design_string)
        pd.testing.assert_frame_equal(test_design_permutation, design_output)

    def test_make_bouquets(self): 
        with patch('sys.stdout', new=StringIO()) as real_output:
            make_bouquets(test_design_permutation, test_flower_stock)
            self.assertEqual(test_output_bouquets, real_output.getvalue().strip())

    def test_exampleInOut(self):
        real_output = subprocess.Popen("cat test/sample_input.txt |  python3 Flowers.py", 
                                shell=True,  stdout=subprocess.PIPE)    
        self.assertEqual(test_flower_output, real_output.stdout.read())


if __name__ == '__main__':
    unittest.main(verbosity=3)
