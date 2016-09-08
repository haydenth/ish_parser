from .Observation import Observation


class Pressure(Observation):
  ''' Pressure is .. well.. pressure '''
  HECTOPASCALS = 1
  MISSING = [99999, 9999.9]

  def __eq__(self, other_value):
    if int(self._obs_value) == int(other_value):
      return True
    else:
      return False

  def __str__(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)

  def get_inches(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return round(self._obs_value * 0.02953, 2)
