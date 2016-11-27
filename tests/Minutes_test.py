from ish_parser import Minutes
import unittest

class Minutes_test(unittest.TestCase):
  
  def test_simple(self):
    minutes = 9999
    self.assertEqual(str(Minutes(minutes)), 'MISSING')

  def test_hours_conversion(self):
    ''' just do some simple verification that we convert properly
    minutes to the right number of hours'''
    self.assertEqual(Minutes(60).get_hours(), 1)
    self.assertEqual(Minutes(75).get_hours(),1.25)
