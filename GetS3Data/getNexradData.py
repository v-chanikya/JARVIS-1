# Referenced from https://nbviewer.org/gist/dopplershift/356f2e14832e9b676207


from siphon.radarserver import RadarServer
from datetime import datetime, timedelta
import numpy as np

from timeit import default_timer


def raw_to_masked_float(var, data):
    # Values come back signed. If the _Unsigned attribute is set, we need to convert
    # from the range [-127, 128] to [0, 255].
    if var._Unsigned:
        data = data & 255

    # Mask missing points
    data = np.ma.array(data, mask=data==0)

    # Convert to float using the scale and offset
    return data * var.scale_factor + var.add_offset

def polar_to_cartesian(az, rng):
    az_rad = np.deg2rad(az)[:, None]
    x = rng * np.sin(az_rad)
    y = rng * np.cos(az_rad)
    return x, y


def get_for_single_timestamp(stattion, date_time):
    start1 = default_timer()
    station = 'KLVX'
    dt = datetime.utcnow()
    print(dt)
    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')

    query = rs.query()
    query.stations(station).time(dt)

    f = rs.validate_query(query)

    if f:

        catalog = rs.get_catalog(query)

        print(catalog.datasets)
        data = catalog.datasets[0].remote_access()
        end1 = default_timer() - start1

        print(end1)
        sweep = 0
        ref_var = data.variables['Reflectivity_HI']
        ref_data = ref_var[sweep]
        rng = data.variables['distanceR_HI'][:]
        az = data.variables['azimuthR_HI'][sweep]

        ref = raw_to_masked_float(ref_var, ref_data)
        x, y = polar_to_cartesian(az, rng)

        return (ref,x,y)


    else:
        print("No data found for given time stamp")
    print("")

def get_for_single_timestamp_range(stattion, date_time):

    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')
    query = rs.query()
    dt = datetime(2012, 10, 29, 15)
    query.lonlat_point(-73.687, 41.175).time_range(dt, dt + timedelta(hours=1))

    cat = rs.get_catalog(query)

    l = []

    for ds_name in cat.datasets:
        # After looping over the list of sorted datasets, pull the actual Dataset object out
        # of our list of items and access over CDMRemote
        data = cat.datasets[ds_name].remote_access()

        # Pull out the data of interest
        sweep = 0
        rng = data.variables['distanceR_HI'][:]
        az = data.variables['azimuthR_HI'][sweep]
        ref_var = data.variables['Reflectivity_HI']

        # Convert data to float and coordinates to Cartesian
        ref = raw_to_masked_float(ref_var, ref_var[sweep])
        x, y = polar_to_cartesian(az, rng)

        l.append((ref,x,y))
    return l


"""
start = default_timer()
x = get_for_single_timestamp("klvx", 'date_time')
end = default_timer() - start
"""