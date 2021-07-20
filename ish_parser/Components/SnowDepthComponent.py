from .BaseComponent import BaseComponent

class SnowDepthComponent(BaseComponent):
  ''' handle AJ1 snow depth types '''

  def loads(self, string):
    self.snow_depth = {'depth': int(string[0:4]),
                       'condition': string[4:5],
                       'quality': string[5:6]}
    self.equivalent_water = {'depth': string[6:12],
                             'condition': string[12:13],
                             'quality': string[13:14]}

  def __repr__(self):
    return str({'snow depth': self.snow_depth, 'equivalent water': self.equivalent_water})

  def __str__(self):
    return str((self.snow_depth, self.equivalent_water))
