import cv2
import numpy as np
import imutils
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Carregar as imagens de treinamento e seus rótulos
imagens_treinamento = []
rotulos_treinamento = []

#Dimensões
x = 100
y = 100
largura = 200
altura = 200

# Carregar imagens positivas (sinais)
for i in range(1, 6):
    imagem = cv2.imread(f"imagens/positivas/sinal_{i}.jpg", 0)  # Substitua pelo caminho correto das imagens
    imagem_redimensionada = cv2.resize(imagem, (300, 300))
    imagens_treinamento.append(imagem_redimensionada)
    rotulos_treinamento.append(1)

# Carregar imagens negativas (não sinais)
for i in range(1, 6):
    imagem = cv2.imread(f"imagens/negativas/nao_sinal_{i}.jpg", 0)  # Substitua pelo caminho correto das imagens
    imagem_redimensionada = cv2.resize(imagem, (300, 300))
    imagens_treinamento.append(imagem_redimensionada)
    rotulos_treinamento.append(0)

# Converter as imagens em um formato adequado para o classificador SVM
imagens_treinamento = np.array(imagens_treinamento).reshape(len(imagens_treinamento), -1)

# Carregar a imagem para classificação
imagem_teste = cv2.imread('imagens/trois.jpg', 0)  # Substitua pelo caminho correto da imagem de teste
imagem_teste_redimensionada = cv2.resize(imagem_teste, (300, 300))

# Converter a imagem de teste em um formato adequado para o classificador SVM
imagem_teste = np.array(imagem_teste_redimensionada).reshape(1, -1)

# Carregar o classificador SVM treinado
classificador = svm.SVC(kernel='linear')
classificador.fit(imagens_treinamento, rotulos_treinamento)

# Louco
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(imagens_treinamento, rotulos_treinamento, test_size=0.1, random_state=42)
rotulo_teste = y_teste[0]

# Realizar a previsão na imagem de teste
previsao = classificador.predict(X_teste)

# Verificar se a imagem é um símbolo correto ou não
if previsao == 1:
    print("A imagem é um símbolo correto.")
else:
    print("A imagem não é um símbolo correto.")