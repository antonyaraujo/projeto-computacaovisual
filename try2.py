import cv2
from skimage import feature

def reconhecer_simbolo_libras():
    # Carregar a imagem contendo o símbolo da Libras
    imagem = cv2.imread('tres.jpg')  # Substitua pelo caminho correto da imagem

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar o detector de bordas Canny
    bordas = feature.canny(imagem_cinza)

    # Verificar se existem bordas presentes na imagem
    if bordas.any():
        # Exemplo de reconhecimento: verificar se há bordas suficientes
        quantidade_bordas = bordas.sum()
        cv2.imshow("Image", imagem_cinza)
        cv2.waitKey(0)
        if quantidade_bordas > 100:
            print("Símbolo da Libras reconhecido")
        else:
            print("Símbolo da Libras não reconhecido")
    else:
        print("Bordas não encontradas na imagem")

# Chamada da função
reconhecer_simbolo_libras()
