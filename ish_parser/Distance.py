from .Observation import Observation


class Distance(Observation):
  ''' observation of a temperature, which we can convert
  between farenheight and celsius, yay '''
  MILLIMETERS = 1
  METERS = 2
  INCHES = 3
  MISSING = [999, 99999, 999999]
  # Inches per cm
  INCH_CONVERSION_FACTOR = 1/2.54

  def get_inches(self):
    ''' convert the measurement to inches '''
    if self._obs_value in self.MISSING:
      return 'MISSING'
    if self._obs_units == self.MILLIMETERS:
      return round(self.INCH_CONVERSION_FACTOR * 10 * self._obs_value, 4)
    if self._obs_units == self.METERS:
      return round(self.INCH_CONVERSION_FACTOR / 100 * self._obs_value, 4)

  def __str__(self):
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)
