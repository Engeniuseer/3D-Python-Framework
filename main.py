import cv2 
import math
import numpy as np
import time
import keyboard

from text_parser import obj_parser
from camera import Camera
from mesh import Mesh

#Screen size
window_width=800
window_height=600


def main():
    print('Loading all components...')
    c=Camera(60,0.1,500,np.array([0,10,20]),np.array([0,10,0]),np.array([0,1,0]),window_width, window_height)
    human=Mesh('data/BodyMesh.obj.txt',(0,0,255))
    tree=Mesh('data/lowpolytree.obj.txt',(0,255,0))
    print('All components loaded!')
    human.rotate(np.pi,[0,1,0])
    tree.translate(3,0,-30)
    tree.scale(3,3,3)
    VP=c.get_view_projection_matrix()
    last_frame=time.perf_counter()
    while True:
        '''
        RENDER: Displaying the final image
        '''
        img1=np.zeros((window_height,window_width,3))
        img1=human.render(img1,c,VP)
        img1=tree.render(img1,c,VP)
        cv2.imshow('3D Python Framework',img1)
        
        '''
        UPDATE: Apply changes in the objects for the next displayed frame
        '''
        #Calculating the seconds elapsed between two consecutives frames is very useful 
        sec_elapsed=time.perf_counter()-last_frame
        
        #Updating the view projection matrix
        #In case the camera is not changed is not necessary
        VP=c.get_view_projection_matrix()
        
        #Examples of the basic model modifications
        #face.model=np.identity(4)
        #face.translate(0,0,5)
        #face.scale(0.5,0.5,0.5)
        #face.rotate(sec_elapsed*0.08,[0,1,0]) 
        
        
        #Examples of updating camera attributes
        #c.eye=np.array([0,10+math.sin(sec_elapsed)*3,60])
        #c.fov=60+math.sin(sec_elapsed)*3
        
        
        #USER INTERACTION
        if cv2.waitKey(33)==27:    # Esc key to stop the execution
            print('Execution stopped successfully')
            cv2.destroyAllWindows()
            break
        elif keyboard.is_pressed('UP'):
            human.translate(0,0,1)
            tree.rotate(-sec_elapsed*0.03,[0,1,0])
        elif keyboard.is_pressed('DOWN'):
            human.translate(0,0,-1)
            tree.rotate(-sec_elapsed*0.03,[0,1,0])
        if keyboard.is_pressed('LEFT'): 
            human.rotate(-sec_elapsed*0.03,[0,1,0])
            tree.rotate(-sec_elapsed*0.03,[0,1,0])
        elif keyboard.is_pressed('RIGHT'):
            human.rotate(sec_elapsed*0.03,[0,1,0])
            tree.rotate(-sec_elapsed*0.03,[0,1,0])
        

if __name__=="__main__":
    main()