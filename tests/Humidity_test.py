from src import Humidity
import unittest

class Humidity_test(unittest.TestCase):
  
  def test_conversion(self):
    air_temp = 16.1
    dewpoint = 10.6
    self.assertEqual(Humidity(air_temp, dewpoint), 70)
