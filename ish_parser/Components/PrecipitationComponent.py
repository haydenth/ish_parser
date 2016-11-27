from ..Distance import Distance
from .BaseComponent import BaseComponent

class PrecipitationComponent(BaseComponent):
  ''' handle AA1,2,3,4 precip types '''

  def loads(self, string):
    self.precipitation = {'hours': int(string[0:2]),
                          'depth': Distance(int(string[2:6])/10.0,
                                   Distance.MILLIMETERS, string[5:6])}
