import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
from time import time
import datetime
from statistics import mode
print("started")

ultimo = 0
identificados = []

# Ler opção 
retorno = 0
def identificar_numero(mensagem, operacao):
    global ultimo  # Indica que a variável `ultimo` é global

    tempo_leitura = datetime.timedelta(seconds=10)
    start = time
    start_time = datetime.datetime.now()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while (datetime.datetime.now() - start_time) < tempo_leitura:
            
        try:  
            ret, frame = cap.read()
            frame=cv2.flip(frame,1)
            cv2.putText(frame, mensagem,(0,50), font, 1, (255,0,0), 3, cv2.LINE_AA)
            cv2.putText(frame, operacao,(0,150), font, 1, (255,0,0), 3, cv2.LINE_AA)
            kernel = np.ones((3,3),np.uint8)
            
            # Definir região da mão
            roi=frame[100:300, 100:300]
            
            
            cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # HSV da cor de pele
            lower_skin = np.array([0,20,70], dtype=np.uint8)
            upper_skin = np.array([20,255,255], dtype=np.uint8)
            
        # segmentação pela cor de pele
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
        # extrapolar a mão para preencher as sombras dentro dela
            mask = cv2.dilate(mask,kernel,iterations = 4)
            
        # blur
            mask = cv2.GaussianBlur(mask,(9,9),100) 
            
        # contornos
            contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            #aproximação dos contornos
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
            epsilon = 0.0005*cv2.arcLength(cnt,True)
            approx= cv2.approxPolyDP(cnt,epsilon,True)
        
            
        # convex hull da mão
            hull = cv2.convexHull(cnt)
            
        # obter area do hull e area do contorno da mão
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)
        
        # proporção de area "sobrando" no convex hull (diferença do convex hull e contorno da mão)
            arearatio=((areahull-areacnt)/areacnt)*100
        
        # "defects" do convex hull são regiões do convex hull que 
        # não fazem parte do contorno da mao, a diferença dos dois contornos.
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)
            
        # numero de dedos
            l=0
            
        # encontrando o numero de defects entre os dedos do contorno
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt= (100,180)
                
                
                # encontrando a dimensão de todos os lados do triângulo entre os dedos (defect)
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                
                # distancia entre ponto e convex hull
                d=(2*ar)/a
                
                # a regra dos cossenos será usada para descobrir o angulo entre os defects
                # Quando o defect tiver angulo menor que 90° significa que é um angulo entre os dedos
                # isso permite contar quantos dedos estão na imagem.
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                
            
                # ignorar ruidos e angulos menores que 90°
                if angle <= 90 and d>30:
                    l += 1
                    cv2.circle(roi, far, 3, [0,0,255], -1)
                
                # desenhar convex hull
                cv2.line(roi,start, end, [0,255,0], 2)
                
                
            l+=1
            
            # Identificando os gestos correspondentes a quantidade de "dedos"
            if l==1:
                if areacnt<2000:
                    cv2.putText(frame,'Coloque a mao na caixa',(0,300), font, 1, (255,0,0), 3, cv2.LINE_AA)
                else:
                    cv2.putText(frame,'1',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                    identificados.append(1)
        
                        
            elif l==2:
                if arearatio<40:
                    cv2.putText(frame,'2',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                    identificados.append(2)
                
            elif l==3:         
                if arearatio<27:
                        cv2.putText(frame,'3',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                        identificados.append(3)
                        
            elif l==4:
                cv2.putText(frame,'4',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                identificados.append(4)
                
            elif l==5:            
                cv2.putText(frame,'5',(0,100), font, 1, (255,0,0), 3, cv2.LINE_AA)
                identificados.append(5)
                          
            else :
                cv2.putText(frame,'reposicione',(10,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                
            # Mostrar nas janelas
            cv2.imshow('mask',mask)
            cv2.imshow('frame',frame)
        except:
            pass
            
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

expressao = ""
identificar_numero("Informe o operando 1", expressao)
if(len(identificados) > 0):
    op_1 =  mode(identificados)
    print("Operando 1: " + str(op_1))
    identificados = []
    expressao = str(op_1)
    identificar_numero("Informe a operacao", expressao)
    if(len(identificados)>0):
        operacao = mode(identificados)
        if(operacao == 1):
            expressao += " + "
        elif(operacao == 2):
                expressao += " - "
        elif(operacao == 3):
            expressao += " * "
        elif(operacao == 4):
            expressao += " / "
        identificados = []
        identificar_numero("Informe o operando 2", expressao)
        if(len(identificados)>0):
            op_2 =  mode(identificados)
            print("Operando 2: " + str(op_2))
            resultado = 0
            if(operacao == 1):
                resultado = op_1 + op_2
            elif(operacao == 2):
                resultado = op_1 - op_2
            elif(operacao == 3):
                resultado = op_1 * op_2
            elif(operacao == 4):
                resultado = op_1 / op_2
            expressao = expressao + str(op_2) + " = " + str(resultado)
            identificar_numero("Resultado", expressao)            
            print(expressao)
        else:                         
            print("Nenhum número identificado")
else:
    print("Nenhum número identificado")



cv2.destroyAllWindows()
cap.release() 
