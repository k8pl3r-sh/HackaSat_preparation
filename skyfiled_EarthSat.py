from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite

stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
print('Loaded', len(satellites), 'satellites')

# by name
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
print(satellite)

# by number
by_number = {sat.model.satnum: sat for sat in satellites}
satellite = by_number[25544]
print(satellite)


# TLE Querying

# Warning: specify reload=True or filename= an other name

n = 25544
url = 'https://celestrak.com/satcat/tle.php?CATNR={}'.format(n)
filename = 'tle-CATNR-{}.txt'.format(n)
satellites = load.tle_file(url, filename=filename)
print(satellites)

# TO load a TLE string already get
ts = load.timescale()
line1 = '1 25544U 98067A   14020.93268519  .00009878  00000-0  18200-3 0  5082'
line2 = '2 25544  51.6498 109.4756 0003572  55.9686 274.8005 15.49815350868473'
satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
print(satellite)

# Check TLE epoch
print(satellite.epoch.utc_jpl())
t = ts.utc(2014, 1, 23, 11, 18, 7)

days = t - satellite.epoch
print('{:.3f} days away from epoch'.format(days))

if abs(days) > 14:
    satellites = load.tle_file(stations_url, reload=True)

# Find when a satellite rises and sets
bluffton = wgs84.latlon(+40.8939, -83.8917)
t0 = ts.utc(2014, 1, 23)
t1 = ts.utc(2014, 1, 24)
t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=30.0) #when it rises above 30 °
for ti, event in zip(t, events):
    name = ('rise above 30°', 'culminate', 'set below 30°')[event]
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

# Generating satellite positions

# You can instead use ts.now() for the current time
t = ts.utc(2014, 1, 23, 11, 18, 7)

geocentric = satellite.at(t)
print(geocentric.position.km)

# OR

subpoint = wgs84.subpoint(geocentric)
print('Latitude:', subpoint.latitude)
print('Longitude:', subpoint.longitude)
print('Elevation (m):', int(subpoint.elevation.m))

# above or bellow the horizon:
difference = satellite - bluffton
print(difference)

# method at()
topocentric = difference.at(t)
print(topocentric.position.km)


alt, az, distance = topocentric.altaz()

if alt.degrees > 0:
    print('The ISS is above the horizon')

print(alt)
print(az)
print(int(distance.km), 'km')

# Coordinates to see where among the stars:

ra, dec, distance = topocentric.radec()  # ICRF ("J2000")

print(ra)
print(dec)

"""
ra, dec, distance = topocentric.radec(epoch='date')

print(ra)
print(dec)
"""

#When satellite is in sunlight:
