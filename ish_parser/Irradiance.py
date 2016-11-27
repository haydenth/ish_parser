from .Observation import Observation

class Irradiance(Observation):
  ''' Global horizontal irradiance measured using a pyranometer. Unit is watts per square meter
   (W/m2) in whole values. Waveband ranges from 0.4 - 2.3 micrometers.'''
  MISSING = 9999

  def __str__(self):
    if int(self._obs_value) == self.MISSING:
      return 'MISSING'
    else:
      return self._obs_value

  def __eq__(self, other_value):
    if int(self._obs_value) == other_value:
      return True
    else:
      return False
