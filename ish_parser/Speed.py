from .Observation import Observation

class Speed(Observation):
  ''' observation of a temperature, which we can convert
  between farenheight and celsius, yay '''
  METERSPERSECOND = 1
  MILESPERHOUR = 1
  MISSING = [999, 9999, 999.9]

  def get_miles(self):
    ''' convert the measurement to inches '''
    if self._obs_value in self.MISSING:
      return 'MISSING'
    if self._obs_units == self.METERSPERSECOND:
      return round(2.23694 * self._obs_value, 4)

  def __str__(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)
