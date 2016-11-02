from .Distance import Distance
from .CloudCoverage import CloudCoverage
from .Constant import Constant
from .Minutes import Minutes
from .Irradiance import Irradiance

class BaseComponent(object):
  ''' base component handler '''

class PresentWeatherComponent(BaseComponent):
  ''' handle any AU Type'''
  INTENSITY = {'0': '', '1': 'Light', '2': 'Moderate',
               '3': 'Heavy', '4': 'Vicinity', '5': 'MISSING'}
  DESCRIPTOR = {'0': '', '1': 'Shallow', '2': 'Partial',
                '3': 'Patches', '4': 'Low Drifting', '5': 'Blowing',
                '6': 'Showers', '7': 'Thunderstorm', '8': 'Freezing',
                '9': 'MISSING'}
  PRECIP = {'00': 'No Precip', '01': 'Drizzle', '02': 'Rain',
            '03': 'Snow', '04': 'Snow Grains', '05': 'Ice Crystals',
            '06': 'Ice Pellets', '07': 'Hail', '08': 'Small Hail',
            '09': 'Unknown Precip'}

  def loads(self, string):
    self.present_weather_array = {'intensity': self.INTENSITY[string[0:1]],
                                  'descriptor': self.DESCRIPTOR[string[1:2]],
                                  'precipitation': self.PRECIP[string[2:4]]}
    present = self.present_weather_array
    try:
      self.present_weather = "%s %s %s" % (present['intensity'],
                                           present['descriptor'],
                                           present['precipitation'])
      self.present_weather = self.present_weather.replace("  ", " ")
    except:
      self.present_weather = ""

class PrecipitationComponent(BaseComponent):
  ''' handle AA1,2,3,4 precip types '''

  def loads(self, string):
    self.precipitation = {'hours': int(string[0:2]),
                          'depth': Distance(int(string[2:6])/10.0,
                                   Distance.MILLIMETERS, string[5:6])}

class SkyCoverComponent(BaseComponent):
  ''' handle GA1..GA8 sky component types '''

  CLOUD_TYPES = {
    "00": "Cirrus (Ci)",
    "01": "Cirrocumulus (Cc)",
    "02": "Cirrostratus (Cs)",
    "03": "Altocumulus (Ac)",
    "04": "Altostratus (As)",
    "05": "Nimbostratus (Ns)",
    "06": "Stratocumulus (Sc)",
    "07": "Stratus (St)",
    "08": "Cumulus (Cu)",
    "09": "Cumulonimbus (Cb)",
    "10": """Cloud not visible owing to darkness, fog,
           duststorm, sandstorm, or other analogous phenomena / sky obscured""",
    "11": "Not used",
    "12": "Towering Cumulus (Tcu)",
    "13": "Stratus fractus (Stfra)",
    "14": "Stratocumulus Lenticular (Scsl)",
    "15": "Cumulus Fractus (Cufra)",
    "16": "Cumulonimbus Mammatus (Cbmam)",
    "17": "Altocumulus Lenticular (Acsl)",
    "18": "Altocumulus Castellanus (Accas)",
    "19": "Altocumulus Mammatus (Acmam)",
    "20": "Cirrocumulus Lenticular (Ccsl)",
    "21": "Cirrus and/or Cirrocumulus",
    "22": "Stratus and/or Fracto-stratus",
    "23": "Cumulus and/or Fracto-cumulus"}
  
  def loads(self, string):
    self.sky_cover = {'coverage': CloudCoverage(string[0:2],
                                  CloudCoverage.OKTA, string[2:3]),
                      'base_height': Distance(int(string[4:9]),
                                     Distance.METERS, string[9:10]),
                      'cloud_type': Constant(string[9:11], None, 
                                    string[11:12], self.CLOUD_TYPES)}

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

class SnowDepthComponent(BaseComponent):
  ''' handle AJ1 snow depth types '''

  def loads(self, string):
    self.snow_depth = {'depth': int(string[0:4]),
                       'condition': string[4:5],
                       'quality': string[5:6]}
    self.equivalent_water = {'depth': string[6:12],
                             'condition': string[12:13],
                             'quality': string[13:14]}
