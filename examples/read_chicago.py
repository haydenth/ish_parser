import csv
from src.WeatherFile import WeatherFile

file = '725300.txt'
output = 'results.csv'

output_fh = open(output, 'wb')
csvwriter = csv.DictWriter(output_fh, ['type', 'datetime', 'temperature'])

with open(file) as fp:
  content = fp.read()
wf = WeatherFile()
wf.loads(content)
for report in wf.get_observations():
  if report.air_temperature.get_fahrenheit() != 'MISSING':
    csvwriter.writerow({'type': report.report_type, 'datetime': report.datetime.isoformat(), 
                        'temperature': report.air_temperature.get_fahrenheit()})
