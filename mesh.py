from text_parser import obj_parser
import numpy as np
import cv2
import math

class Mesh():
    def __init__(self,filename,color):
        #This are the attributes we need
        self.vertexs=obj_parser(filename)
        self.color=color
        self.model=np.identity(4)
    
    #This function modifies the model by translating each point in a given direction.
    def translate(self,x,y,z):
        trans_matrix=np.identity(4)
        trans_matrix[3][0]=x
        trans_matrix[3][1]=y
        trans_matrix[3][2]=z
        self.model=np.matmul(trans_matrix,self.model)
    
    #This function modifies the model by changing the proportions of the object.
    def scale(self,x,y,z):
        scale_matrix=np.identity(4)
        scale_matrix[0][0]=x
        scale_matrix[1][1]=y
        scale_matrix[2][2]=z
        self.model=np.matmul(scale_matrix,self.model)
        
    #This function modifies the model by rotating each point in a given angle and axis.
    def rotate(self,angle,direction):
        if direction[0]==1:
            rotate_x=np.array([[1,0,0,0],[0,math.cos(angle),-math.sin(angle),0],[0,math.sin(angle),math.cos(angle),0],[0,0,0,1]])
            self.model=np.matmul(rotate_x,self.model)
        elif direction[1]==1:
            rotate_y=np.array([[math.cos(angle),0,-math.sin(angle),0],[0,1,0,0],[math.sin(angle),0,math.cos(angle),0],[0,0,0,1]])
            self.model=np.matmul(rotate_y,self.model)
        elif direction[2]==1:
            rotate_z=np.array([[math.cos(angle),-math.sin(angle),0,0],[math.sin(angle),math.cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
            self.model=np.matmul(rotate_z,self.model)
    
    
    #Returns an image with the object rendered.
    def render(self,img1,c,VP):
        #Each point is multiplied by the VP matrix
        #Then it is transformed from homogenous space to clip space (normalizing over the fourth component)
        #Finally each point has assigned a screen coordinate (in case in clip space it is between -1 and 1) and it is painted
        VP=np.matmul(self.model,VP)
        for i in range(0, len(self.vertexs)):
            result=np.matmul(np.array([float(self.vertexs[i][0]),float(self.vertexs[i][1]),float(self.vertexs[i][2]),1]),VP)
            for j in range(0,3):
                result[j]=result[j]/result[3]
            clipvector=[result[0]/result[2],result[1]/result[2]]
            if(clipvector[0]>=-1 and clipvector[0]<=1 and clipvector[1]>=-1 and clipvector[1]<=1):
                fbpoint=[c.lim1-clipvector[0]*c.lim1,c.lim2-clipvector[1]*c.lim2]
                cv2.circle(img1,(int(fbpoint[0]),int(fbpoint[1])), 1, self.color, -1)
        return img1
    