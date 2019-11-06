from .Observation import Observation

class Speed(Observation):
  ''' observation of a wind speed, which we can convert
  between m/s and mph, yay '''
  METERSPERSECOND = 1
  MILESPERHOUR = 2
  SPEED_SCALE = 10
  MPH_PER_MPS = 100 / 2.54 / 12 / 5280 * 60 * 60
  MISSING = [999, 9999, 999.9]

  def get_MilesPerHour(self):
    ''' convert the measurement to inches '''
    if self._obs_value in self.MISSING:
      return None
    if self._obs_units == self.METERSPERSECOND:
      return round(self._obs_value * self.MPH_PER_MPS, 4)

  def __str__(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)
