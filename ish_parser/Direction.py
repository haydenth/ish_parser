from .Observation import Observation


class Direction(Observation):
  ''' Direction reflects an angle (usually wind direction). It should
  always range from 0-360. Missing is 999 '''
  RADIANS = 1
  MISSING = 999

  def __str__(self):
    if int(self._obs_value) == self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)

  def __eq__(self, other_value):
    if int(self._obs_value) == int(other_value):
      return True
    else:
      return False
