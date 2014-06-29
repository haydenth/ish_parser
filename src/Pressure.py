from Observation import Observation


class Pressure(Observation):
  ''' Pressure is .. well.. pressure '''
  HECTOPASCALS = 1
  MISSING = 99999

  def __eq__(self, other_value):
    if int(self._obs_value) == int(other_value):
      return True
    else:
      return False

  def __str__(self):
    if self._obs_value == self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)
