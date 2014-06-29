class ObservationException(BaseException):
  ''' base exception handling class for  ish_observations'''


class Observation(object):
  ''' base class to hold observational data '''

  def __init__(self, obs_value, obs_units='', obs_quality=''):
    self._obs_value = obs_value
    self._obs_units = obs_units
    self._obs_quality = obs_quality

  def __repr__(self):
    return str(self._obs_value)

  def __eq__(self, other_value):
    if self._obs_value == other_value:
      return True
    else:
      return False
