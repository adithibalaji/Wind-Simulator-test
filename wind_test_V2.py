import numpy as np

#Seed number to be set as input for simulation 
SEED = 1234


#Properties for map
RESOLUTION = 0.25
LAT_S = 48.5
LAT_N = 50.75
LON_E = -123.0
LON_W = -128.5

#Standard deviation of wind strength (set wider for forecast than nowcast)
STD_NOW = 2.0
STD_FORE = 3.2


def rng(seed):
    #Initialize a random number generator based on seed
    return  np.random.default_rng(seed)

def calc_array_size(lat_min,lat_max,lon_min,lon_max, res):
    #Function to calculate array size of output based on input coordinates and resolution
    # Note that coordinates must be multiples of resolution
    latrange = abs(lat_max-lat_min)/res
    lonrange = abs(lon_max - lon_min)/res
    return [int(latrange), int(lonrange)]

def generate_grid(lat_min,lat_max,lon_min,lon_max, res, std):
    #Generate grids for u and v direction winds based on input coordinates, resolution and standard devition 
    #of the i=wind strength
    size = calc_array_size(lat_min,lat_max,lon_min,lon_max, res)
    rand1 = rng(SEED)
    rand2 = rng(SEED)
    ugrid = rand1.normal(0,std,size)
    vgrid = rand2.normal(0,std,size)
    return ugrid,vgrid



#Sample grids for Vancouver Island coordinates for one level of wind
wind_now = generate_grid(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,STD_NOW)
wind_fore = generate_grid(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,STD_FORE)
print(wind_now)
print(wind_fore)