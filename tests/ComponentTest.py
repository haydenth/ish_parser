import unittest
from src import SnowDepthComponent

class SnowDepthComponentTest(unittest.TestCase):

  def test_string(self):
    simple_string = '00089500007694'
    sd = SnowDepthComponent()
    sd.loads(simple_string)
    self.assertEqual(sd.snow_depth, {'depth': 8, 'quality': '5', 'condition': '9'})

class SkyCoverComponentTest(unittest.TestCase):

  def test_string(self):
    sample_string = '1005+999999999'
    sky = SnowCoverComponent()
    sky.loads(sample_string)
    self.assertEquals(sky.coverage, {'code': '10', 'quality': '5', 'height': 
    self.assertEquals(sky.cloud_type_code, '
