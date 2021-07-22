from ..Speed import Speed
from ..Direction import Direction
from .BaseComponent import BaseComponent


class WindObservationComponent(BaseComponent):
  ''' handle OD1/OD2/OD3 Additional Wind observation types '''
  WIND_OBSERVATION_TYPES = {
    '1': 'Average speed of prevailing wind',
    '2': 'Mean wind speed',
    '3': 'Maximum instantaneous wind speed',
    '4': 'Maximum gust speed',
    '5': 'Maximum mean wind speed',
    '6': 'Maximum 1 - minute mean wind speed',
    '9': 'Missing'
  }

  def loads(self, string):
    self.wind_observation = {
      'type': self.WIND_OBSERVATION_TYPES[string[0:1]],
      'hours': int(string[1:3]),
      'speed': Speed(float(string[3:7]) / 10.0, Speed.METERSPERSECOND, string[7:8]),
      'direction': Direction(string[8:11], Direction.RADIANS)
    }
