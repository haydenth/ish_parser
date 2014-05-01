import unittest
from src.WeatherFile import WeatherFile
from src.WeatherReport import WeatherReport

class WeatherFileTest(unittest.TestCase):

  ORD_FILE = 'tests/725300.txt'
  AUS_FILE = 'tests/722540-13904-2014'
  OTHER_RANDOM = 'tests/010060-99999-2014'
  OLDRANDOMFILE = 'tests/725300-94846-1983'

  def test_from_file(self):
    ''' test that we can load a weather file from a file '''
    with open(self.ORD_FILE) as fp:
      content = fp.read()
    wf = WeatherFile()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 4262)
    self.assertEquals(type(wf.get_reports()[10]), WeatherReport)
    self.assertEquals(len(wf.get_observations()), 3135)

  def test_random_old_file(self):
    ''' test that we can load another random old file with no problems 
    from 30 years ago '''
    with open(self.OLDRANDOMFILE) as fp:
      content = fp.read()
    wf = WeatherFile()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 8760)
    self.assertEquals(type(wf.get_reports()[10]), WeatherReport)
    self.assertEquals(len(wf.get_observations()), 7466)

  def test_random_other_file(self):
    ''' test that we can load another random old file with no problems 
    from 30 years ago '''
    with open(self.OTHER_RANDOM) as fp:
      content = fp.read()
    wf = WeatherFile()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 2816)
    self.assertEquals(type(wf.get_reports()[10]), WeatherReport)
    self.assertEquals(len(wf.get_observations()), 2816)

  def test_other_airport(self):
    with open(self.AUS_FILE) as fp:
      content = fp.read()
    wf = WeatherFile()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 4237)
    self.assertEquals(type(wf.get_reports()[10]), WeatherReport)
    self.assertEquals(len(wf.get_observations()), 3333)
