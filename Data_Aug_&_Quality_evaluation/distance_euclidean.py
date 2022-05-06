from time import time
import numpy as np
import nibabel as nib
from data_aug import Data_aug
from scipy.spatial import distance
import ray
import time


start = time.time()


@ray.remote
def REshape(data):
    """
    Transform the 3D image to vector
    """
    return np.reshape(data, (data.shape[0]*data.shape[1]*data.shape[2], ))


@ray.remote
def distance_euclidean(x, y):
    """
    Euclidean distance between original data and generated data 
    """
    return distance.euclidean(x,y)


    
# read the data
data = nib.load("Specify your path").get_fdata()


 # bright data
data_bright = Data_aug.brightness(data)

# Rotated data between 0-30 degrees
data_rotated30 = Data_aug.rotation_zoom3D(data)



data_vec_id = REshape.remote(data)
data_rotated30_vec_id = REshape.remote(data_rotated30)
data_bright_vec_id = REshape.remote(data_bright)

disEuc_rotate30_id = distance_euclidean.remote(data_vec_id, data_rotated30_vec_id)
disEuc_bright_id = distance_euclidean.remote(data_vec_id, data_bright_vec_id)


disEuc_rotate30 = ray.get(disEuc_rotate30_id)
disEuc_bright = ray.get(disEuc_bright_id)

print(" Euclidean distance between original data and data rotated30:", (1/(data.shape[0]*data.shape[1]*data.shape[2]))*disEuc_rotate30)
print(" Euclidean distance between original data and data brightness:", (1/(data.shape[0]*data.shape[1]*data.shape[2]))*disEuc_bright)

end = time.time()
print(end - start, "seconds")