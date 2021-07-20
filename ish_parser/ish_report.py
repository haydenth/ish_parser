from datetime import datetime, timedelta
import logging
import pytz

from .Temperature import Temperature
from .Speed import Speed
from .Units import Units
from .Distance import Distance
from .Humidity import Humidity
from .ReportType import ReportType
from .Pressure import Pressure
from .Direction import Direction
from .Components import *

class ish_reportException(BaseException):
  ''' handler class for exceptions '''


class ish_report(object):
  ''' This is the class which can parse a SINGLE NOAA weather 
  report. It first reads the mandatory data elements, storing them
  as attributes. It then parses the additional data elements and makes
  those methods available via magic methods '''

  RECORD_DELIMITER = "\n"
  PREAMBLE_LENGTH = 105
  TEMPERATURE_SCALE = 10.0
  PRESSURE_SCALE = 10.0
  SPEED_SCALE = 10
  ADDR_CODE_LENGTH = 3
  GEO_SCALE = 1000
  MISSING = '9999'
  MAP = {'AA1': ['LIQUID-PRECIP', 8, PrecipitationComponent],
         'AA2': ['LIQUID-PRECIP', 8, PrecipitationComponent],
         'AA3': ['LIQUID-PRECIP', 8, PrecipitationComponent],
         'AA4': ['LIQUID-PRECIP', 8, PrecipitationComponent],
         'AB1': ['LIQUID-PRECIP-MONTHLY', 7],
         'AC1': ['PRECIPITATION-OBSERVATION-HISTORY', 3],
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
         'AT1': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT2': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT3': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT4': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT5': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT6': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT7': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AT8': ['DAILY-PRESENT-WEATHER-OBSERVATION', 9],
         'AU1': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU2': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU3': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU4': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU5': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU6': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU7': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU8': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AU9': ['WEATHER-OCCURANCE', 8, PresentWeatherComponent],
         'AW1': ['PRESENT-WEATHER-OBSERVATION', 3, PresentWeatherConditionComponent],
         'AW2': ['PRESENT-WEATHER-OBSERVATION', 3, PresentWeatherConditionComponent],
         'AW3': ['PRESENT-WEATHER-OBSERVATION', 3, PresentWeatherConditionComponent],
         'AW4': ['PRESENT-WEATHER-OBSERVATION', 3, PresentWeatherConditionComponent],
         'AW5': ['PRESENT-WEATHER-OBSERVATION', 3, PresentWeatherConditionComponent],
         'AW6': ['PRESENT-WEATHER-OBSERVATION', 3, PresentWeatherConditionComponent],
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
         'CN4': ['SECONDARY-HOURLY-DIAGNOSTIC', 19],
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
         'GA1': ['SKY-COVER-LAYER', 13, SkyCoverComponent],
         'GA2': ['SKY-COVER-LAYER', 13, SkyCoverComponent],
         'GA3': ['SKY-COVER-LAYER', 13, SkyCoverComponent],
         'GA4': ['SKY-COVER-LAYER', 13, SkyCoverComponent],
         'GA5': ['SKY-COVER-LAYER', 13, SkyCoverComponent],
         'GA6': ['SKY-COVER-LAYER', 13, SkyCoverComponent],
         'GD1': ['SKY-COVER-SUMMATION', 12, SkyCoverSummationComponent],
         'GD2': ['SKY-COVER-SUMMATION', 12, SkyCoverSummationComponent],
         'GD3': ['SKY-COVER-SUMMATION', 12, SkyCoverSummationComponent],
         'GD4': ['SKY-COVER-SUMMATION', 12, SkyCoverSummationComponent],
         'GD5': ['SKY-COVER-SUMMATION', 12, SkyCoverSummationComponent],
         'GD6': ['SKY-COVER-SUMMATION', 12, SkyCoverSummationComponent],
         'GE1': ['SKY-CONDITION', 19],
         'GF1': ['SKY-CONDITION', 23, SkyConditionObservationComponent],
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
         'GM1': ['SOLAR-IRRADIANCE', 30, SolarIrradianceComponent],
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
         'MA1': ['ATMOSPHERIC-PRESSURE', 12, PressureComponent],
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
         'MW8': ['PRESENT-WEATHER-OBS', 3],
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
         'REM': ['REMARKS', False],
         'EQD': ['ELEMENT QUALITY', 16],
         'NO1': ['ORIGINAL-OBSERVATION', 13],
         'OA1': ['SUPPLEMENTARY-WIND-OBSERVATION', 8],
         'OA2': ['SUPPLEMENTARY-WIND-OBSERVATION', 8],
         'OA3': ['SUPPLEMENTARY-WIND-OBSERVATION', 8],
         'OB1': ['HOURLY-SUBHOURLY-WIND', 28],
         'OB2': ['HOURLY-SUBHOURLY-WIND', 28],
         'OC1': ['WIND-GUST-OBSERVATION', 5],
         'OD1': ['SUPPLEMENTARY-WIND-OBSERVATION', 11],
         'OD2': ['SUPPLEMENTARY-WIND-OBSERVATION', 11],
         'OD3': ['SUPPLEMENTARY-WIND-OBSERVATION', 11],
         'OE1': ['SUMMARY-OF-DAY-WIND', 16],
         'OE2': ['SUMMARY-OF-DAY-WIND', 16],
         'OE3': ['SUMMARY-OF-DAY-WIND', 16],
         'QNN': ['ORIGINAL-OBSERVATION-NCDC', 999],
         'R01': ['ORIGINATED_NCDC_DATA', 13],
         'R02': ['ORIGINATED_NCDC_DATA', 13],
         'R03': ['ORIGINATED_NCDC_DATA', 13],
         'R04': ['ORIGINATED_NCDC_DATA', 13],
         'R05': ['ORIGINATED_NCDC_DATA', 13],
         'R06': ['ORIGINATED_NCDC_DATA', 13],
         'R07': ['ORIGINATED_NCDC_DATA', 13],
         'R08': ['ORIGINATED_NCDC_DATA', 13],
         'R09': ['ORIGINATED_NCDC_DATA', 13],
         'R10': ['ORIGINATED_NCDC_DATA', 13],
         'R11': ['ORIGINATED_NCDC_DATA', 13],
         'R12': ['ORIGINATED_NCDC_DATA', 13],
         'R13': ['ORIGINATED_NCDC_DATA', 13],
         'R14': ['ORIGINATED_NCDC_DATA', 13],
         'R15': ['ORIGINATED_NCDC_DATA', 13],
         'R16': ['ORIGINATED_NCDC_DATA', 13],
         'R17': ['ORIGINATED_NCDC_DATA', 13],
         'R18': ['ORIGINATED_NCDC_DATA', 13],
         'R19': ['ORIGINATED_NCDC_DATA', 13],
         'R20': ['ORIGINATED_NCDC_DATA', 13],
         'R21': ['ORIGINATED_NCDC_DATA', 13],
         'R22': ['ORIGINATED_NCDC_DATA', 13],
         'R23': ['ORIGINATED_NCDC_DATA', 13],
         'R24': ['ORIGINATED_NCDC_DATA', 13],
         'RH1': ['RELATIVE-HUMIDITY', 9],
         'RH2': ['RELATIVE-HUMIDITY', 9],
         'RH3': ['RELATIVE-HUMIDITY', 9],
         'SA1': ['SEA-SURFACE-TEMPERATURE', 5],
         'ST1': ['SOIL-TEMPERATURE', 17],
         'UA1': ['WAVE-MEASUREMENT', 10],
         'UG1': ['WAVE-MEASUREMENT-SWELL', 9],
         'UG2': ['WAVE-MEASUREMENT-SECONDARY-SWELL', 9],
         'WA1': ['PLATFORM-ICE-ACCRETION', 6],
         'WD1': ['WATER-SURFACE-ICE', 20],
         'WG1': ['WATER_SURFACE-ICE-HISTORICAL', 11],
         'WJ1': ['WATER-LEVEL-OBSERVATION', 19]}

  def __init__(self):
    self._additional = {}
    self._remarks = {}

  def __getattr__(self, attribute_name):
    values_to_return = []
    for (addl_code, addl) in self._additional.items():
      try:
        addl_value = getattr(addl, attribute_name)
        values_to_return.append(addl_value)
      except:
        pass

    if len(values_to_return) > 0:
      return values_to_return

  def formatted(self):
    ''' print a nicely formatted output of this report '''

    return """
Weather Station: %s (%s, %s)
Elevation: %s m
Time: %s UTC
Air Temperature: %s C (%s F)
Wind Speed: %s m/s (%s mph)
Wind Direction: %s
Present Weather Obs: %s
Precipitation: %s
Cloud Coverage: %s oktas
Cloud Summation: %s
Solar Irradiance: %s 
    """ % (self.weather_station, self.latitude, self.longitude,
           self.elevation, self.datetime, self.air_temperature,
           self.air_temperature.get_fahrenheit(), self.wind_speed,
           self.wind_speed.get_MilesPerHour(), self.wind_direction,
           str(self.present_weather), str(self.precipitation),
           str(self.sky_cover), str(self.sky_cover_summation),
           str(self.solar_irradiance))

  def loads(self, noaa_string):
    ''' load in a report (or set) from a string '''
    self.raw = noaa_string
    self.weather_station = noaa_string[4:10]
    self.wban = noaa_string[10:15]
    expected_length = int(noaa_string[0:4]) + self.PREAMBLE_LENGTH
    actual_length = len(noaa_string)
    if actual_length != expected_length:
      msg = "Non matching lengths. Expected %d, got %d" % (expected_length,
                                                           actual_length)
      raise ish_reportException(msg)

    try:
      self.datetime = datetime.strptime(noaa_string[15:27], '%Y%m%d%H%M')
    except ValueError:
      ''' some cases, we get 2400 hours, which is really the next day, so 
      this is a workaround for those cases '''
      time = noaa_string[15:27]
      time = time.replace("2400", "2300")
      self.datetime = datetime.strptime(time, '%Y%m%d%H%M')
      self.datetime += timedelta(hours=1)

    self.datetime = self.datetime.replace(tzinfo=pytz.UTC)

    self.report_type = ReportType(noaa_string[41:46].strip())

    self.latitude = float(noaa_string[28:34]) / self.GEO_SCALE
    self.longitude = float(noaa_string[34:41]) / self.GEO_SCALE
    self.elevation = int(noaa_string[46:51])

    ''' other mandatory fields '''
    self.wind_direction = Direction(noaa_string[60:63],
                                    Direction.RADIANS,
                                    noaa_string[63:64])
    self.wind_observation_direction_type = noaa_string[64:64]
    self.wind_speed = Speed(int(noaa_string[65:69]) / float(self.SPEED_SCALE),
                            Speed.METERSPERSECOND,
                            noaa_string[69:70])
    self.sky_ceiling = Distance(int(noaa_string[70:75]),
                                Distance.METERS,
                                noaa_string[75:76])
    self.sky_ceiling_determination = noaa_string[76:77]
    self.visibility_distance = Distance(int(noaa_string[78:84]),
                                        Distance.METERS,
                                        noaa_string[84:85]) 
    self.visibility_variability = noaa_string[85:86]
    self.visibility_variability_quality = noaa_string[86:87]

    self.air_temperature = Temperature(int(noaa_string[87:92]) / self.TEMPERATURE_SCALE,
                                           Units.CELSIUS,
                                           noaa_string[92:93])
    self.dew_point = Temperature(int(noaa_string[93:98]) / self.TEMPERATURE_SCALE,
                                 Units.CELSIUS,
                                 noaa_string[98:99])

    self.humidity = Humidity(str(self.air_temperature), str(self.dew_point))
    self.sea_level_pressure = Pressure(int(noaa_string[99:104])/self.PRESSURE_SCALE,
                                       Pressure.HECTOPASCALS,
                                       noaa_string[104:104])

    ''' handle the additional fields '''
    additional = noaa_string[105:108]
    if additional == 'ADD':
      position = 108
      while position < expected_length:
        try:
          (position, (addl_code, addl_string)) = self._get_component(noaa_string,
                                                                     position)
          self._additional[addl_code] = addl_string
        except ish_reportException as err:
          ''' this catches when we move to remarks section '''
          break

    ''' handle the remarks section if it exists '''
    try:
      position = noaa_string.index('REM', 108) 
      self._get_remarks_component(noaa_string, position)
    except (ish_reportException, ValueError) as err:
      ''' this catches when we move to EQD section '''

    return self

  def _get_remarks_component(self, string, initial_pos):
    ''' Parse the remarks into the _remarks dict '''
    remarks_code = string[initial_pos:initial_pos + self.ADDR_CODE_LENGTH]
    if remarks_code != 'REM':
      raise ish_reportException("Parsing remarks. Expected REM but got %s." % (remarks_code,))

    expected_length = int(string[0:4]) + self.PREAMBLE_LENGTH
    position = initial_pos + self.ADDR_CODE_LENGTH
    while position < expected_length:
      key = string[position:position + self.ADDR_CODE_LENGTH]
      if key == 'EQD':
        break
      chars_to_read = string[position + self.ADDR_CODE_LENGTH:position + \
                      (self.ADDR_CODE_LENGTH * 2)]
      chars_to_read = int(chars_to_read)
      position += (self.ADDR_CODE_LENGTH * 2)
      string_value = string[position:position + chars_to_read]
      self._remarks[key] = string_value
      position += chars_to_read

  def _get_component(self, string, initial_pos):
    ''' given a string and a position, return both an updated position and
    either a Component Object or a String back to the caller '''
    add_code = string[initial_pos:initial_pos + self.ADDR_CODE_LENGTH]
    
    if add_code == 'REM':
      raise ish_reportException("This is a remarks record")
    if add_code == 'EQD':
      raise ish_reportException("This is EQD record")

    initial_pos += self.ADDR_CODE_LENGTH 
    try:
      useable_map = self.MAP[add_code]
    except:
      raise BaseException("Cannot find code %s in string %s (%d)." % (add_code, string, initial_pos))

    # if there is no defined length, then read next three chars to get it
    # this only applies to REM types, which have 3 chars for the type, then variable
    if useable_map[1] is False:
      chars_to_read = string[initial_pos + self.ADDR_CODE_LENGTH:initial_pos + \
                      (self.ADDR_CODE_LENGTH * 2)]
      chars_to_read = int(chars_to_read)
      initial_pos += (self.ADDR_CODE_LENGTH * 2)
    else:
      chars_to_read = useable_map[1]

    new_position = initial_pos + chars_to_read
    string_value = string[initial_pos:new_position]

    try:
      object_value = useable_map[2]()
      object_value.loads(string_value)
    except IndexError as err:
      object_value = string_value

    return (new_position, [add_code, object_value])

  def remarks(self):
    return self._remarks

  def get_additional_field(self, addl_code):
    ''' Given an additional field code (AA1, AJ1..), return whatever match
    we have available for this code '''
    return self._additional[addl_code]

  def additional(self):
    ''' return the entire additional dictionary '''
    return self._additional
