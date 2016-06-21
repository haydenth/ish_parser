NOAA ISH Weather Parser Library
--------------------------------
It's surprisingly hard to find accurate raw weather data that hasn't already been parsed by some third party and is free. Fortunately, the NOAA puts out a daily/weekly/yearly feed of raw weather data for thousands of weather stations. It's in a format called ISH (integrated surface reporting hourly). There is also a daily format as well. The format is tricky and has hundreds of delimters and variable length text fields. It's tricky to parse. Full documentation is available from the NOAA:
http://www1.ncdc.noaa.gov/pub/data/ish/ish-format-document.pdf

The file itself consists of a:
* Mandatory section: temperature, location, windspeed
* Additional Optional Data Elements: Snow Depth, Precipritation, things like that
* Remarks: Usually a METAR or something crazy
* Element Quality Section

The files themselves are available on the NOAA's FTP site, stored in an annual set of folders, keyed by weather station id. You can find them at this location:
http://www1.ncdc.noaa.gov/pub/data/noaa/

This python module is an attempt to be able to parse it as best as possible.

Simple Example
--------------------------------
Suppose you want to get all the hourly weather observations for a single airport, say O'Hare (ORD) for 2014. First, you need to figure out the weather station ID for O'hare. You can find it in this file:
ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-history.txt

You'll see a row:
725300 94846 CHICAGO/O HARE ARPT           US US IL KORD  +41995 -087934 +02054    19461001 20140313

The airport code is 725300. Now that you've got this, go to another spot in the NOAA FTP or www1 server to pull down the actual gzipped report for the year. In the case of O'Hare, you can find it at:

ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2014/725300-94846-2014.gz

If you uncompress, you'll find a ton of data in the file. In the case of O'hare and 2014, they log data at least every hour if not more frequently. For instance, the data is lines and lines that look like this:

```
0317725300948462014010506397+41995-087934FM-16+0205KORD V0303605N00465002135MN0012075N5-00285-00505999999ADDAA101001031AU110030015AU200001015AW1105AW2715GA1075+002135991GA2085+003665991GD13991+0021359GD24991+0036659GE19MSL   +99999+99999GF199999990990002131991991MA1101525099085REMMET13501/05/14 00:39:02 SPECI KORD 050639Z 36009KT 3/4SM R10L/5500VP6000FT -SN BR BKN007 OVC012 M03/M05 A2998 RMK AO2 P0004 T10281050 $ (MJF)
0324725300948462014010506517+41995-087934FM-15+0205KORD V0303605N00675002135MN0012075N5-00335-00565101625ADDAA101001895AU110030015AU200001015AW1105AW2715GA1075+002135991GA2085+003665991GD13991+0021359GD24991+0036659GE19MSL   +99999+99999GF199999990990002131991991MA1101565099115REMMET14201/05/14 00:51:02 METAR KORD 050651Z 36013KT 3/4SM R10L/5000VP6000FT -SN BR BKN007 OVC012 M03/M06 A2999 RMK AO2 SLP162 P0006 T10331056 $ (MJF)
0296725300948462014010507297+41995-087934FM-16+0205KORD V0303505N00625003355MN0012075N5-00445-00725999999ADDAA101001031AU110030015AW1715GA1025+002135991GA2085+003355991GD11991+0021359GD24991+0033559GE19MSL   +99999+99999GF199999990990002131991991MA1101595099155REMMET13101/05/14 01:29:02 SPECI KORD 050729Z 35012KT 3/4SM R10L/5000V5500FT -SN FEW007 OVC011 M04/M07 A3000 RMK AO2 P0004 T10441072 $ (MJF)
0297725300948462014010507517+41995-087934FM-15+0205KORD V0303505N00515003665WN0012075N5-00505-00725101675ADDAA101001395AU110030015AU200001015AW1105AW2715GA1095+003665991GD15991+0036659GE19MSL   +99999+99999GF109991990990003661991991MA1101595099155REMMET14601/05/14 01:51:02 METAR KORD 050751Z 35010KT 3/4SM R10L/6000VP6000FT -SN BR VV012 M05/M07 A3000 RMK AO2 SLP167 SNINCR 1/10 P0005 T10501072 $ (MJF)
0281725300948462014010508237+41995-087934FM-16+0205KORD V0303505N00625005795MN0020125N5-00565-00835999999ADDAA101000531AU110030015AW1715GA1025+003355991GA2085+005795991GD11991+0033559GD24991+0057959GE19MSL   +99999+99999GF199999990990003351991991MA1101665099215REMMET11601/05/14 02:23:02 SPECI KORD 050823Z 35012KT 1 1/4SM -SN FEW011 OVC019 M06/M08 A3002 RMK AO2 P0002 T10561083 $ (MJF)
```

There is a TON of data encoded in these records in a very strange weird way. This module does its best to parse out this crazyness. Here's an example:

```
>>> import ish_parser
>>> from src import ish_report
>>> rpt = ish_report().loads("""0281725300948462014010508237+41995-087934FM-16+0205KORD V0303505N00625005795MN0020125N5-00565-00835999999ADDAA101000531AU110030015AW1715GA1025+003355991GA2085+005795991GD11991+0033559GD24991+0057959GE19MSL   +99999+99999GF199999990990003351991991MA1101665099215REMMET11601/05/14 02:23:02 SPECI KORD 050823Z 35012KT 1 1/4SM -SN FEW011 OVC019 M06/M08 A3002 RMK AO2 P0002 T10561083 $ (MJF)""")
>>> print rpt
<src.ish_report.ish_report object at 0x7f9ba29cb8d0>
>>> print rpt.formatted()
Weather Station: 725300 (41.995, -87.934)
Elevation: 205 m
Time: 2014-01-05 08:23:00 UTC
Air Temperature: -6 C (21.2 F)
Wind Speed: 6.2 m/s (13.869 mph)
Wind Direction: 350
```

Installing
-------------------------------
The current stable version is available on pip. If you're a python and pip user, you can install the current development version with:

```
sudo pip install git+https://github.com/haydenth/ish_parser.git
```

If you'd like to install the current stable version (will most certainly be behind the development version). You can just use the regular pip repository:
```
sudo pip install ish_parser
```

Using
------------------------------
Using the module should be pretty straightforward. Here's an example from one of the unittests:

```
SOMEFILE = 'path/to/a/ish/file'

# read the file
with open(SOMEFILE) as fp:
  content = fp.read()
fp.close()

wf = ish_parser()
wf.loads(content)

# get the list of all reports
reports = wf.get_reports()
print len(reports)

# look at just one report
report = reports[23]
print report.air_temperature.get_fahrenheit()
print report.air_temperature

# see all the other options for this report
print dir(report)
```

Developing
--------------------------------
If you make some code changes (yay) please write the appropriate tests and run all unittests before sending pull request.  You can do this with
```
python -m unittest tests
```

Contact
--------------------------------
For questions, contact Tom Hayden (thayden@gmail.com)
