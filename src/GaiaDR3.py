"""import astropy.units as u
from astropy.coordinates.sky_coordinate import SkyCoord
from astropy.units import Quantity
from astroquery.gaia import Gaia

import matplotlib.pyplot as plt
import numpy as np

# Suppress warnings. Comment this out if you wish to see the warning messages
import warnings
warnings.filterwarnings('ignore')

from astroquery.gaia import Gaia
tables = Gaia.load_tables(only_names=True)
for table in (tables):
    print (table.get_qualified_name())

job = Gaia.launch_job_async("SELECT * \
FROM gaiadr1.gaia_source \
WHERE CONTAINS(POINT(gaiadr1.gaia_source.ra,gaiadr1.gaia_source.dec),CIRCLE(56.75,24.1167,2))=1;" \
, dump_to_file=True)

print (job)

r = job.get_results()
print (r['source_id'])"""

############################################################################################################

import pyvo as vo

tap_service = vo.dal.TAPService("http://dc.g-vo.org/tap")
ex_query = """
    SELECT TOP 5
    source_id, ra, dec, phot_g_mean_mag
    FROM gaia.dr3lite
    WHERE phot_g_mean_mag BETWEEN 19 AND 20
    ORDER BY phot_g_mean_mag
    """
result = tap_service.search(ex_query)
print(result)

####################################################################

def download_gaia_dr3_data(folder = FOLDER, file_name = setup.dr3_random_file, n=100000):
    """
    Downloads a subset of Gaia DR3 data based on specified criteria.

    Parameters:
    folder (str): The directory where the downloaded data will be saved.
    file_name (str): The name of the file to save the downloaded data.
    n (int): The maximum number of records to download.
    """
    # Set up the TAP service connection for Gaia DR3
    tap_service_url = 'https://gaia.aip.de/tap'  #not final url
    service = vo.dal.TAPService(tap_service_url)
        # Construct the ADQL query for the desired Gaia DR3 data
    query = """
    SELECT TOP  %i * FROM gaiadr3.gaia_source ORDER BY random_Index'%n
    source_id, ra, dec, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE phot_g_mean_mag < 15
    """.format(n)

    # Execute the query
    result = service.search(query)

    # Convert the results to an Astropy table and save
    data_table = result.to_table()
    data_table.write(folder + file_name, format='fits', overwrite=True)
    print(f"Data successfully downloaded and saved to {folder + file_name}")

