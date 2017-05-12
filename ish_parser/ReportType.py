from .Observation import Observation


class ReportType(Observation):
  MAP = {'AERO': 'Aerological report',
         'AUST': 'Dataset from Australia',
         'AUTO': 'Report from an automatic station',
         'BOGUS': 'Bogus Report',
         'BRAZ': 'Dataset from Brazil',
         'COOPD': 'US Cooperative Network summary of day report',
         'COOPS': 'US Cooperative Network soil temperature report',
         'CRB': 'Climate Reference Book data from CDMP',
         'CRN05': 'Climate Reference Network report, with 5-minute reporting interval',
         'CRN15': 'Climate Reference Network report, with 15-minute reporting interval',
         'FM-12': 'SYNOP Report of surface observation form a fixed land station',
         'FM-13': 'SHIP Report of surface observation from a sea station',
         'FM-14': 'SYNOP MOBIL Report of surface observation from a mobile land station',
         'FM-15': 'METAR Aviation routine weather report',
         'FM-16': 'SPECI Aviation selected special weather report',
         'FM-18': 'BUOY Report of a buoy observation',
         'GREEN': 'Dataset from Greenland',
         'MESOS': 'MESONET operated civilian or government agency',
         'MEXIC': 'Dataset from Mexico',
         'NSRDB': 'National Solar Radiation Data Base',
         'PCP15': 'US 15-minute precipitation network report',
         'PCP60': 'US 60-minute precipitation network report',
         'S-S-A': 'Synoptic, airways, and auto merged report',
         'SA-AU': 'Airways and auto merged report',
         'SAO': 'Airways report (includes record specials)',
         'SAOSP': 'Airways special report (excluding record specials)',
         'SHEF': 'Standard Hydrologic Exchange Format', 
         'SMARS': 'Supplementary airways station report', 
         'SOD': 'Summary of day report from U.S. ASOS or AWOS station',
         'SOM': 'Summary of month report from U.S. ASOS or AWOS station', 
         'SURF': 'Surface Radiation Network report',
         'SY-AE': 'Synoptic and aero merged report',
         'SY-AU': 'Synoptic and auto merged report',
         'SY-MT': 'Synoptic and METAR merged report',
         'SY-SA': 'Synoptic and airways merged report', 
         'WBO': 'Weather Bureau Office',
         'WNO': 'Washington Naval Observatory',
         '99999': 'Missing'}

  def __str__(self):
    return self.MAP[self._obs_value]

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other_value):
    if self._obs_value == other_value:
      return True
    elif self.MAP[self._obs_value] == other_value:
      return True
    else:
      return False
