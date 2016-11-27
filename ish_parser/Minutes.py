from .Observation import Observation

class Minutes(Observation):
  ''' represents (obviously) minutes '''
  MISSING = 9999
  MINUTES_IN_HOUR = 60.00

  def __str__(self):
    if int(self._obs_value) == self.MISSING:
      return 'MISSING'
    else:
      return int(self._obs_value)

  def __eq__(self, other_value):
    if int(self._obs_value) == other_value:
      return True
    else:
      return False

  def get_hours(self):
    if int(self._obs_value) == self.MISSING:
      return 'MISSING'
    else:
      return self._obs_value / self.MINUTES_IN_HOUR
