import os
import unittest

from mdpmflc import app
from mdpmflc.utils.driver import get_config_fields


class TestParseSrc(unittest.TestCase):
    def test_get_config_fields(self):
        src_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "../static/MdpmflcTutorial.cpp")
        with open(src_fn, "r") as src_f:
            src = src_f.read()

#        for line in src.split("\n"):
#            print(line)
        print(get_config_fields(src, "pars"))


if __name__ == "__main__":
    cl = TestParseSrc()
    cl.test_get_config_fields()
