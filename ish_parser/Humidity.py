import math

from .Observation import Observation


class Humidity(object):

  def __init__(self, air_temp, dew_point):
    ''' both must be temperature objects
        100*(EXP((17.625*TD)/(243.04+TD))/EXP((17.625*T)/(243.04+T))) '''
    try:
      self.humidity = 100*(math.exp((17.625*float(dew_point))/(243.04+float(dew_point)))/math.exp((17.625*float(air_temp))/(243.04+float(air_temp))))
      self.humidity = round(self.humidity)
    except:
      self.humidity = "MISSING"

  def __str__(self):
    return str(self.humidity)

  def __eq__(self, other_value):
    if self.humidity == other_value:
      return True
    return False

  def get_numeric(self):
      if self.humidity == "MISSING":
          return float('NaN')
      else:
          return self.humidity
