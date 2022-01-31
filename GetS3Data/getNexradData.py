# Code for reading S3 data is Referenced from https://nbviewer.org/gist/dopplershift/356f2e14832e9b676207
import json
from datetime import datetime, timedelta
from timeit import default_timer

import numpy as np
from flask import Flask, request, json
from flask_restful import Api, Resource, reqparse
from siphon.radarserver import RadarServer

app = Flask(__name__)
api = Api(app)


class NexradData(Resource):
    def post(self):
        data = json.loads(request.data)
        x = get_for_single_timestamp(data['station'], data['date'], data['time'])
        return x


def raw_to_masked_float(var, data):
    # Values come back signed. If the _Unsigned attribute is set, we need to convert
    # from the range [-127, 128] to [0, 255].
    if var._Unsigned:
        data = data & 255

    # Mask missing points
    data = np.ma.array(data, mask=data == 0)

    # Convert to float using the scale and offset
    return data * var.scale_factor + var.add_offset


def polar_to_cartesian(az, rng):
    az_rad = np.deg2rad(az)[:, None]
    x = rng * np.sin(az_rad)
    y = rng * np.cos(az_rad)
    return x, y


def get_for_single_timestamp(station, date, time):
    start1 = default_timer()
    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')

    query = rs.query()
    d = date.split('-')
    t = time.split(':')
    date_time = datetime(int(d[0]), int(d[1]), int(d[2]), int(t[0]), int(t[1]), int(t[2]))
    query.stations(station).time(date_time)

    d = {}

    f = rs.validate_query(query)

    if f:

        catalog = rs.get_catalog(query)

        data = catalog.datasets[0].remote_access()

        sweep = 0

        ref_var = data.variables['Reflectivity_HI']
        ref_data = ref_var[sweep]
        rng = data.variables['distanceR_HI'][:]
        az = data.variables['azimuthR_HI'][sweep]

        ref = raw_to_masked_float(ref_var, ref_data)
        d['ref_val'] = ref.tolist()
        x, y = polar_to_cartesian(az, rng)
        d['ref_x'] = x.tolist()
        d['ref_y'] = y.tolist()

        rad_vel_var = data.variables['RadialVelocity_HI']
        rad_vel_data = rad_vel_var[sweep]
        rng = data.variables['distanceV_HI'][:]
        az = data.variables['azimuthV_HI'][sweep]

        rad_vel = raw_to_masked_float(rad_vel_var, rad_vel_data)
        #d['rad_vel_val'] = rad_vel.tolist()
        x, y = polar_to_cartesian(az, rng)
        #d['rad_vel_x'] = x.tolist()
        #d['rad_vel_y'] = y.tolist()

        spec_wid_var = data.variables['SpectrumWidth_HI']
        spec_wid_data = spec_wid_var[sweep]
        rng = data.variables['distanceD_HI'][:]
        az = data.variables['azimuthD_HI'][sweep]

        spec_wid = raw_to_masked_float(spec_wid_var, spec_wid_data)
        #d['spec_wid_val'] = spec_wid.tolist()
        x, y = polar_to_cartesian(az, rng)
        #d['spec_wid_x'] = x.tolist()
        #d['spec_wid_y'] = y.tolist()


        return json.dumps(d)


    else:
        return "No data found for given time stamp"


def get_for_single_timestamp_range(station, date_time):
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

        l.append((ref, x, y))
    return l


api.add_resource(NexradData, '/api/nexraddata')

if __name__ == '__main__':
    app.run(port='5002')
