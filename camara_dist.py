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
    
    frame_type = openvr.VRTrackedCameraFrameType_Distorted
    frame_size = camera.getCameraFrameSize(0,frame_type)
    frame_buffer = (ctypes.c_uint8 * frame_size[2])()
    
    frame_header = openvr.VRTextureBounds_t()
    
    while True:
        try:
            result = camera.getVideoStreamFrameBuffer(camera_handle, frame_type, frame_buffer, frame_size[2])
            original_matrix = np.frombuffer(frame_buffer, dtype=np.uint8)
            matriz_reshaped = np.reshape(original_matrix, (1, 563040, 4))
            matriz_reshaped[:, :, 3] = 255
            matriz_reshaped = np.reshape(matriz_reshaped, (2, 281520, 4))
            imagen_ambas_dist = Image.frombuffer("RGBA", (612,920), matriz_reshaped, "raw")
            imagen_derecha = Image.frombuffer("RGBA", (612,460), matriz_reshaped[0], "raw")
            imagen_izquierda = Image.frombuffer("RGBA", (612,460), matriz_reshaped[1], "raw")
            imagen_derecha.save("camera_der_dist.png")
            imagen_izquierda.save("camera_izq_dist.png")
            imagen_ambas_dist.save("camera_ambas_dist.png")
        except openvr.error_code.TrackedCameraError as e:
            print(f"TrackedCameraError: {e}")
        
        # Espera un tiempo antes de intentar capturar el siguiente fotograma
        time.sleep(0.1)  # Espera aproximadamente 16 ms (60 FPS)


    
    
    
if __name__ == "__main__":
    main()