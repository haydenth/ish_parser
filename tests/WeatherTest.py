import unittest
import datetime
from src.WeatherReport import WeatherReport, WeatherReportException

class WeatherTest(unittest.TestCase):

  def test_single_reading(self):
    noaa_string = """0243725300948462014010101087+41995-087934FM-16+0205KORD V0302905N00155004575MN0020125N5-01115-01445999999ADDAA101000231AU110030015AW1715GA1085+004575991GD14991+0045759GE19MSL   +99999+99999GF199999990990004571991991MA1102615100145REMMET10912/31/13 19:08:03 SPECI KORD 010108Z 29003KT 1 1/4SM -SN OVC015 M11/M14 A3030 RMK AO2 P0001 T11111144 $ (KLC)"""
    weather = WeatherReport()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(2014, 01, 01))
    self.assertEquals(weather.wban, '94846')
    self.assertEquals(weather.weather_station, '725300')
    self.assertEquals(weather.report_type, 'FM-16')
    self.assertEquals(weather.latitude, 41.995)
    self.assertEquals(weather.longitude, -87.934)
    self.assertEquals(weather.visibility_distance, 2012)
    self.assertEquals(weather.air_temperature, -12)

  def test_fm15(self):
    noaa_string = """0250725300948462014010100517+41995-087934FM-15+0205KORD V0302505N00155005795MN0024145N5-01115-01445102735ADDAA101000895AU110030015AW1715GA1085+005795991GD14991+0057959GE19MSL   +99999+99999GF199999990990005791991991MA1102575100115REMMET11612/31/13 18:51:03 METAR KORD 010051Z 25003KT 1 1/2SM -SN OVC019 M11/M14 A3029 RMK AO2 SLP273 P0003 T11111144 $ (KLC)"""
    weather = WeatherReport()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(2014, 01, 01))
    self.assertEquals(weather.wban, '94846')
    self.assertEquals(weather.weather_station, '725300')
    self.assertEquals(weather.report_type, 'FM-15')
    self.assertEquals(weather.elevation, 205)
    self.assertEquals(weather.wind_speed, 15)
    self.assertEquals(weather.sky_ceiling, 579)
    self.assertEquals(weather.air_temperature, -12)
    self.assertEquals(weather.air_temperature.get_fahrenheit(), 10.4)
    self.assertEquals(weather.sea_level_pressure, 10273)

  def test_austin(self):
    string = """0190722540139042014042819537+30183-097680FM-15+0151KAUS V0203505N004152200059N0160935N5+03175+00065100325ADDAA101000095GA1005+999999999GD10991+9999999GF100991999999999999999999MA1100445098655REMMET09504/28/14 13:53:02 METAR KAUS 281953Z 35008KT 10SM CLR 32/01 A2966 RMK AO2 SLP032 T03170006 (JP)"""
    weather = WeatherReport()
    weather.loads(string)
    print weather.additional()

  def test_snowfall(self):
    string = """0479725300948462014010105517+41995-087934FM-15+0205KORD V0300105N00465007015MN0028165N5-01225-01565102655ADDAA101001095AA206005691AJ100089500007694AU110030015AW1715GA1075+007015991GA2075+011285991GA3085+016765991GD13991+0070159GD23991+0112859GD34991+0167659GE19MSL   +99999+99999GF199999990990007011991991KA1060M-01111KA2060N-01221KA3240M-01111KA4240N-01671MA1102515100045MD1690154+9999REMMET17012/31/13 23:51:03 METAR KORD 010551Z 01009KT 1 3/4SM -SN BKN023 BKN037 OVC055 M12/M16 A3027 RMK AO2 SLP265 4/003 P0005 60022 T11221156 11111 21122 411111167 56015 $ (SMN)EQDQ01  00558PRCP06"""
    weather = WeatherReport()
    weather.loads(string)
    self.assertEquals(weather.datetime.date(), datetime.date(2014, 01, 01))
    print weather.additional()
    self.assertEquals(weather.snow_depth, 8)
    #self.assertEquals(weather.present_weather_observation, 'Snow, Slight')

  def test_bad_length(self):
    noaa_string = """1243725300948462014010101087+41995-087934FM-16+0205KORD V0302905N00155004575MN0020125N5-01115-01445999999ADDAA101000231AU110030015AW1715GA1085+004575991GD14991+0045759GE19MSL   +99999+99999GF199999990990004571991991MA1102615100145REMMET10912/31/13 19:08:03 SPECI KORD 010108Z 29003KT 1 1/4SM -SN OVC015 M11/M14 A3030 RMK AO2 P0001 T11111144 $ (KLC)"""
    self.assertRaises(WeatherReportException, 
                      WeatherReport().loads, noaa_string)
