import numpy as np

#Seed number to be set as input for simulation 
SEED = 1234
def rng(seed):
    #Initialize a random number generator based on seed
    return  np.random.default_rng(seed)


#Properties for map
RESOLUTION = 0.25
LAT_S = 48.5
LAT_N = 50.75
LON_E = -123.0
LON_W = -128.5

#Height of tropopause in hPa pressure altitude (approximate height for Vancouver Island lattitude) 
TROPOPAUSE_HEIGHT = 264


#Standard deviations of wind strengths (set wider for forecast than nowcast, with each further forecast having a wider standard deviation)
BASE_STDEV = 2.0
WINDSTDEV_INC_PER6HR = 0.05
stds = {'NOWCAST_STDEV': BASE_STDEV}

for x in range(1,29):
    stds['FORECAST_STDEV_%02d' % x] = BASE_STDEV + (x)*WINDSTDEV_INC_PER6HR

#Alititudes (in hPa pressure heights) at which we want data
HEIGHTS = [600, 450, 300, 200, 150, 100, 50, 30, 15, 7]

#Bias direction and strength to be applied in the positive direcion below toropopause and negative above the tropopause
BIAS_DIRECTION = rng(SEED).integers(0,2*np.pi)
BIAS_STRENGTH = 3.0

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

    def apply_bias_under(self):
        #apply bias to winds under troposphere
        self.ugrid += BIAS_STRENGTH*np.cos(BIAS_DIRECTION)
        self.vgrid += BIAS_STRENGTH*np.sin(BIAS_DIRECTION)

    def apply_bias_over(self):
        #apply bias to winds over troposphere
        self.ugrid -= BIAS_STRENGTH*np.cos(BIAS_DIRECTION)
        self.vgrid -=  BIAS_STRENGTH*np.cos(BIAS_DIRECTION)

class windGrid3D:
    #Class containing  dictionnary of windGrid2D objects for each given height
    def __init__(self,lat_min,lat_max,lon_min,lon_max, res, std, heights):
        self.altitudes = {}
        seed = SEED
        for height in heights:
            self.altitudes[height] = windGrid2D(lat_min, lat_max, lon_min, lon_max, res, std)
            #Apply biasing
            if height <= TROPOPAUSE_HEIGHT:
                self.altitudes[height].apply_bias_under()
            else:
                self.altitudes[height].apply_bias_over()
                
            #Locally change seed value to get different values for each altitude's wind data
            #set to 2 and not 1 so there is no overlap between current level v-grid and next level u-grid
            seed += 2
        
    def __repr__(self):
        return str(self.altitudes)

            

            



#Sample grids for Vancouver Island coordinates for wind during one time period
wind_now = windGrid3D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,stds['NOWCAST_STDEV'], HEIGHTS)
wind_fore_01 = windGrid3D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,stds['FORECAST_STDEV_01'], HEIGHTS)
wind_fore_08 = windGrid3D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,stds['FORECAST_STDEV_08'], HEIGHTS)
wind_fore_26 = windGrid3D(LAT_S,LAT_N,LON_E,LON_W,RESOLUTION,stds['FORECAST_STDEV_26'], HEIGHTS)

