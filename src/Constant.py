from .Observation import Observation


class Constant(Observation):
  ''' constant is for constant variables that have types
  or indices associated with them like types of clouds, etc'''
  MISSING = ["99"]

  def __str__(self):
    if self._obs_value in self._obs_index.keys():
      return self._obs_index.get(self._obs_value)  
    if self._obs_value in self.MISSING:
      return 'MISSING'
    else:
      return str(self._obs_value)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, value2):
    if self._obs_value in self._obs_index.keys():
      if self._obs_index.get(self._obs_value) == value2:
        return True

    if str(self._obs_value) == str(value2):
      return True
    else:
      return False
