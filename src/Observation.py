class ObservationException(BaseException):
  ''' base exception handling class for  ish_observations'''


class Observation(object):
  ''' base class to hold observational data '''

  def __init__(self, obs_value, obs_units='', obs_quality='', obs_index=None):
    self._obs_value = obs_value
    self._obs_units = obs_units
    self._obs_quality = obs_quality
    self._obs_index = obs_index

  def __repr__(self):
    return str(self._obs_value)

  def __eq__(self, other_value):
    if self._obs_value == other_value:
      return True
    else:
      return False

  def get_numeric(self):
      if isinstance(self.MISSING, list):
          return self._get_numeric(self.MISSING)
      else:
          return self._get_numeric([self.MISSING])

  def _get_numeric(self, missing):
      if self._obs_value in missing:
          return float('NaN')
      elif int(self._obs_value) in missing:
          return float('NaN')
      else:
          return float(self._obs_value)
