import unittest
from src import CloudCoverage, Minutes, Irradiance
from src import SnowDepthComponent, SkyCoverComponent, SolarIrradianceComponent
from src import SkyConditionObservationComponent
from src import SkyCoverSummationComponent

class SkyCoverSummationComponentTest(unittest.TestCase):

  def test_string(self):
    simple_string = '4991+0061059'
    sd = SkyCoverSummationComponent()
    sd.loads(simple_string)
    self.assertEqual(sd.sky_cover_summation, {'coverage': 'OVERCAST - 8/8 coverage',
                                               'secondary_coverage': 'Missing',
                                               'height': 610,
                                               'characteristic': 'Missing'})

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
    self.assertEqual(sky.sky_cover['coverage'], CloudCoverage('00', CloudCoverage.OKTA, '5'))

class SolarIrradianceComponentTest(unittest.TestCase):
  
  def test_string(self):
    sample_string = '006010140690989029013102999999'
    sol = SolarIrradianceComponent()
    sol.loads(sample_string)
    self.assertEqual(sol.solar_irradiance['time_period'], Minutes(60))
    self.assertEqual(sol.solar_irradiance['global_irradiance'], Irradiance('1014'))
    self.assertEqual(sol.solar_irradiance['irradiance_data_flag'], 'Value estimated; passes all pertinent SERI_QC tests')
    self.assertEqual(sol.solar_irradiance['direct_beam_irradiance'], Irradiance('0989'))
    self.assertEqual(sol.solar_irradiance['uvb_global_irradiance'], Irradiance('9999'))

class SkyConditionObservationComponentTest(unittest.TestCase):

  def test_string(self):
    sample_string = '08991999999999999999999'
    sky = SkyConditionObservationComponent()
    sky.loads(sample_string)
    self.assertEqual(sky.sky_condition_observation['total_coverage'],
                      CloudCoverage('08', CloudCoverage.OKTA, '1'))
    self.assertEqual(sky.sky_condition_observation['total_lowest_coverage'],
                      CloudCoverage('99', CloudCoverage.OKTA, '9'))
