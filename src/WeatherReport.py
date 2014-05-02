import sys
from Temperature import Temperature
from Units import Units
from datetime import datetime
from Components import SnowDepthComponent

class WeatherReportException(BaseException):
  ''' handler class for exceptions '''

class WeatherReport(object):

  RECORD_DELIMITER = "\n"
  PREAMBLE_LENGTH = 105
  TEMPERATURE_SCALE = 10
  GEO_SCALE = 1000
  MISSING = '9999'
  MAP = {'AA1': ['LIQUID-PRECIP', 8],
         'AA2': ['LIQUID-PRECIP', 8],
         'AA3': ['LIQUID-PRECIP', 8],
         'AA4': ['LIQUID-PRECIP', 8],
         'AB1': ['LIQUID-PRECIP-MONTHLY', 7],
         'AC1': ['PRECIPITATION-OBSERVATION-HISTORY', 6],
         'AD1': ['LIQUID-PRECIP-GREATEST-AMOUNT-24-HOURS', 19],
         'AE1': ['LIQUID-PREICP-NUMBER-OF-DAYS', 12],
         'AG1': ['PRECIPITATION-ESTIMATED-OBSERVATION', 4],
         'AH1': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AH2': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AH3': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AH4': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AH5': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AH6': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AI1': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AI2': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AI3': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AI4': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AI5': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AI6': ['LIQUID-PRECIP-MAX-SHORT-DURATION', 15],
         'AJ1': ['SNOW_DEPTH', 14, SnowDepthComponent],
         'AK1': ['SNOW-DEPTH-GREATEST-ON-GROUND', 12],
         'AL1': ['SNOW-ACCUMULATION', 7],
         'AL2': ['SNOW-ACCUMULATION', 7],
         'AL3': ['SNOW-ACCUMULATION', 7],
         'AL4': ['SNOW-ACCUMULATION', 7],
         'AM1': ['SNOW-ACCUMULATION-GREATEST', 18],
         'AN1': ['SNOW-ACCUMULATION-FOR-MONTH', 9],
         'AO1': ['LIQUID-PRECIP', 8],
         'AO2': ['LIQUID-PRECIP', 8],
         'AO3': ['LIQUID-PRECIP', 8],
         'AO4': ['LIQUID-PRECIP', 8],
         'AP1': ['15MIN-LIQUID-PRECIP', 6],
         'AP2': ['15MIN-LIQUID-PRECIP', 6],
         'AP3': ['15MIN-LIQUID-PRECIP', 6],
         'AP4': ['15MIN-LIQUID-PRECIP', 6],
         'AU1': ['WEATHER-OCCURANCE', 8],
         'AU2': ['WEATHER-OCCURANCE', 8],
         'AU3': ['WEATHER-OCCURANCE', 8],
         'AU4': ['WEATHER-OCCURANCE', 8],
         'AU5': ['WEATHER-OCCURANCE', 8],
         'AU6': ['WEATHER-OCCURANCE', 8],
         'AU7': ['WEATHER-OCCURANCE', 8],
         'AU8': ['WEATHER-OCCURANCE', 8],
         'AU9': ['WEATHER-OCCURANCE', 8],
         'AW1': ['PRESENT-WEATHER-OBSERVATION', 3],
         'AW2': ['PRESENT-WEATHER-OBSERVATION', 3],
         'AW3': ['PRESENT-WEATHER-OBSERVATION', 3],
         'AW4': ['PRESENT-WEATHER-OBSERVATION', 3],
         'AX1': ['PAST-WEATHER-OBSERVATION', 6],
         'AX2': ['PAST-WEATHER-OBSERVATION', 6],
         'AX3': ['PAST-WEATHER-OBSERVATION', 6],
         'AX4': ['PAST-WEATHER-OBSERVATION', 6],
         'AX5': ['PAST-WEATHER-OBSERVATION', 6],
         'AX6': ['PAST-WEATHER-OBSERVATION', 6],
         'AY1': ['PAST-WEATHER-OBSERVATION-MANUAL', 5],
         'AY2': ['PAST-WEATHER-OBSERVATION-MANUAL', 5],
         'AZ1': ['PAST-WEATHER-OBSERVATION-AUTOMATED', 5],
         'AZ2': ['PAST-WEATHER-OBSERVATION-AUTOMATED', 5],
         'CB1': ['SUBHOURLY-OBSERVED-LIQ-PRECIP-SECONDARY', 10],
         'CB2': ['SUBHOURLY-OBSERVED-LIQ-PRECIP-SECONDARY', 10],
         'CF1': ['HOURLY-FAN-SPEED', 6],
         'CF2': ['HOURLY-FAN-SPEED', 6],
         'CF3': ['HOURLY-FAN-SPEED', 6],
         'CG1': ['PRIMARY-SENSOR', 8],
         'CG2': ['PRIMARY-SENSOR', 8],
         'CG3': ['PRIMARY-SENSOR', 8],
         'CH1': ['HOURLY-RELATIVE-HUMIDITY', 15],
         'CH2': ['HOURLY-RELATIVE-HUMIDITY', 15],
         'CI1': ['RELATIVE-HUMIDITY-TEMPERATURE', 28],
         'CN1': ['HOURLY-BATTERY-VOLTAGE', 18],
         'CN2': ['HOURLY-DIAGNOSTIC', 18],
         'CN3': ['SECONDARY-HOURLY-DIAGNOSTIC', 16],
         'CN4': ['SECONDARY-HOURLY-DIAGNOSTIC', 16],
         'CO1': ['US-NETWORK-METADATA', 5],
         'CO2': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO3': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO4': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO5': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO6': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO7': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO8': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CO9': ['US-COOP-NETWORK-TIME-OFFSET', 8],
         'CR1': ['CONTROL-SECTION', 7],
         'CT1': ['SUBHOURLY-TEMPERATURE', 7],
         'CT3': ['SUBHOURLY-TEMPERATURE', 7],
         'CT2': ['SUBHOURLY-TEMPERATURE', 7],
         'CU1': ['HOURLY-TEMPERATURE', 13],
         'CU2': ['HOURLY-TEMPERATURE', 13],
         'CU3': ['HOURLY-TEMPERATURE', 13],
         'CV1': ['HOURLY-TEMPERATURE-EXTREME', 26],
         'CV2': ['HOURLY-TEMPERATURE-EXTREME', 26],
         'CV3': ['HOURLY-TEMPERATURE-EXTREME', 26],
         'CW1': ['SUBHOURLY-WETNESS', 14],
         'CX1': ['HOURLY-GEONOR-VIBRATING-WIRE', 26],
         'CX2': ['HOURLY-GEONOR-VIBRATING-WIRE', 26],
         'CX3': ['HOURLY-GEONOR-VIBRATING-WIRE', 26],
         'ED1': ['RUNWAY-VISUAL-RANGE', 8],
         'GA1': ['SKY-COVER-LAYER', 13],
         'GA2': ['SKY-COVER-LAYER', 13],
         'GA3': ['SKY-COVER-LAYER', 13],
         'GA4': ['SKY-COVER-LAYER', 13],
         'GA5': ['SKY-COVER-LAYER', 13],
         'GA6': ['SKY-COVER-LAYER', 13],
         'GD1': ['SKY-COVER-SUMMATION', 12],
         'GD2': ['SKY-COVER-SUMMATION', 12],
         'GD3': ['SKY-COVER-SUMMATION', 12],
         'GD4': ['SKY-COVER-SUMMATION', 12],
         'GD5': ['SKY-COVER-SUMMATION', 12],
         'GD6': ['SKY-COVER-SUMMATION', 12],
         'GE1': ['SKY-CONDITION', 19],
         'GF1': ['SKY-CONDITION', 23],
         'GG1': ['BELOW-STATION-CLOUD-LAYER', 15],
         'GG2': ['BELOW-STATION-CLOUD-LAYER', 15],
         'GG3': ['BELOW-STATION-CLOUD-LAYER', 15],
         'GG4': ['BELOW-STATION-CLOUD-LAYER', 15],
         'GG5': ['BELOW-STATION-CLOUD-LAYER', 15],
         'GG6': ['BELOW-STATION-CLOUD-LAYER', 15],
         'GH1': ['HOURLY-SOLAR-RADIATION', 28],
         'GJ1': ['SUNSHINE', 5],
         'GK1': ['SUNSHINE-OBSERVATION', 4],
         'GL1': ['SUSHINE-OBSERVATION-FOR-MONTH', 6],
         'GM1': ['SOLAR-IRRADIANCE', 30],
         'GN1': ['SOLAR-RADIATION', 28],
         'GO1': ['NET-SOLAR-RADIATION', 19],
         'GP1': ['MODELED-SOLAR', 31], 
         'GQ1': ['HOURLY-SOLAR-ANGLE', 14],
         'GR1': ['HOURLY-EXTRATERRESTRIAL-RADIATION', 14],
         'HL1': ['HAIL', 4],
         'IA1': ['GROUND-SURFACE', 3],
         'IA2': ['GROUND-SURFACE', 9],
         'IB1': ['HOURLY-SURFACE', 27],
         'IB2': ['HOURLY-SURFACE', 13],
         'IC1': ['GROUND-SURFACE', 25],
         'KA1': ['EXTREME-AIR-TEMPERATURE', 10],
         'KA2': ['EXTREME-AIR-TEMPERATURE', 10],
         'KA3': ['EXTREME-AIR-TEMPERATURE', 10],
         'KA4': ['EXTREME-AIR-TEMPERATURE', 10],
         'KB1': ['AVERAGE-AIR-TEMPERATUER', 10],
         'KB2': ['AVERAGE-AIR-TEMPERATUER', 10],
         'KB3': ['AVERAGE-AIR-TEMPERATUER', 10],
         'KC1': ['EXTREME-AIR-TEMP-FOR-MONTH', 14],
         'KC2': ['EXTREME-AIR-TEMP-FOR-MONTH', 14],
         'KD1': ['HEATING-COOLING-DEGREE-DAYS', 9],
         'KD2': ['HEATING-COOLING-DEGREE-DAYS', 9],
         'KE1': ['EXTREME-TEMPS-EXCEEDING-CRITERIA', 12],
         'KF1': ['HOURLY-CALCULATED-TEMP', 6],
         'KG1': ['AVERAGE-DEW_POINT', 11],
         'KG2': ['AVERAGE-DEW_POINT', 11],
         'MA1': ['ATMOSPHERIC-PRESSURE', 12],
         'MD1': ['ATMOSPHERIC-PRESSURE-CHANGE', 11],
         'ME1': ['GEOPOTENTIAL-HEIGHT', 6],
         'MF1': ['ATMOSPHERIC-PRESSURE-STP-SLP', 12],
         'MG1': ['ATMOSPHERIC-PRESSURE', 12],
         'MH1': ['ATMOSPHERIC-PRESSURE-FOR-MONTH', 12],
         'MK1': ['ATMOSPHERIC-PRESSURE-FOR-MONTH', 24],
         'MW1': ['PRESENT-WEATHER-OBS', 3],
         'MW2': ['PRESENT-WEATHER-OBS', 3],
         'MW3': ['PRESENT-WEATHER-OBS', 3],
         'MW4': ['PRESENT-WEATHER-OBS', 3],
         'MW5': ['PRESENT-WEATHER-OBS', 3],
         'MW6': ['PRESENT-WEATHER-OBS', 3],
         'MW7': ['PRESENT-WEATHER-OBS', 3],
         'MV1': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'MV2': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'MV3': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'MV4': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'MV5': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'MV6': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'MV7': ['PRESENT-WEATHER-IN-VICINITY', 3],
         'N01': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'N02': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'N03': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'N04': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'P01': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'P02': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'P03': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'P04': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'Q01': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'Q02': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'Q03': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'Q04': ['ORIGINAL-OBSERVATION-ELEMENT', 13],
         'REM': ['REMARKS', 1095],
         'EQD': ['ELEMENT QUALITY', 16],
         'NO1': ['ORIGINAL-OBSERVATION', 13],
         'OC1': ['WIND-GUST-OBSERVATION', 5],
         'OD1': ['SUPPLEMENTARY-WIND-OBSERVATION', 11],
         'OD2': ['SUPPLEMENTARY-WIND-OBSERVATION', 11],
         'OD3': ['SUPPLEMENTARY-WIND-OBSERVATION', 11],
         'OE1': ['SUMMARY-OF-DAY-WIND', 16],
         'OE2': ['SUMMARY-OF-DAY-WIND', 16],
         'OE3': ['SUMMARY-OF-DAY-WIND', 16],
         'QNN': ['ORIGINAL-OBSERVATION-NCDC', 999],
         'RH1': ['RELATIVE-HUMIDITY', 9],
         'RH2': ['RELATIVE-HUMIDITY', 9],
         'RH3': ['RELATIVE-HUMIDITY', 9],
         'SA1': ['SEA-SURFACE-TEMPERATURE', 5],
         'ST1': ['SOIL-TEMPERATURE', 17]}

  def __getattr__(self, attribute_name):
    for (addl_code, addl) in self._additional.items():
      try:
        addl_value = getattr(addl, attribute_name)
        return addl_value
      except:
        ''' no attribute found '''

  def loads(self, noaa_string):
    ''' load in a report (or set) from a string '''
    self.weather_station = noaa_string[4:10]
    self.wban = noaa_string[10:15]
    expected_length = int(noaa_string[0:4]) + self.PREAMBLE_LENGTH
    actual_length = len(noaa_string)
    if actual_length != expected_length:
      msg = "Non matching lengths. Expected %d, got %d" % (expected_length, actual_length)
      raise WeatherReportException(msg)

    self.datetime = datetime.strptime(noaa_string[15:27], '%Y%m%d%H%M')
    self.report_type = noaa_string[41:46].strip()

    self.latitude = float(noaa_string[28:34]) / self.GEO_SCALE
    self.longitude = float(noaa_string[34:41]) / self.GEO_SCALE
    self.elevation = int(noaa_string[46:51])

    ''' other mandatory fields '''
    self.wind_observation_direction = noaa_string[60:63]
    self.wind_observation_direction_quality = noaa_string[63:64]
    self.wind_observation_direction_type = noaa_string[64:64]
    self.wind_speed = int(noaa_string[65:69])
    self.wind_speed_quality = noaa_string[69:70]
    self.sky_ceiling = int(noaa_string[70:75])
    self.sky_ceiling_quality = noaa_string[75:76]
    self.sky_ceiling_determination = noaa_string[76:77]
    self.visibility_distance = int(noaa_string[78:84])
    self.visibility_quality = noaa_string[84:85]
    self.visibility_variability = noaa_string[85:86]
    self.visibility_variability_quality = noaa_string[86:87]

    self.air_temperature = Temperature(int(noaa_string[87:92]) / self.TEMPERATURE_SCALE,
                                           Units.CELSIUS,
                                           noaa_string[92:93])
    self.dew_point_temperature = int(noaa_string[93:98])
    self.dew_point_temperature_quality = noaa_string[98:99]
    self.sea_level_pressure = int(noaa_string[99:104])
    self.sea_level_pressure_quality = noaa_string[104:104]

    ''' handle the additional fields '''
    self._additional = {}
    additional = noaa_string[105:108]
    if additional == 'ADD':
      position = 108
      while position <= expected_length:
        (position, (addl_code, addl_string)) = self._get_component(noaa_string, position)
        self._additional[addl_code] = addl_string

  def _get_component(self, string, initial_pos):
    add_code = string[initial_pos:initial_pos+3]
    initial_pos += 3
    try:
      useable_map = self.MAP[add_code]
    except:
      raise BaseException("Cannot find code %s in string %s (%d)" % (add_code, string, initial_pos))
    new_position = initial_pos + useable_map[1]
    string_value = string[initial_pos:new_position]
    
    try:
      object_value = useable_map[2]()
      object_value.loads(string_value)
    except:
      object_value = string_value

    return (new_position, [add_code, object_value])

  def get_additional_field(self, addl_code):
    return self._additional[addl_code] 

  def additional(self):
    return self._additional
