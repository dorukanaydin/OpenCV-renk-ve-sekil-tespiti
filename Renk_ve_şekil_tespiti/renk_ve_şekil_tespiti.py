from operator import length_hint
import numpy as np
import cv2

#Webcam görüntüsündeki 4 rengi(mavi,yeşil,kırmızı,sarı) dikdörtgen veya daire içine alıp cismin adını, rengini ve ağırlık merkezini gösteren program 

"""
Renklerin filtre değerlerinin bulunması:

blue = np.uint8([[[255,0,0]]])
hsv_blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
print(hsv_blue)
[[[ 120 255 255]]]

green = np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)
[[[ 60 255 255]]]

red = np.uint8([[[0,0,255]]])
hsv_red = cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
print(hsv_red)
[[[ 0 255 255]]]

yellow = np.uint8([[[0,255,255]]])
hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)print(hsv_blue)
#[[[ 30 255 255]]]

"""

#lower = [H-10, 100,100]
#upper = [H+10, 255, 255]
 
red_lower = np.array([0, 100, 100],np.uint8)
red_upper = np.array([10, 255, 255],np.uint8)
 
green_lower = np.array([50, 100, 100])
green_upper = np.array([100, 255, 255])	
 
blue_lower=np.array([100,100,100],np.uint8)
blue_upper=np.array([200,255,255],np.uint8)
 
yellow_lower=np.array([20,100,100],np.uint8)
yellow_upper=np.array([40,255,255],np.uint8)
 
cam=cv2.VideoCapture(0)

def filtre(lower,upper):
    mask=None
    mask=cv2.inRange(hsv, lower, upper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    return mask

while(1):
    _,frame=cam.read()
    
    blur=cv2.GaussianBlur(frame,(5,5),0)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    red=filtre(red_lower,red_upper)
    green=filtre(green_lower,green_upper)
    blue=filtre(blue_lower,blue_upper)
    yellow=filtre(yellow_lower,yellow_upper)

#Kırmızı
    cntr, _ = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i,c in enumerate(cntr):
        if cv2.contourArea(c)<1000:
            continue

        peri=cv2.arcLength(c,True)
        approx =cv2.approxPolyDP(c,0.04*peri,True)
    
        if len(approx)==4:
            x,y,w,h=cv2.boundingRect(approx)		
            ar=w/float(h)
            shape="Kirmizi Kare" if ar>=0.95 and ar<=1.05 else "Kirmizi Dikdortgen"
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.putText(frame,shape,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        else:
            #print(len(cntr))
            #Ağırlık merkezi bulma ve daire çizimi 
            c=max(cntr,key=cv2.contourArea)
            ((x,y),radius)=cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx,cy)
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,0,255),3)
            cv2.circle(frame,center,5,(0,0,255),-1)
            cv2.putText(frame,"Kirmizi Daire",(cx,(cy-int(radius)-10)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

#Yeşil
    cntr,_ =cv2.findContours(green, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i,c in enumerate(cntr):
        if cv2.contourArea(c)<1000:
            continue

        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.04*peri,True)
        
        if len(approx)==4:
            x,y,w,h=cv2.boundingRect(approx)		
            ar=w/float(h)
            shape=" Yesil Kare" if ar>=0.95 and ar<=1.05 else "Yesil Dikdortgen"
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(frame,shape,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
        else:    
                      
            c=max(cntr,key=cv2.contourArea)
            ((x,y),radius)=cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx,cy)
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,0),3)
            cv2.circle(frame,center,5,(0,255,0),-1)
            cv2.putText(frame,"Yesil Daire",(cx,(cy-int(radius)-10)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            
                      
#Mavi 
    cntr,_=cv2.findContours(blue, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
 
    for i,c in enumerate(cntr):
        if cv2.contourArea(c)<1000:
            continue
        
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.04*peri,True)
        
        if len(approx)==4:
            x,y,w,h=cv2.boundingRect(approx)		
            ar=w/float(h)
            shape=" Mavi Kare" if ar>=0.95 and ar<=1.05 else "Mavi Dikdortgen"

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            cv2.putText(frame,shape,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        
        else:
            c=max(cntr,key=cv2.contourArea)
            ((x,y),radius)=cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx,cy)
            cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,0),3)
            cv2.circle(frame,center,5,(255,0,0),-1)
            cv2.putText(frame,"Mavi Daire",(cx,(cy-int(radius)-10)),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
               
#Sarı 
    cntr,_=cv2.findContours(yellow, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
 
    for i,c in enumerate(cntr):
        if cv2.contourArea(c)<1000:
            continue
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.04*peri,True)
        
        if len(approx)==4:
            x,y,w,h=cv2.boundingRect(approx)		
            ar=w/float(h)
            shape=" Sari Kare" if ar>=0.95 and ar<=1.05 else "Sari Dikdortgen"
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),3)
            cv2.putText(frame,shape,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        else:
            
            c=max(cntr,key=cv2.contourArea)
            ((x,y),radius)=cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx,cy)
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),3)
            cv2.circle(frame,center,5,(0,255,255),-1)
            cv2.putText(frame,"Sari Daire",(cx,(cy-int(radius)-10)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
  
    cv2.imshow('frame',frame)
    if cv2.waitKey(33) & 0xFF == ord("q"):
        break
 
cam.release()
cv2.destroyAllWindows()