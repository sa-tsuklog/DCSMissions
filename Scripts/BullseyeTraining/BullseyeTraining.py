'''
Created on 2021/02/08

@author: sa
'''

import cv2
import numpy as np

RANGE_SCALE = 40
DEP = False


def genHsi(hsiSize,radHeading):
    hsi = np.zeros((hsiSize,hsiSize,3),dtype=np.uint8)
    
    angles = ["N","3","6","E","12","15","S","21","24","W","30","33"]
    angleLen=[1,  1,  1,  1,  2,   2,   1,    2,  2,   1,  2,   2]
    for i in range(12):
        tmp = np.zeros((hsiSize,hsiSize,3),dtype=np.uint8)*255
        if(angleLen[i] == 1):
            offset = 16
        else:
            offset = 30
        cv2.putText(tmp,angles[i],(hsiSize//2-offset,int(hsiSize*0.13)),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),1)
        trans = cv2.getRotationMatrix2D((hsiSize//2,hsiSize//2),-30*i,1.0)
        tmp = cv2.warpAffine(tmp,trans,(hsiSize,hsiSize));
        hsi = hsi+tmp
    
    for i in range(36):
        x0 = hsiSize/2 * np.sin(i*10/180*np.pi)
        y0 = hsiSize/2 * np.cos(i*10/180*np.pi)
        x1 = x0*0.9
        y1 = y0*0.9
        
        cv2.line(hsi,(int(x0+hsiSize/2),int(y0+hsiSize/2)),(int(x1+hsiSize/2),int(y1+hsiSize/2)),(255,255,255),1)
    
    for i in range(36):
        x0 = hsiSize/2 * np.sin((i*10+5)/180*np.pi)
        y0 = hsiSize/2 * np.cos((i*10+5)/180*np.pi)
        x1 = x0*0.95
        y1 = y0*0.95
        
        cv2.line(hsi,(int(x0+hsiSize/2),int(y0+hsiSize/2)),(int(x1+hsiSize/2),int(y1+hsiSize/2)),(255,255,255),1)
    
    trans = cv2.getRotationMatrix2D((hsiSize//2,hsiSize//2),radHeading*180/np.pi,1.0)
    hsi = cv2.warpAffine(hsi,trans,(hsiSize,hsiSize))
    
    
    return hsi


def genHsd(hsdSize,bluePosX,bluePosY,blueHidden,redPosX,redPosY,bullseyePosX,bullseyePosY):
    hsd = np.zeros((hsdSize,hsdSize,3),dtype=np.uint8)
    
    cv2.putText(hsd,str(RANGE_SCALE),(20,180),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),1)
    cv2.rectangle(hsd,(0,0),(hsdSize-1,hsdSize-1),(255,255,255),1)
    
    
    ########################################
    # Range Circle
    ########################################
    cv2.circle(hsd,(hsdSize//2,hsdSize//2),hsdSize//2-1,(255,0,128),1)
    cv2.circle(hsd,(hsdSize//2,hsdSize//2),hsdSize//4,(255,0,128),1)
    cv2.drawMarker(hsd,(hsdSize//2,hsdSize//2),(255,0,128),cv2.MARKER_CROSS,markerSize=20,thickness=1)
    
    ########################################
    # Red
    ########################################
    cv2.drawMarker(hsd,(int(hsdSize*redPosX),int(hsdSize*redPosY)),(0,0,255),cv2.MARKER_TRIANGLE_UP,markerSize=30,thickness=2)
    
    
    ########################################
    # Bullseye
    ########################################
    cv2.circle(hsd,(int(hsdSize*bullseyePosX),int(hsdSize*bullseyePosY)),8,(255,80,80),thickness=1)
    cv2.circle(hsd,(int(hsdSize*bullseyePosX),int(hsdSize*bullseyePosY)),16,(255,80,80),thickness=1)
    
    ########################################
    # Blue
    ########################################
    if(not blueHidden):
        cv2.circle(hsd,(int(hsdSize*bluePosX),int(hsdSize*bluePosY)),16,(0,255,0),thickness=2)
    
    return hsd

def nextProblem(count,radHeading,bluePosX,bluePosY,blueHidden,redPosX,redPosY,bullseyePosX,bullseyePosY,printBraa):
    hsiSize = 400
    hsdSize = 800
    img = np.zeros((1080,1920,3),dtype=np.uint8)
    
    hsi = genHsi(hsiSize,radHeading)
    hsd = genHsd(hsdSize,bluePosX,bluePosY,blueHidden,redPosX,redPosY,bullseyePosX,bullseyePosY)
    
    
    
    hsiOffsetX = 50
    hsiOffsetY = 280
    
    hsdOffsetX = hsiSize + hsiOffsetX + 100
    hsdOffsetY = 210
    img[hsiOffsetY:hsiOffsetY+hsiSize,hsiOffsetX:hsiOffsetX+hsiSize,:] = hsi
    img[hsdOffsetY:hsdOffsetY+hsdSize,hsdOffsetX:hsdOffsetX+hsdSize,:] = hsd
    
    headingTextOffsetX = 50
    headingTextOffsetY = hsiOffsetY + hsiSize + 100
    degHeading = int(radHeading*180/np.pi)
    degHeading = degHeading%360
    while(degHeading < 0):
        degHeading += 360
    
    cv2.putText(img,"heading"+str(degHeading),(headingTextOffsetX,headingTextOffsetY),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),1)
    
    
    degBlueDirBullseye = int((np.arctan2(bluePosY-bullseyePosY,bluePosX-bullseyePosX)+np.pi/2+radHeading)*180/np.pi)
    blueRangeBullseye = RANGE_SCALE*2 * np.sqrt((bluePosX-bullseyePosX)**2 + (bluePosY-bullseyePosY)**2)
    degBlueDirBullseye = degBlueDirBullseye%360
    while(degBlueDirBullseye<0):
        degBlueDirBullseye += 360
    
#     print("dir:",radBlueDirBullseye*180/np.pi)
#     print("range:",blueRangeBullseye)
    bullseyeTextOffsetX = 30
    bullseyeTextOFfsetY = 100
    bullseyeText = str(count)+": bullseye "+str(degBlueDirBullseye)+","+str(int(blueRangeBullseye))
    cv2.putText(img,bullseyeText,(bullseyeTextOffsetX,bullseyeTextOFfsetY),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),1)
    
    braaBearing = int((np.arctan2(redPosY-bluePosY,redPosX-bluePosX)+np.pi/2+radHeading)*180/np.pi)
    braaRange   = int(RANGE_SCALE*2 * np.sqrt((redPosX-bluePosX)**2 + (redPosY-bluePosY)**2))
    braaBearing = braaBearing%360
    while(braaBearing < 0):
        braaBearing += 360
    
    if(printBraa):
        print(count,": BRA",braaBearing," for ",braaRange)
    
    cv2.imshow("bullseye",img);
    c = cv2.waitKey()
    
    return c

if __name__ == "__main__":
    c1 = ord(' ')
    c2 = ord(' ')
    
    count = 0
    
    while(c1 != ord('q') and c2 != ord('q')):
        count += 1
        radHeading = np.random.rand() * np.pi*2
    
        bluePosX = np.random.rand()
        bluePosY = np.random.rand()
        redPosX = np.random.rand()
        redPosY = np.random.rand()
        bullseyePosX = np.random.rand()
        bullseyePosY = np.random.rand()
        
        
        
        c1 = nextProblem(count,radHeading,bluePosX,bluePosY,True,redPosX,redPosY,bullseyePosX,bullseyePosY,False)
        c2 = nextProblem(count,radHeading,bluePosX,bluePosY,False,redPosX,redPosY,bullseyePosX,bullseyePosY,True)
    
    
    
    