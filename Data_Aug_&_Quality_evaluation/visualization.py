import os
# from itertools import cycle
import numpy as np
import vispy
from vispy import app, scene
from vispy.visuals.transforms import STTransform
import nibabel as nib
import scipy.ndimage
from data_aug import Data_aug


# Inspired by:
# https://github.com/pranathivemuri/vispy-example-3d/blob/master/display_numpy_volume.py
# create colormaps that work well for translucent and additive volume rendering

# class TransFire(BaseColormap):
#     glsl_map = """
#     vec4 translucent_fire(float t) {
#         return vec4(pow(t, 0.5), t, t*t, max(0, t*1.05 - 0.05));
#     }
#     """
    
# class TransGrays(BaseColormap):
#     glsl_map = """
#     vec4 translucent_grays(float t) {
#         return vec4(t, t, t, t*0.05);
#     }
#     """
    
# # Setup colormap iterators
# opaque_cmaps = cycle(get_colormaps())
# translucent_cmaps = cycle([TransFire(), TransGrays()])
# opaque_cmap = next(opaque_cmaps)
# translucent_cmap = next(translucent_cmaps)

class ArrayView3D(object):

    def view3DArray(data):
        ArrayView3D.gain = 0.8
        ArrayView3D.gamma = 0.8
        canvas = scene.SceneCanvas(
            keys='interactive', size=(800, 600), show=True)
        
        # Set up a viewbox to display the image with interactive pan/zoom
        view = canvas.central_widget.add_view()
        
        # Create the volume visuals, only one is visible
        volume1 = scene.visuals.Volume(
            data, parent=view.scene, threshold=0.225)        
        
        fov = 60.
        cam2 = scene.cameras.TurntableCamera(
            parent=view.scene, fov=fov,
            name='Turntable')
        view.camera = cam2

        # Create an XYZaxis visual
        axis = scene.visuals.XYZAxis(parent=view)
        s = STTransform(translate=(50, 50), scale=(50, 50, 50, 1))
        affine = s.as_matrix()
        axis.transform = affine

        # Implement axis connection with cam2
        @canvas.events.mouse_move.connect
        def on_mouse_move(event):
            if event.button == 1 and event.is_dragging:
                axis.transform.reset()

                axis.transform.rotate(cam2.roll, (0,1, 0))
                axis.transform.rotate(cam2.elevation, (0,0,1))
                axis.transform.rotate(cam2.azimuth, (1,0,0))

                axis.transform.scale((50, 50, 0.001))
                axis.transform.translate((50., 50.))
                axis.update()
        
        # Implement key presses
        @canvas.events.key_press.connect
        def on_key_press(event):
            global opaque_cmap, translucent_cmap

            
            if event.text == 'r':
                data = data_rot30
                volume1.set_data(data, copy=True)    
                view.update() 
            

            if event.text == 'b':
                data = data_bright
                volume1.set_data(data_bright, copy=True)    
                view.update() 
            
            if event.text == 'o':
                data = data_
                volume1.set_data(data, copy=True)    
                view.update() 



if __name__ == "__main__":
    data = nib.load(r"C:\Users\Utilisateur\OneDrive - ABYS MEDICAL\Bureau\DataAugmentation\data\Test_Patient2.nii.gz").get_fdata() 
    data_bright = Data_aug.brightness(data)
    data_rot30 = Data_aug.rotation_zoom3D(data)
    data_ = data
    ArrayView3D.view3DArray(data)
    app.run()