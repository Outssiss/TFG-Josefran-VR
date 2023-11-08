import openvr
import numpy as np
import cv2
import sys
import time
import ctypes
from PIL import Image
def main():

    if openvr.isHmdPresent():
        print("VR head set found")
        
    if openvr.isRuntimeInstalled():
        print("Runtime is installed")
        
    vr_system = openvr.init(openvr.VRApplication_Scene)
    compositor = openvr.IVRCompositor()
    overlay = openvr.IVROverlay()
    
    imagen_der = Image.open("camera_der_dist.png")
    if imagen_der.mode != "RGBA":
        imagen_der = imagen_der.convert("RGBA")
        
    img_data = np.array(imagen_der)
    
    
    compositor.submit(eye=openvr.Eye_Right, texture=img_data)
    print("sent")
    
if __name__ == "__main__":
    main()