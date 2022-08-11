
#include <iostream>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <random>
#include <algorithm>
#include <functional>
#include <iterator>



using namespace std;

//Seed number to be set as input for simulation 
int SEED = 1234;

//Properties for map
const float RESOLUTION = 0.25;
const float LAT_S = 48.5;
const float LAT_N = 50.75;
const float LON_E = -123.0;
const float LON_W = -128.5;


//Height of tropopause in hPa pressure altitude (approximate height for Vancouver Island lattitude) 
const float TROPOPAUSE_HEIGHT= 264;

//Alititudes (in hPa pressure heights) at which we want data
int HEIGHTS[10]  = {600, 450, 300, 200, 150, 100, 50, 30, 15, 7};

//Values to initialize standard deviations for different timeframes
float BASE_STDEV = 2.0;
float WINDSTDEV_INC_PER6HR = 0.05;


//Bias direction and strength to be applied in the positive direcion below toropopause and negative above the tropopause
float BIAS_STRENGTH = 3.0;
float BIAS_DIRECTION = 0.2;

std::vector<float> create_random_arr(int seed, int n, float stdev) {
    //Random array filling mechanism with inputs for generator seed, number of array elements
    // and standard deviation for sample distribution (locally seeded to prevent data overlap)
    std::mt19937 eng(seed);
    std::normal_distribution<> dist{0, stdev};
    std::vector<float> v(n);
    generate(begin(v), end(v), bind(dist, eng));
  return v;

}

//General functions
int calc_array_size(float, float, float);
void print(std::vector<float> const &input);

//Functions used to apply biases to wind data
float bias_cos(float x) {  return (x+BIAS_STRENGTH*cos(BIAS_DIRECTION)); }
float bias_sin(float x) {  return (x+BIAS_STRENGTH*sin(BIAS_DIRECTION)); }
float bias_neg_cos(float x) {  return (x-BIAS_STRENGTH*cos(BIAS_DIRECTION)); }

//Class for one-level wind data
class windGrid2D {
    public:
    // Base level attributes
    float lat_min, lat_max, lon_min, lon_max, res, stdev, lat_size, lon_size;
    std::vector<float> ugrid, vgrid;
    //constructor
    void create_grid(int height, float lat_min, float lat_max,float lon_min,float lon_max,float res,float stdev){
        height = height;
        lat_min = lat_min;
        lat_max = lat_max;
        lon_min = lon_min;
        lon_max = lon_max;
        res = res;
        stdev = stdev;
        //populate arrays of u and v wind grids
        lat_size = calc_array_size(lat_min, lat_max, res);
        lon_size = calc_array_size(lon_min, lon_max, res);
        ugrid = create_random_arr(SEED, lat_size, stdev);
        vgrid = create_random_arr(SEED+1, lon_size, stdev);
        }
    
    void apply_bias_under(){
        //apply bias to winds below the tropopause
        transform(ugrid.begin(), ugrid.end(), ugrid.begin(), bias_cos);
        transform(vgrid.begin(), vgrid.end(), vgrid.begin(), bias_sin);
    }

    void apply_bias_over(){
        //aply bias to winds above the tropopause
        transform(ugrid.begin(), ugrid.end(), ugrid.begin(), bias_neg_cos);
        transform(vgrid.begin(), vgrid.end(), vgrid.begin(), bias_neg_cos);
    }
};

class windGrid3D{
    public:
    //base level attributes
    float lat_min, lat_max, lon_min, lon_max, res, stdev, lat_size, lon_size;
    int heights[10];
    windGrid2D data[10];
    //constructor
    windGrid3D(int heights[10], float lat_min, float lat_max,float lon_min,float lon_max,float res,float stdev){
        heights = heights;
        lat_min = lat_min;
        lat_max = lat_max;
        lon_min = lon_min;
        lon_max = lon_max;
        res = res;
        stdev = stdev;

        //Generate wind grids for each height level
        for (int i = 0; i < 10; i++)  {
        windGrid2D windgrid;
        windgrid.create_grid(heights[i], lat_min, lat_max, lon_min, lon_max, res, stdev);

        //apply biasing based on height
        if (i > TROPOPAUSE_HEIGHT){
            windgrid.apply_bias_over();
        }
        else{
            windgrid.apply_bias_under();
        }
        //package 2D wind grid objects in data array
        data[i] = windgrid;
        SEED += 2;

        }
}

    void print_grid3D(){
        // Print out grid data for every height for a single instance of a 3D grid
        for (int i = 0; i<10; i++){
            cout << HEIGHTS[i] << " hPa ugrid : ";
            print(data[i].ugrid);
            cout << "\n" << HEIGHTS[i] << " hPa vgrid : " ; 
            print(data[i].vgrid);
            cout << "\n";

        }
    }

};

int main()
{
    //Initialize random device 
    std::random_device rd{};
    std::mt19937 gen{rd()};
    std::mt19937 eng(SEED);

    //Initialize standard deviations 
    float STDS[30];
    STDS[0] = BASE_STDEV;
    for (int i=0; i<29; i++){
        STDS[i] = BASE_STDEV + i*WINDSTDEV_INC_PER6HR;
    }

    // Example grids
    windGrid3D windgrid_now(HEIGHTS, LAT_S, LAT_N, LON_E, LON_W, RESOLUTION, STDS[0]);
    windGrid3D windgrid_6hr(HEIGHTS, LAT_S, LAT_N, LON_E, LON_W, RESOLUTION, STDS[1]);

    windgrid_now.print_grid3D();
	return 0;

}



int calc_array_size(float min, float max, float res){
    // Function to calculate array size of output based on input coordinates and resolution
    // Note that coordinates must be multiples of resolution
    int range = abs(min- max)/res;
    return range;

}



void print(std::vector<float> const &input){
    // Function to print vectors (mostly used for testing)
    std::copy(input.begin(),
            input.end(),
            std::ostream_iterator<float>(std::cout, " "));
}

