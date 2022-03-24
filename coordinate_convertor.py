from astropy import coordinates as coord
from astropy import units as u
from astropy.time import Time
from astropy import time
import datetime
import pymap3d as pm

# def ecef_to_eci(present_time, xyz):
#     cartrep = coord.CartesianRepresentation(*xyz, unit=u.m)
#     itrs = coord.ITRS(cartrep, obstime=present_time)
#     gcrs = itrs.transform_to(coord.GCRS(obstime=present_time))
#     loc = coord.EarthLocation(*gcrs.cartesian.xyz)
#     return loc

# def eci_to_ecef(target_time, xyz):
#     cartrep = coord.CartesianRepresentation(*xyz, unit=u.m)
#     gcrs = coord.GCRS(cartrep, obstime=target_time)
#     itrs = gcrs.transform_to(coord.ITRS(obstime=target_time))
#     loc = coord.EarthLocation(*itrs.cartesian.xyz)
#     return loc

def ecef_to_j2000(target_time, *xyz):
    loc = pm.ecef2eci(*xyz, target_time)
    return loc

def j2000_to_ecef(current_time, *xyz):
    loc = pm.eci2ecef(*xyz, current_time)
    return loc





if __name__ == "__main__":
    current_time = datetime.datetime(2022, 3, 13, 0, 0, 0)
    current_time += datetime.timedelta(seconds=1000)

    eci_xyz = [2195952.2080041654, -5872767.623322786, -2005211.4364909476]
    print(current_time)

    current_time = datetime.datetime(2022, 3, 13, 0, 0, 0)
    current_time += datetime.timedelta(seconds=1000)
    loc = j2000_to_ecef(current_time, *eci_xyz)
    print(loc)



