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
    
    camera = openvr.IVRTrackedCamera()
    camera_handle = camera.acquireVideoStreamingService(0)
    
    frame_type = openvr.VRTrackedCameraFrameType_Undistorted
    frame_size = camera.getCameraFrameSize(0,frame_type)
    frame_buffer = (ctypes.c_uint8 * frame_size[2])()
    
    frame_header = openvr.VRTextureBounds_t()
    
    while True:
        try:
            result = camera.getVideoStreamFrameBuffer(camera_handle, frame_type, frame_buffer, frame_size[2])
            original_matrix = np.frombuffer(frame_buffer, dtype=np.uint8)
            
            #matriz_reshaped[:, :, 3] = 255
            matriz_reshaped = np.reshape(original_matrix, (2, 1126080, 4))
            imagen_ambas_no_dist = Image.frombuffer("RGBA", (1224,1840), matriz_reshaped, "raw")
            imagen_derecha_no_dist = Image.frombuffer("RGBA", (1224,920), matriz_reshaped[0], "raw")
            imagen_izquierda_no_dist = Image.frombuffer("RGBA", (1224,920), matriz_reshaped[1], "raw")
            imagen_izquierda_no_dist.save("camera_izq_no_dist.png")
            imagen_derecha_no_dist.save("camera_der_no_dist.png")
            imagen_ambas_no_dist.save("camera_ambas_no_dist.png")
        except openvr.error_code.TrackedCameraError as e:
            print(f"TrackedCameraError: {e}")
        
        
        time.sleep(0.016) 


    
    
    
if __name__ == "__main__":
    main()