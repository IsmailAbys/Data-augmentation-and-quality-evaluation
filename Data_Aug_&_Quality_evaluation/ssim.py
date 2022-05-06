from skimage.metrics import structural_similarity as ssim
import nibabel as nib
from data_aug import Data_aug
import numpy as np
import ray
import time

start = time.time()


@ray.remote
def ssim_(x,y):
    return ssim(x,y)


@ray.remote
def REshape(data):
    """
    Transform the 3D image to vector
    """
    return np.reshape(data, (data.shape[0]*data.shape[1]*data.shape[2], ))

   
# read the data
data = nib.load(r"C:\Users\Utilisateur\OneDrive - ABYS MEDICAL\Bureau\DataAugmentation\data\ParoiPost.nii.gz").get_fdata()

 # bright data
data_bright = Data_aug.brightness(data)

# Rotated data between 0-30 degrees
data_rotated30 = Data_aug.rotation_zoom3D(data)



data_vec_id = REshape.remote(data)
data_rotated30_vec_id = REshape.remote(data_rotated30)
data_bright_vec_id = REshape.remote(data_bright)

ssim_rotate30_id = ssim_.remote(data_vec_id, data_rotated30_vec_id)
ssim_bright_id = ssim_.remote(data_vec_id, data_bright_vec_id)


ssim_rotate30 = ray.get(ssim_rotate30_id)
ssim_bright = ray.get(ssim_bright_id)

print(" ssim between original data and data rotated30:", ssim_rotate30)
print(" ssim between original data and data brightness:", ssim_bright)

end = time.time()
print(end - start, "seconds")

