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

HEIGHTS = ['10m','20m','40m','60m']

def rng(seed):
    #Initialize a random number generator based on seed
    return  np.random.default_rng(seed)

def calc_array_size(lat_min,lat_max,lon_min,lon_max, res):
    #Function to calculate array size of output based on input coordinates and resolution
    # Note that coordinates must be multiples of resolution
    latrange = abs(lat_max-lat_min)/res
    lonrange = abs(lon_max - lon_min)/res
    return [int(latrange), int(lonrange)]



class windGrid2D:
    #Class containing both u and v direction wind data for one atmospheric height wihtin a given region
    def __init__(self,lat_min,lat_max,lon_min,lon_max, res, std):
    #Generate grids for u and v direction winds based on input coordinates, resolution and standard devition 
    #of the i=wind strength
        size = calc_array_size(lat_min,lat_max,lon_min,lon_max, res)
        rand1 = rng(SEED)
        rand2 = rng(SEED+1)
        self.ugrid = rand1.normal(0,std,size)
        self.vgrid = rand2.normal(0,std,size)

    def __repr__(self):
        return f'u-grid: {self.ugrid}, v-grid: {self.vgrid}' 

class windGrid3D:
    #Class containing  dictionnary of windGrid2D objects for each given height
    def __init__(self,lat_min,lat_max,lon_min,lon_max, res, std, heights):
        self.altitudes = {}
        seed = SEED
        for height in heights:
            self.altitudes[height] = windGrid2D(lat_min, lat_max, lon_min, lon_max, res, std)
            #Locally change seed value to get different values for each altitude's wind data
            #set to 2 and not 1 so there is no overlap between current level v-grid and next level u-grid
            seed += 2
        
    def __repr__(self):
        return str(self.altitudes)

            

            



#Sample grids for Vancouver Island coordinates for one level of wind
#wind_now = windGrid2D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,STD_NOW,HEIGHTS)
wind_fore = windGrid3D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,STD_FORE, HEIGHTS)
wind_now = windGrid3D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,STD_NOW, HEIGHTS)
