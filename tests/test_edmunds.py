import unittest
import requests
import logging
from automarket import edmunds


logging.basicConfig(level=logging.INFO)


class TestEdmunds(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.infiniti = ('infiniti', 'q70', '2015')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_value(self):
        values = edmunds.get_values(*self.infiniti)

        for k, v in values.items():
            print(f"{k} = \n")
            print(v)
