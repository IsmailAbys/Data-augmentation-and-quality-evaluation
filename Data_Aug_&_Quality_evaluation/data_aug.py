import nibabel as nib
import os
import numpy as np
from scipy.ndimage import affine_transform
import time

start = time.time()


class Data_aug(object):
    
    
    def brightness(X):
        """
        Changing the brighness of a image using power-law gamma transformation.
        Gain and gamma are chosen randomly for each image channel.
    
        Gain chosen between [1.2 - 2.0]
        Gamma chosen between [1.2 - 2.0]
    
        new_im = gain * im^gamma
        """
        X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
        X_new = np.zeros(X.shape)

        for c in range(X.shape[-1]):
            im = X[:,:,:, c]        
            gain =0.67474081005230144
            gamma = 1.1
            im_new = np.sign(im)*gain*(np.abs(im)**gamma)
            X_new[:,:,:, c] = im_new 
        X_new = np.reshape(X_new, (X_new.shape[0], X_new.shape[1], X_new.shape[2]))
        return X_new


    # def flip3D(X):
    #     """
    #     Flip the 3D image respect one of the 3 axis chosen randomly
    #     """
    #     choice = np.random.randint(3)
    #     if choice == 0: # flip on x
    #         X_flip = X[::-1, :, :]
    #     if choice == 1: # flip on y
    #         X_flip = X[:, ::-1, :]
    #     if choice == 2: # flip on z
    #         X_flip= X[:, :, ::-1]
    #     return X_flip


    def rotation_zoom3D(X):
        """
        Rotate a 3D image with alfa, beta and gamma degree respect the axis x, y and z respectively.
            The three angles are chosen randomly between 0-30 degrees
        """
        alpha, beta, gamma = np.random.random_sample(3)*np.pi/10
        Rx = np.array([[1, 0, 0],
                    [0, np.cos(alpha), -np.sin(alpha)],
                    [0, np.sin(alpha), np.cos(alpha)]])
    
        Ry = np.array([[np.cos(beta), 0, np.sin(beta)],
                    [0, 1, 0],
                    [-np.sin(beta), 0, np.cos(beta)]])
    
        Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                    [np.sin(gamma), np.cos(gamma), 0],
                    [0, 0, 1]])
        
        R_rot = np.dot(np.dot(Rx, Ry), Rz)
        
        a, b = 0.8, 1.2
        alpha, beta, gamma = (b-a)*np.random.random_sample(3) + a
        R_scale = np.array([[alpha, 0, 0],
                    [0, beta, 0],
                    [0, 0, gamma]])
        
        R = np.dot(R_rot, R_scale)
        X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
        X_rot = np.empty_like(X)
        for channel in range(X.shape[-1]):
            X_rot[:,:,:,channel] = affine_transform(X[:,:,:,channel], R, offset=0, order=1, mode='constant')
        X_rot = np.reshape(X_rot, (X_rot.shape[0], X_rot.shape[1], X_rot.shape[2]))
        return X_rot
    
    # @ray.remote
    # def elastic(X):
    #     """
    #     Elastic deformation on a image
    #     """
    
    #     X_el= elasticdeform.deform_random_grid(X, sigma=2, mode='constant')
    
    #     return X_el


    # def rotate90(X):
    #     """
    #     Rotate a 3D image 90 degrees
    #     """
    #     return np.rot90(X)


