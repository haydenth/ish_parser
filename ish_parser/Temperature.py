from .Observation import Observation


class Temperature(Observation):
  ''' observation of a temperature, which we can convert
  between farenheight and celsius, yay '''
  CELSIUS = 1
  FARENHEIT = 2
  MISSING = [999, 999.9]

  def get_fahrenheit(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    if self._obs_units == self.CELSIUS:
      return round(1.8 * self._obs_value + 32.0, 1)

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
