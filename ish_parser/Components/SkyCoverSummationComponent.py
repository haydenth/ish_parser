from ..Distance import Distance
from ..CloudCoverage import CloudCoverage
from ..Constant import Constant
from .BaseComponent import BaseComponent

class SkyCoverSummationComponent(BaseComponent):
  ''' handle GD1 .. GD8 component types '''

  CLOUD_TYPES = {
    "0": "Clear - No coverage",
    "1": "FEW - 2/8 or less coverage (not including zero)",
    "2": "SCATTERED - 3/8-4/8 coverage",
    "3": "BROKEN - 5/8-7/8 coverage",
    "4": "OVERCAST - 8/8 coverage",
    "5": "OBSCURED",
    "6": "PARTIALLY OBSCURED",
    "9": "MISSING"}
  CLOUD_TYPES_SIMPLE = {
    "0": "Clear",
    "1": "Partly Cloudy",
    "2": "Scattered Clouds",
    "3": "Mostly Cloudy",
    "4": "Overcast",
    "5": "",
    "6": "",
    "9": "MISSING"}
  SECONDARY_TYPES = {
    "00": "None, SKC or CLR",
    "01": "One okta - 1/10 or less but not zero",
    "02": "Two oktas - 2/10 - 3/10, or FEW",
    "03": "Three oktas - 4/10",
    "04": "Four oktas - 5/10, or SCT",
    "05": "Five oktas - 6/10",
    "06": "Six oktas - 7/10 - 8/10",
    "07": "Seven oktas - 9/10 or more but not 10/10, or BKN",
    "08": "Eight oktas - 10/10, or OVC",
    "09": "Sky obscured, or cloud amount cannot be estimated",
    "10": "Partial Obscuration",
    "11": "Thin Scattered",
    "12": "Scattered",
    "13": "Dark Scattered",
    "14": "Thin Broken",
    "15": "Broken",
    "16": "Dark Broken",
    "17": "Thin Overcast",
    "18": "Overcast",
    "19": "Dark overcast",
    "99": "Missing"}
  CHARACTERISTIC = {
    "1": "Variable height",
    "2": "Variable amount",
    "3": "Thin clouds",
    "4": "Dark layer (reported in data prior to 1950)",
    "9": "Missing"}

  def loads(self, string):

    self.sky_cover_summation  = {
      'coverage': Constant(string[0:1], None,
        string[3:4], self.CLOUD_TYPES),
      'coverage_simple': Constant(string[0:1], None,
        string[3:4], self.CLOUD_TYPES_SIMPLE),
      'secondary_coverage': Constant(string[1:3], None,
        string[3:4], self.SECONDARY_TYPES),
      'height': Distance(int(string[4:10]),
        Distance.METERS, string[10:11]),
      'characteristic': Constant(string[11:12], None, 
        None, self.CHARACTERISTIC)}

  def __str__(self):
    return str(self.sky_cover_summation)

  def __repr__(self):
    return str(self.sky_cover_summation)
