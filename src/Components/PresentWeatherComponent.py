from .BaseComponent import BaseComponent

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
