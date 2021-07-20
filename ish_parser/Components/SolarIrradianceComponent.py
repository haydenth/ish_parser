from ..Constant import Constant
from ..Minutes import Minutes
from ..Irradiance import Irradiance
from .BaseComponent import BaseComponent

class SolarIrradianceComponent(BaseComponent):
  ''' handle GM1 solar irradiance '''

  # TODO: add support for codes from 10-97
  DATA_FLAGS = {"00": "Untested", 
                "01": "Passed one-component test; data fall within max-min limit of Kt, Kn, or Kd",
                "02": "Passed two-component test; data fall within 0.03 of the Gompertz boundaries",
                "03": "Passed three-component test; data come within + 0.03 of satisfying Kt = Kn + Kd",
                "04": "Passed visual inspection: not used by SERI_QC1",
                "05": "Failed visual inspection: not used by SERI_QC1",
                "06": "Value estimated; passes all pertinent SERI_QC tests",
                "07": "Failed one-component test; lower than allowed minimum",
                "08": "Failed one-component test; higher than allowed maximum",
                "09": "Passed three-component test but failed two-component test by 0.05",
                "98": "Not Used"}

  def loads(self, string):
    self.solar_irradiance = {'time_period': Minutes(string[0:4]),
                             'global_irradiance': Irradiance(string[4:8]),
                             'irradiance_data_flag': Constant(string[8:10], None, 
                                                     string[10:11], self.DATA_FLAGS),
                             'direct_beam_irradiance': Irradiance(string[11:15]),
                             'direct_beam_irradiance_data_flag': Constant(string[15:17], None,
                                                                 string[17:18], self.DATA_FLAGS),
                             'diffuse_irradiance': Irradiance(string[18:22]),
                             'diffuse_irradiance_data_flag': Constant(string[22:24], None,
                                                             string[24:25], self.DATA_FLAGS),
                             'uvb_global_irradiance': Irradiance(string[26:30])}

  def __repr__(self):
    return str(self.solar_irradiance)

  def __str__(self):
    return str(self.solar_irradiance)
