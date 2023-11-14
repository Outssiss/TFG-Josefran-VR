import openvr
import pygame as pg
from OpenGL import *
from OpenGL.GL import *
import numpy as np
import glfw
from ctypes import c_float, c_uint16, c_void_p, cast, sizeof
from PIL import Image

def main():
    
    pg.display.set_mode((0,0),pg.OPENGL|pg.DOUBLEBUF)
    
    poses = []

    if openvr.isHmdPresent():
        print("VR head set found")
        
    if openvr.isRuntimeInstalled():
        print("Runtime is installed")
    
    glfw.init()
    glfw.window_hint(glfw.SAMPLES, 4)
    window = glfw.create_window(1, 1, 'hello_vr', None, None)
    glfw.make_context_current(window)
    
    hmd = openvr.init(openvr.VRApplication_Scene)
    vr_sys = openvr.VRSystem()
    
    textures = glGenTextures(2)
    
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image_izq = pg.image.load("camera_izq_no_dist.png").convert_alpha()
    image_width_izq,image_height_izq = image_izq.get_rect().size
    img_data_izq = pg.image.tostring(image_izq,'RGBA',1)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width_izq,image_height_izq,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data_izq)
    glGenerateMipmap(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D,textures[0])
    
    left_eye_texture = openvr.Texture_t(
                handle=int(textures[0]),
                eType=openvr.TextureType_OpenGL,
                eColorSpace=openvr.ColorSpace_Gamma,
            )
    
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image_der = pg.image.load("camera_der_no_dist.png").convert_alpha()
    image_width_der,image_height_der = image_der.get_rect().size
    img_data_der = pg.image.tostring(image_der,'RGBA', 1)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width_der,image_height_der,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data_der)
    glGenerateMipmap(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D,textures[1])
    
    right_eye_texture = openvr.Texture_t(
                handle=int(textures[1]),
                eType=openvr.TextureType_OpenGL,
                eColorSpace=openvr.ColorSpace_Gamma,
            )
    
    
    
    while not glfw.window_should_close(window):
        try:
            openvr.VRCompositor().submit(openvr.Eye_Left, left_eye_texture)
            openvr.VRCompositor().submit(openvr.Eye_Right, right_eye_texture)
        except openvr.error_code.CompositorError_DoNotHaveFocus:
            pass  # First frame fails because waitGetPoses has not been called yet
    
        poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)    
    
if __name__ == "__main__":
    main()