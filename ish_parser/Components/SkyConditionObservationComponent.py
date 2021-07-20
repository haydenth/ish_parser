from ..CloudCoverage import CloudCoverage
from .BaseComponent import BaseComponent

class SkyConditionObservationComponent(BaseComponent):
  ''' handler for GF1 data type '''

  def loads(self, string):
    self.sky_condition_observation = {'total_coverage': CloudCoverage(string[0:2],
                                                        CloudCoverage.OKTA, string[3:4]),
                                      'total_lowest_coverage': CloudCoverage(string[5:7],
                                                               CloudCoverage.OKTA, string[7:8])}

  def __repr__(self):
    return str(self.sky_condition_observation)

  def __str__(self):
    return str(self.sky_condition_observation)
