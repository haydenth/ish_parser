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
Suppose you want to get all the hourly weather observations for a single airport, say O'Hare (ORD) for 2013. First, you need to figure out the weather station ID for O'hare. You can find it in this file:
http://www1.ncdc.noaa.gov/pub/data/noaa/ish-history.txt

You'll see a row:
725300 94846 CHICAGO/O HARE ARPT           US US IL KORD  +41995 -087934 +02054    19461001 20140313

The airport code is 725300. 

Developing
--------------------------------
If you make some code changes (yay) please write the appropriate tests and run all unittests before sending pull request.  You can do this with
```
python -m unittest tests
```

Contact
--------------------------------
For questions, contact Tom Hayden (thayden@gmail.com)
