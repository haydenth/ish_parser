from src import Minutes
import unittest

class Minutes_test(unittest.TestCase):
  
  def test_simple(self):
    minutes = 9999
    self.assertEqual(str(Minutes(minutes)), 'MISSING')

  def test_hours_conversion(self):
    minutes = 60
    self.assertEquals(Minutes(minutes).get_hours(), 1)

    minutes = 75
    self.assertEquals(Minutes(minutes).get_hours(),1.25)
