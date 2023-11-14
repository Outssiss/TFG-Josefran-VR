import openvr
import numpy as np
import time
from ctypes import *
from PIL import Image
import pygame as pg
from OpenGL import *
from OpenGL.GL import *
import glfw
import queue
import threading

class VRSAM:
    def __init__(self):
        self.vr_app_scene = openvr.init(openvr.VRApplication_Scene)
        
    def initCamera(self):
        self.camera = openvr.IVRTrackedCamera()
        self.camera_handle = self.camera.acquireVideoStreamingService(0)
        self.frame_type = openvr.VRTrackedCameraFrameType_Undistorted
        self.frame_size = self.camera.getCameraFrameSize(0,self.frame_type)
        self.frame_buffer = (ctypes.c_uint8 * self.frame_size[2])()
        self.frame_header = openvr.VRTextureBounds_t()

    def startCameraRecording(self, q ,saveFile=False):
        while True:
            try:
                result = self.camera.getVideoStreamFrameBuffer(self.camera_handle, self.frame_type, self.frame_buffer, self.frame_size[2])
                self.pyimage_ambos = pg.image.frombuffer(self.frame_buffer, 
                                              self.frame_size[:2],
                                              "RGBA")
                
                self.doOpenGLStuff(q)
                if saveFile: 
                    pg.image.save(self.pyimage_ambos, "./cameraImages/ambasNoDistortV1.png")
            except openvr.error_code.TrackedCameraError as e:
                print(f"TrackedCameraError: {e}")
            
        
    def initSubmit(self):
        self.IMG_WIDTH = 1224
        self.IMG_HEIGHT = 920
        pg.display.set_mode((0,0),pg.OPENGL|pg.DOUBLEBUF|pg.NOFRAME)
        glfw.init()
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(1, 1, 'hello_vr', None, None)   
        vr_sys = openvr.VRSystem()
        
    def doOpenGLStuff(self, q):
        #OpenGL stuff
        glfw.make_context_current(self.window) 
        if self.pyimage_ambos:
            img_data = pg.image.tostring(self.pyimage_ambos, "RGBA")
            img_data_izq, img_data_der = img_data[:len(img_data)//2], img_data[len(img_data)//2:]
            textures = glGenTextures(2)
            glBindTexture(GL_TEXTURE_2D, textures[0])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,self.IMG_WIDTH,self.IMG_HEIGHT,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data_izq)
            glGenerateMipmap(GL_TEXTURE_2D)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D,textures[0])
            
            self.left_eye_texture = openvr.Texture_t(
                    handle=int(textures[0]),
                    eType=openvr.TextureType_OpenGL,
                    eColorSpace=openvr.ColorSpace_Gamma,
                )
            q.put(self.left_eye_texture)
            glBindTexture(GL_TEXTURE_2D, textures[1])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,self.IMG_WIDTH,self.IMG_HEIGHT,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data_der)
            
            glGenerateMipmap(GL_TEXTURE_2D)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D,textures[1])
            
            self.right_eye_texture = openvr.Texture_t(
                        handle=int(textures[1]),
                        eType=openvr.TextureType_OpenGL,
                        eColorSpace=openvr.ColorSpace_Gamma,
                )
            q.put(self.right_eye_texture)
        
    def beginSubmit(self, q):
        poses = []
        while not glfw.window_should_close(self.window):
            try:
                self.left_eye_texture = q.get()
                self.right_eye_texture = q.get()
                openvr.VRCompositor().submit(openvr.Eye_Left, self.left_eye_texture)
                openvr.VRCompositor().submit(openvr.Eye_Right, self.right_eye_texture)
            except openvr.error_code.CompositorError_DoNotHaveFocus:
                pass  # First frame fails because waitGetPoses has not been called yet
        
            poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
        
        
        
    

if __name__ == "__main__":
   
    q = queue.Queue()
    vrsam = VRSAM()
    vrsam.initCamera()
    vrsam.initSubmit()
    
    pr1 = threading.Thread(target=vrsam.startCameraRecording, args=(q,))
    pr2 = threading.Thread(target=vrsam.beginSubmit, args=(q,))
    pr1.start()
    pr2.start()
    
    
    