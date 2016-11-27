from .Observation import Observation


class CloudCoverage(Observation):
  '''okta is a unit of measurement used to 
  describe the amount of cloud cover at any given location such 
  as a weather station. Sky conditions are estimated in 
  terms of how many eighths of the sky are covered in cloud, 
  ranging from 0 oktas (completely clear sky) through to 
  8 oktas (completely overcast).
  '''
  OKTA = 1
  MISSING = ['99', 99]

  def __str__(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, value2):
    if self._obs_value == value2:
      return True
    else:
      return False
