#!/usr/local/bin/python3

# On windows installation

# Astronomical Coordinates 1

import matplotlib.pyplot as plt
import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord, Distance
from astropy.io import fits
from astropy.table import QTable
from astropy.utils.data import download_file

from astroquery.gaia import Gaia
Gaia.ROW_LIMIT = 10000  # Set the row limit for returned data
print("#########################################")
# Representing On-sky positions with astropy.cooordinates

# star ngc188, we know the coordinates
ngc188_center = SkyCoord(12.11*u.deg, 85.26*u.deg, frame='icrs') #  ICRS coordinate frame or equatorial or J2000
# recommended to specify frame even if icrs if default one


ngc188_center_bis = SkyCoord('00h48m26.4s', '85d15m36s', frame='icrs')


SkyCoord('00:48:26.4 85:15:36', unit=(u.hour, u.deg), frame='icrs') # To specify delimiters

ngc188_center = SkyCoord.from_name('NGC 188') # To have coordinates from the Internet
print(ngc188_center)
print(ngc188_center.ra, ngc188_center.dec) # RA for Right Ascension and DEC for declinaison
type(ngc188_center.ra), type(ngc188_center.dec)

(ngc188_center.ra.to(u.hourangle),
 ngc188_center.ra.to(u.radian),
 ngc188_center.ra.to(u.degree))

# d for degree, m for minute and s for second or respectively ° ' "

# Querying the Gaia Archive to Retrieve Coordinates of Stars in NGC 188

job = Gaia.cone_search_async(ngc188_center, radius=0.5*u.deg)
ngc188_table = job.get_results()

# only keep stars brighter than G=19 magnitude
ngc188_table = ngc188_table[ngc188_table['phot_g_mean_mag'] < 19*u.mag]
cols = ['source_id',
 'ra',
 'dec',
 'parallax',
 'parallax_error',
 'pmra',
 'pmdec',
 'radial_velocity',
 'phot_g_mean_mag',
 'phot_bp_mean_mag',
 'phot_rp_mean_mag']
ngc188_table[cols].write('gaia_results.fits', overwrite=True)

ngc188_table = QTable.read('gaia_results.fits')
print(len(ngc188_table))
# ngc188_table['dec'] to see dec part for instance

ngc188_gaia_coords = SkyCoord(ngc188_table['ra'], ngc188_table['dec'])
print(ngc188_gaia_coords)


# Distance information

ngc188_center_3d = SkyCoord(12.11*u.deg, 85.26*u.deg, distance=1.96*u.kpc)

parallax_snr = ngc188_table['parallax'] / ngc188_table['parallax_error']
ngc188_table_3d = ngc188_table[parallax_snr > 10]
len(ngc188_table_3d)
# parallax_snr to work on !

gaia_dist = Distance(parallax=ngc188_table_3d['parallax'])
print(gaia_dist)

ngc188_coords_3d = SkyCoord(ra=ngc188_table_3d['ra'],
                            dec=ngc188_table_3d['dec'],
                            distance=gaia_dist)
print(ngc188_coords_3d)

# matplotlib to illustrate the coordinates

fig, ax = plt.subplots(figsize=(6.5, 5.2),
                       constrained_layout=True)
cs = ax.scatter(ngc188_coords_3d.ra.degree,
                ngc188_coords_3d.dec.degree,
                c=ngc188_coords_3d.distance.kpc,
                s=5, vmin=1.5, vmax=2.5, cmap='twilight')
cb = fig.colorbar(cs)
cb.set_label(f'distance [{u.kpc:latex_inline}]')

ax.set_xlabel('RA [deg]')
ax.set_ylabel('Dec [deg]')

ax.set_title('Gaia DR2 sources near NGC 188', fontsize=18)
plt.show()
