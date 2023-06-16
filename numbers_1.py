import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
from time import time
import datetime
from statistics import mode
print("started")
     
# image = cv2.imread('pic.jpg')
# cv2.namedWindow("imagem", cv2.WINDOW_GUI_EXPANDED)
# cv2.imshow('img',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

ultimo = 0
identificados = []

# Ler opção 
retorno = 0
def identificar_numero(mensagem):
    global ultimo  # Indica que a variável `ultimo` é global

    tempo_leitura = datetime.timedelta(seconds=10)
    start = time
    start_time = datetime.datetime.now()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while (datetime.datetime.now() - start_time) < tempo_leitura:
            
        try:  #an error comes if it does not find anything in window as it cannot find contour of max area
            #therefore this try error statement
            
            ret, frame = cap.read()
            frame=cv2.flip(frame,1)
            cv2.putText(frame, mensagem,(0,50), font, 1, (255,0,0), 3, cv2.LINE_AA)
            kernel = np.ones((3,3),np.uint8)
            
            #define region of interest
            roi=frame[100:300, 100:300]
            
            
            cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)    
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            
            
        # define range of skin color in HSV
            lower_skin = np.array([0,20,70], dtype=np.uint8)
            upper_skin = np.array([20,255,255], dtype=np.uint8)
            
        #extract skin color image 
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
    
            
        #extrapolate the hand to fill dark spots within
            mask = cv2.dilate(mask,kernel,iterations = 4)
            
        #blur the image
            mask = cv2.GaussianBlur(mask,(9,9),100) 
            
            
            
        #find contours
            contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
    #find contour of max area(hand)
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
            
        #approx the contour a little
            epsilon = 0.0005*cv2.arcLength(cnt,True)
            approx= cv2.approxPolyDP(cnt,epsilon,True)
        
            
        #make convex hull around hand
            hull = cv2.convexHull(cnt)
            
        #define area of hull and area of hand
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)
        
        #find the percentage of area not covered by hand in convex hull
            arearatio=((areahull-areacnt)/areacnt)*100
        
        #find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)
            
        # l = no. of defects
            l=0
            
        #code for finding no. of defects due to fingers
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt= (100,180)
                
                
                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                
                #distance between point and convex hull
                d=(2*ar)/a
                
                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                
            
                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d>30:
                    l += 1
                    cv2.circle(roi, far, 3, [0,0,255], -1)
                
                #draw lines around hand
                cv2.line(roi,start, end, [0,255,0], 2)
                
                
            l+=1
            
            #print corresponding gestures which are in their ranges
            if l==1:
                if areacnt<2000:
                    cv2.putText(frame,'Put hand in the box',(0,50), font, 1, (255,0,0), 3, cv2.LINE_AA)
                else:
                    # if arearatio<10:
                    #     cv2.putText(frame,'fist vertical',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                    # elif arearatio<18:
                    #     cv2.putText(frame,'thumbs down',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                    # elif arearatio<27:
                    #     cv2.putText(frame,'Best of luck',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                    # else:
                        cv2.putText(frame,'1',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                        ultimo = 1
                        identificados.append(1)
            
                        
            elif l==2:
                if arearatio<40:
                    cv2.putText(frame,'2',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                    ultimo = 2
                    identificados.append(2)
                # else:
                #     cv2.putText(frame,'L',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)

                
            elif l==3:         
                if arearatio<27:
                        cv2.putText(frame,'3',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                        ultimo = 3
                        identificados.append(3)
                #   else:
                #         cv2.putText(frame,'ok',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                        
            elif l==4:
                cv2.putText(frame,'4',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                ultimo = 4
                identificados.append(4)
                
            elif l==5:            
                cv2.putText(frame,'5',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                ultimo = 5
                identificados.append(5)
                
            # elif l==6:
            #     cv2.putText(frame,'reposition',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                
            else :
                cv2.putText(frame,'reposition',(10,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                
            #show the windows
            cv2.imshow('mask',mask)
            cv2.imshow('frame',frame)
        except:
            pass
            
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

identificar_numero("Informe a operacao, seu corno")
if(len(identificados)>0):    
        print("Identificou corretamente: " + str(ultimo))
        opcao = mode(identificados)
        if(opcao == 1): # SOMA
            identificados = []
            identificar_numero("Informe o operando 1")
            if(len(identificados)>0):                
                    op_1 =  mode(identificados)
                    print("Operando 1: " + str(op_1))
                    identificados = []
                    identificar_numero("Informe o operando 2")
                    if(len(identificados)>0):
                            op_2 =  mode(identificados)
                            print("Operando 2: " + str(op_2))
                            print(str(op_1) + " + " + str(op_2) + " = " + str(op_1+op_2))       

cv2.destroyAllWindows()
cap.release() 
