from .BaseComponent import BaseComponent

class PresentWeatherComponent(BaseComponent):
  ''' handle any AU Type'''
  INTENSITY = {
    '0': '',
    '1': 'Light',
    '2': 'Moderate',
    '3': 'Heavy',
    '4': 'Vicinity',
    '5': 'MISSING'
  }
  DESCRIPTOR = {
    '0': '',
    '1': 'Shallow',
    '2': 'Partial',
    '3': 'Patches',
    '4': 'Low Drifting',
    '5': 'Blowing',
    '6': 'Showers',
    '7': 'Thunderstorm',
    '8': 'Freezing',
    '9': 'MISSING'
  }
  PRECIP = {
    '00': '',
    '01': 'Drizzle',
    '02': 'Rain',
    '03': 'Snow',
    '04': 'Snow Grains',
    '05': 'Ice Crystals',
    '06': 'Ice Pellets',
    '07': 'Hail',
    '08': 'Small Hail',
    '09': 'Unknown Precip'
  }
  OBSCURATION = {
    '0': '',
    '1': 'Mist',
    '2': 'Fog',
    '3': 'Smoke',
    '4': 'Volcanic Ash',
    '5': 'Widespread Dust',
    '6': 'Sand',
    '7': 'Haze',
    '8': 'Spray',
    '9': 'MISSING'
  }
  def loads(self, string):
    self.present_weather_array = {'intensity': self.INTENSITY[string[0:1]],
                                  'descriptor': self.DESCRIPTOR[string[1:2]],
                                  'precipitation': self.PRECIP[string[2:4]],
                                  'obscuration': self.PRECIP[string[4:5]]}
    present = self.present_weather_array
    try:
      ', '.join([present_weather_array[r] for r in present_weather_array if present_weather_array[r]])
    except:
      self.present_weather = ""
