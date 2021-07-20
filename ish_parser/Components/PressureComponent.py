from ..Pressure import Pressure
from .BaseComponent import BaseComponent

class PressureComponent(BaseComponent):
  ''' handle MA1 pressure type '''

  def loads(self, string):
      self.pressure_observation = {
          'altimeter_setting': Pressure(int(string[0:5])/10.0, Pressure.HECTOPASCALS, string[5:6]),
          'station_pressure': Pressure(int(string[6:11]) / 10.0, Pressure.HECTOPASCALS, string[11:12]),
      }
