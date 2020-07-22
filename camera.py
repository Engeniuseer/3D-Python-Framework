import cv2 
import math
import numpy as np
import time

class Camera:
    def __init__(self,fov,near,far,eye,center,up,window_width, window_height):
        #This are all attributes needed to create a 3D camera with perspective.
        self.fov=fov
        self.aspect=window_width/window_height
        self.near=near
        self.far=far
        self.eye=eye
        self.center=center
        self.up=up
        self.lim1=window_width/2
        self.lim2=window_height/2
        
    def get_projection_matrix(self):
        f=1/math.tan(math.radians(self.fov)/2)
        P=np.array([[f/self.aspect,0,0,0],[0,f,0,0],[0,0,(self.far+self.near)/(self.near-self.far),(2*self.far*self.near)/(self.near-self.far)],[0,0,-1,0]])
        return P
    
    def get_view_matrix(self):
        front=self.center-self.eye
        if np.linalg.norm(front)>0:
            front=front/np.linalg.norm(front)

        side=np.cross(front,self.up)
        if np.linalg.norm(side)>0:
            side=side/np.linalg.norm(side)

        top=np.cross(side,front)
        V=np.array([[side[0],side[1],side[2],-self.eye[0]],[top[0],top[1],top[2],-self.eye[1]],[-front[0],-front[1],-front[2],-self.eye[2]],[0,0,0,1]])
        V=V.T
        return V
    
    #The view projection matrix is used to project 3D points into 2D space.
    #Dimension 4x4
    def get_view_projection_matrix(self):
        P=self.get_projection_matrix()
        V=self.get_view_matrix()
        VP=np.matmul(V,P)
        return VP