import unittest
from src.ish_parser import ish_parser
from src.ish_report import ish_report

class ish_parser_test(unittest.TestCase):

  ORD_FILE = 'tests/725300.txt'
  AUS_FILE = 'tests/722540-13904-2014'
  OTHER_RANDOM = 'tests/010060-99999-2014'
  RECURSIONBUG = 'tests/035480-99999-1943'
  OTHER_BUG = 'tests/723030-13714-1973'
  OLDRANDOMFILE = 'tests/725300-94846-1983'

  def test_from_file(self):
    ''' test that we can load a weather file from a file '''
    with open(self.ORD_FILE) as fp:
      content = fp.read()
    wf = ish_parser()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 4262)
    self.assertEquals(type(wf.get_reports()[10]), ish_report)
    self.assertEquals(len(wf.get_observations()), 3135)

  def test_random_old_file(self):
    ''' test that we can load another random old file with no problems 
    from 30 years ago '''
    with open(self.OLDRANDOMFILE) as fp:
      content = fp.read()
    wf = ish_parser()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 8760)
    self.assertEquals(type(wf.get_reports()[10]), ish_report)
    self.assertEquals(len(wf.get_observations()), 7466)

  def test_file_throwing_problems(self):
    ''' test a file that was getting stuck in crazy infinite recursion '''
    with open(self.RECURSIONBUG) as fp:
      content = fp.read()
    wf = ish_parser()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 4410)
    self.assertEquals(type(wf.get_reports()[10]), ish_report)
    
    one_report = wf.get_reports()[22]
    self.assertEquals(one_report.air_temperature.get_fahrenheit(), 'MISSING')

  def test_random_other_file(self):
    ''' test that we can load another random old file with no problems 
    from 30 years ago '''
    with open(self.OTHER_RANDOM) as fp:
      content = fp.read()
    wf = ish_parser()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 2816)
    self.assertEquals(type(wf.get_reports()[10]), ish_report)

  def test_another_weird_file(self):
    ''' test that we can load another random old file with no problems 
    from 30 years ago '''
    with open(self.OTHER_BUG) as fp:
      content = fp.read()
    wf = ish_parser()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 8580)
    one_report = wf.get_reports()[22]
    self.assertEquals(one_report.air_temperature.get_fahrenheit(), 64.4)

  def test_other_airport(self):
    with open(self.AUS_FILE) as fp:
      content = fp.read()
    wf = ish_parser()
    wf.loads(content)
    self.assertEquals(len(wf.get_reports()), 4237)
    self.assertEquals(type(wf.get_reports()[10]), ish_report)
    self.assertEquals(len(wf.get_observations()), 3333)
