class BaseComponent(object):
  ''' base component handler '''


class SnowDepthComponent(BaseComponent):
  ''' handle AJ1 snow depth types '''

  def loads(self, string):
    self.snow_depth = int(string[0:4])
    self.snow_depth_condition = string[4:5]
    self.snow_depth_quality = string[5:6]
    self.equivalent_water_depth = string[6:12]
    self.equivalent_water_depth_condition = string[12:13]
    self.equivalent_water_depth_quality = string[13:14]
