from tokenize import Floatnumber
from pydap.client import open_url
import numpy as np
import matplotlib as mpl
import re


#Sample constants for grid resolution and area
RESOLUTION = 0.25
LAT_S = 48.5
LAT_N = 50.75
LON_E = -123.0
LON_W = -128.5
TIMESTAMP = 0
#Normal distribution standard error used for generating random numbers
ERR = 0.5

#Base dataset which we can permute. Can also run script to automatically procure data. 
dataset = open_url('https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs20220526/gfs_0p25_18z_anl')

#Function to find index of a specific coordinate within the data array, given the grid resolution, the coordinate value,
# and the type of coordinate (lat or lon)
def find_idx(res: float, coord:float, coord_type: str)->int:
    coord = round(coord/res)*res
    if coord_type == 'lat':
        return int((coord + 90)/res) 

    elif coord_type == 'lon':
        return int((coord+180)/res)

    raise Exception ('Need to specify whether coordinate is lat or lon')



#Find grid endpoints
lat_low = find_idx(RESOLUTION,LAT_S, 'lat')
lat_high = find_idx(RESOLUTION,LAT_N, 'lat')
lon_low = find_idx(RESOLUTION, LON_W, 'lon')
lon_high = find_idx(RESOLUTION,LON_E, 'lon')



#Class representing wind data for one height level of selected area
#TO DO: Implement regex to avoid having to manually input height
class WindGrid_2D:
    def __init__(self, ugrid, vgrid, height):
        self.ugrid = ugrid
        self.vgrid = vgrid
        self.height = height
        self.latsize = len(ugrid)
        self.lonsize = len(ugrid[0])

    def __repr__(self):
        #TO DO: Implement map printing function in mpl, using quiver plot
        return f"Wind component map at height {self.height}"

    def rand_all(self, error):
        #method to randomize all u and v vectors by a different random scaling factor
        #Probably too slow for actual implmentation, but gives more varied results. 
        randarr1 = np.random.normal(0,error,size = (self.latsize, self.lonsize))
        self.ugrid = np.multiply(self.ugrid,randarr1)
        #Two random number arrays used to induce changes in wind direction vectors
        randarr2 = np.random.normal(0,error,size = (self.latsize, self.lonsize))
        self.vgrid = np.multiply(self.vgrid,randarr2)


    def rand_unif(self, error):
        #method to scale all u vectors by a random number drawn from a normal distribution, and scale v vectors by a separate random number
        #Faster implementation, but could exaggerate winds to an unrealistic extent by up-scaling all winds
        randint1 = np.random.normal(0,error)
        randint2 = np.random.normal(0,error)
        self.ugrid *=randint1
        self.vgrid *=randint2    

    def generate_gradient(self,error):
        #Sub-method to be used for rand_gradient method to generate scaling array
        #Generate random numbers to scale 4 corner points, points read from top left counterclockwise
        randint1 = np.random.normal(0,error)
        randint2 = np.random.normal(0,error)
        randint3 = np.random.normal(0,error)
        randint4 = np.random.normal(0,error)

        #Generate scaling arrays for left and right edges
        leftarr = np.linspace(randint1, randint4, self.latsize)
        rightarr = np.linspace(randint2, randint3, self.latsize)
        #Generate scaling factors
        full_arr = []
        for i in range(self.latsize):
            line_arr = np.linspace(leftarr[i], rightarr[i], self.lonsize)
            line_arr = np.array(line_arr)
            full_arr.append(line_arr)
        full_arr = np.array(full_arr)
        return full_arr
    
    def rand_gradient(self, error):
        #Method to randomly sclaes edges of graph and then apply gradiented scaling to the center points
        #(Test method to see if calculating array-based scaling factors is faster than generating individual random numbers)
        gradient_u = self.generate_gradient(error)
        gradient_v = self.generate_gradient(error)
        self.ugrid = np.multiply(self.ugrid,gradient_u)
        self.vgrid = np.multiply(self.vgrid,gradient_v)
        
        


#sample grid data for one height
vgrd40m = dataset['vgrd40m'].vgrd40m[TIMESTAMP, lat_low:lat_high, lon_low:lon_high][0]
ugrd40m = dataset['ugrd40m'].ugrd40m[TIMESTAMP, lat_low:lat_high, lon_low:lon_high][0]
winddata1 = WindGrid(ugrd40m,vgrd40m,40)


print(winddata1.ugrid[0])
winddata1.rand_gradient(ERR)
print(winddata1.ugrid[0])

