import unittest
from src import CloudCoverage
from src import SnowDepthComponent, SkyCoverComponent

class SnowDepthComponentTest(unittest.TestCase):

  def test_string(self):
    simple_string = '00089500007694'
    sd = SnowDepthComponent()
    sd.loads(simple_string)
    self.assertEqual(sd.snow_depth, {'depth': 8, 'quality': '5', 'condition': '9'})

class SkyCoverComponentTest(unittest.TestCase):

  def test_string(self):
    sample_string = '005+999999999'
    sky = SkyCoverComponent()
    sky.loads(sample_string)
    self.assertEquals(sky.sky_cover['coverage'], CloudCoverage('00', CloudCoverage.OKTA, '5'))
