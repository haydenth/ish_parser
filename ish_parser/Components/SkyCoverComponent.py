from ..Distance import Distance
from ..CloudCoverage import CloudCoverage
from ..Constant import Constant
from .BaseComponent import BaseComponent

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
    self.sky_cover = {
      'coverage': CloudCoverage(string[0:2],
        CloudCoverage.OKTA, string[2:3]),
      'base_height': Distance(int(string[4:9]),
        Distance.METERS, string[9:10]),
      'cloud_type': Constant(string[9:11], None, 
        string[11:12], self.CLOUD_TYPES)}

  def __repr__(self):
    return str(self.sky_cover)

  def __str__(self):
    return str(self.sky_cover)
