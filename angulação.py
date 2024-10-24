import cv2

# Variáveis globais para armazenar os dois pontos do quadrado
ponto_inicial = (0, 0)
ponto_final = (0, 0)
desenhando = False  # Variável para indicar se estamos desenhando o quadrado

# Função de callback para capturar eventos do mouse
def desenha_quadrado(event, x, y, flags, param):
    global ponto_inicial, ponto_final, desenhando

    if event == cv2.EVENT_LBUTTONDOWN:  # Quando o botão esquerdo é pressionado
        desenhando = True
        ponto_inicial = (x, y)  # Primeiro ponto do quadrado

    elif event == cv2.EVENT_MOUSEMOVE:  # Quando o mouse é movido
        if desenhando:
            ponto_final = (x, y)  # Atualiza o segundo ponto dinamicamente

    elif event == cv2.EVENT_LBUTTONUP:  # Quando o botão esquerdo é solto
        desenhando = False
        ponto_final = (x, y)  # Define o segundo ponto final
        cv2.rectangle(img, ponto_inicial, ponto_final, (0, 255, 0), 2)  # Desenha o quadrado
        print(f"Coordenadas do quadrado: {ponto_inicial} até {ponto_final}")
        cv2.imshow("Imagem", img)

# Carrega a imagem
img = cv2.imread(r"C:\Users\Revlo-Marketing\Downloads\photo-1553649033-3fbc8d0fa3cb.jpg")

# Mostra a imagem
cv2.imshow("Imagem", img)

# Define a função de callback para capturar eventos de mouse
cv2.setMouseCallback("Imagem", desenha_quadrado)

# Aguarda a tecla ESC para fechar a janela
cv2.waitKey(0)
cv2.destroyAllWindows()
