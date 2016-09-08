import unittest
from src import SnowDepthComponent

class SnowDepthComponentTest(unittest.TestCase):

  def test_string(self):
    simple_string = '00089500007694'
    sd = SnowDepthComponent()
    sd.loads(simple_string)
    self.assertEqual(sd.snow_depth, {'depth': 8, 'quality': '5', 'condition': '9'})
