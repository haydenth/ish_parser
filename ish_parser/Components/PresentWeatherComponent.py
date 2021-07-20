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
  EVENT_DESCRIPTOR = {
    '0': '',
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': '',
    '6': 'Showers',
    '7': 'Thunderstorm',
    '8': 'Freezing',
    '9': ''
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
    self.present_weather_array = {
      'intensity': self.INTENSITY[string[0:1]],
      'descriptor': self.DESCRIPTOR[string[1:2]],
      'precipitation': self.PRECIP[string[2:4]],
      'obscuration': self.OBSCURATION[string[4:5]]
      }
    self.present_weather_event_array =  {
      'descriptor': self.EVENT_DESCRIPTOR[string[1:2]],
      'precipitation': self.PRECIP[string[2:4]],
      'obscuration': self.OBSCURATION[string[4:5]]
      }
      
    present = [
      self.INTENSITY[string[0:1]],
      self.DESCRIPTOR[string[1:2]],
      self.PRECIP[string[2:4]],
      self.OBSCURATION[string[4:5]]
      ]
    present_event = [
      self.EVENT_DESCRIPTOR[string[1:2]],
      self.PRECIP[string[2:4]],
      self.OBSCURATION[string[4:5]]
      ]

    try:
      self.present_weather = ' '.join([r for r in present if r])
      self.present_weather_event = ' '.join([r for r in present_event if r])
    except:
      self.present_weather = ""
      self.present_weather_event = ""

  def __repr__(self):
    return str({'present_weather': self.present_weather, 'present_weather_event': self.present_weather_event})

  def __str__(self):
    return str({'present_weather': self.present_weather, 'present_weather_event': self.present_weather_event})

