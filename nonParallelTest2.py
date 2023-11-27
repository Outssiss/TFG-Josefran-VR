import openvr
import numpy as np
import pygame as pg
from OpenGL.GL import *
import glfw

vr_app_scene = openvr.init(openvr.VRApplication_Scene)

camera = openvr.IVRTrackedCamera()
camera_handle = camera.acquireVideoStreamingService(0)
frame_type = openvr.VRTrackedCameraFrameType_Distorted
frame_size = camera.getCameraFrameSize(0, frame_type)
frame_buffer = (ctypes.c_uint8 * frame_size[2])()
print(frame_size[2])
frame_header = openvr.VRTextureBounds_t()

IMG_WIDTH = 612
IMG_HEIGHT = 460

pg.display.set_mode((0, 0), pg.OPENGL | pg.DOUBLEBUF | pg.NOFRAME)
glfw.init()
glfw.window_hint(glfw.SAMPLES, 4)
window = glfw.create_window(1, 1, 'hello_vr', None, None)
vr_sys = openvr.VRSystem()
left_eye_texture = None
right_eye_texture = None

poses = []

glfw.make_context_current(window)

# Rendering loop
while not glfw.window_should_close(window):
    try:
        # Update headset pose
        poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
        
        # Get camera frame
        result = camera.getVideoStreamFrameBuffer(camera_handle, frame_type, frame_buffer, frame_size[2])
        pyimage_ambos = pg.image.frombuffer(frame_buffer, frame_size[:2], "RGBA")

        if pyimage_ambos:
            img_data = pg.image.tostring(pyimage_ambos, "RGBA", 1)
            img_data_izq, img_data_der = img_data[:len(img_data)//2], img_data[len(img_data)//2:]
            textures = glGenTextures(2)

            # Left eye texture
            glBindTexture(GL_TEXTURE_2D, textures[0])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)
            glDepthFunc(GL_LEQUAL)
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,IMG_WIDTH,IMG_HEIGHT,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data_izq)
            # ... (texture parameters and data setup)

            left_eye_texture = openvr.Texture_t(
                handle=int(textures[0]),
                eType=openvr.TextureType_OpenGL,
                eColorSpace=openvr.ColorSpace_Gamma,
            )

            # Right eye texture
            glBindTexture(GL_TEXTURE_2D, textures[1])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)
            glDepthFunc(GL_LEQUAL)
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,IMG_WIDTH,IMG_HEIGHT,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data_der)
            # ... (texture parameters and data setup)

            right_eye_texture = openvr.Texture_t(
                handle=int(textures[1]),
                eType=openvr.TextureType_OpenGL,
                eColorSpace=openvr.ColorSpace_Gamma,
            )

            # Submit textures to VR compositor
            if right_eye_texture is not None and left_eye_texture is not None:
                try:
                    openvr.VRCompositor().submit(openvr.Eye_Left, left_eye_texture, submitFlags=openvr.Submit_LensDistortionAlreadyApplied)
                    openvr.VRCompositor().submit(openvr.Eye_Right, right_eye_texture, submitFlags=openvr.Submit_LensDistortionAlreadyApplied)
                except openvr.error_code.CompositorError_DoNotHaveFocus:
                    pass  # First frame fails because waitGetPoses has not been called yet

    except openvr.error_code.TrackedCameraError as e:
        print(f"TrackedCameraError: {e}")

    glfw.swap_buffers(window)
    glfw.poll_events()
