import logging
from .ish_report import ish_report

class ish_parser(object):
  ''' primary object for parsing ish files, this class is
  primarily responsible for opening a file, splitting it
  and handing off each line to ish_report, which process
  the specific ish report '''

  OBS_TYPES = ['FM-12', 'FM-15', 'SAO']

  def __init__(self):
    self._reports = []

  def loads(self, string):
    ''' load from a string '''
    for line in string.split("\n"):
      if len(line) < 10:
        continue

      try:
        report = ish_report()
        report.loads(line)
        self._reports.append(report)
      except BaseException as exp:
        ''' don't complain TOO much '''
        logging.warning('unable to load report, error: %s' % exp)

  def get_reports(self):
    ''' return a list of all the reports '''
    return self._reports

  def get_observations(self):
    ''' return only specific weather observations (FM types) and
    ignore the summary of day reports '''
    return [rpt for rpt in self._reports if rpt.report_type in self.OBS_TYPES]
