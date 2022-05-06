from sklearn.metrics import mean_squared_error
import numpy as np
from data_aug import Data_aug
import nibabel as nib
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
def mse_(x, y):
    return mean_squared_error(x, y)



    
# read the data
data = nib.load("Specify your path").get_fdata()

 # bright data
data_bright = Data_aug.brightness(data)

# Rotated data between 0-30 degrees
data_rotated30 = Data_aug.rotation_zoom3D(data)



data_vec_id = REshape.remote(data)
data_rotated30_vec_id = REshape.remote(data_rotated30)
data_bright_vec_id = REshape.remote(data_bright)


mse_rotate30_id = mse_.remote(data_vec_id, data_rotated30_vec_id)
mse_bright_id = mse_.remote(data_vec_id, data_bright_vec_id)


mse_rotate30 = ray.get(mse_rotate30_id)
mse_bright = ray.get(mse_bright_id)

print(" MSE between original data and data rotated30:", mse_rotate30)
print(" MSE between original data and data brightness:", mse_bright)

end = time.time()
print(end - start, "seconds")