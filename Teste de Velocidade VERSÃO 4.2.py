import cv2
import time
import os
from datetime import datetime

# Carrega o classificador
classifier_path = r"C:\Users\Revlo-Marketing\Desktop\Projeto_Ca\haarcascade_car.xml"
classifier = cv2.CascadeClassifier(classifier_path)

# Distância em metros entre dois pontos de referência
distancia = 2  # Ajuste conforme necessário
velocidade_limite = 60  # Limite de velocidade em KM/H
log_path = r"C:\\Users\\Revlo-Marketing\\Desktop\\Projeto_Ca\\imagens_acima_limite"

# Função para criar pasta se não existir
def create_directory(path):
    os.makedirs(path, exist_ok=True)

def detecta_carros(frame):
    """Detecta carros em um frame e retorna suas posições."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converte o frame para escala de cinza
    carros = classifier.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=4, minSize=(60, 60))
    return carros

def calcular_velocidade(tempo):
    """Calcula a velocidade em MPH dado o tempo em segundos."""
    if tempo > 0:
        velocidade_mph = (distancia / tempo) * 2.23694  # Converte metros por segundo para milhas por hora
        return velocidade_mph
    return 0

def converter_mph_para_kmh(velocidade_mph):
    """Converte a velocidade de MPH para KM/H."""
    return velocidade_mph * 1.60934

def save_snapshot(frame, objectID, speed):
    """Salva uma imagem quando o carro ultrapassa o limite de velocidade."""
    snapshot_filename = f"carro_{objectID}_speed_{speed:.2f}KMH_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    snapshot_path = os.path.join(log_path, snapshot_filename)
    cv2.imwrite(snapshot_path, frame)
    print(f"[INFO] Imagem salva: {snapshot_path}")

def simulator(video):
    """Executa a simulação da detecção de carros em um vídeo."""
    if not video.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    create_directory(log_path)

    objectID = 0  # Identificador único para o carro

    while True:
        ret, frame = video.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler o frame.")
            break

        carros = detecta_carros(frame)
        for (x, y, w, h) in carros:
            objectID += 1  # Incrementa o ID do carro detectado
            # Desenha o retângulo ao redor do carro
            cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

            # Inicia o cálculo de tempo para a velocidade
            tempo_inicial = time.time()
            
            # Simulação de tempo até o carro sair da tela
            time.sleep(0.5)  # Simula o tempo em segundos que o carro leva para sair da tela

            tempo_final = time.time()
            tempo_passado = tempo_final - tempo_inicial
            velocidade_mph = calcular_velocidade(tempo_passado)
            velocidade_kmh = converter_mph_para_kmh(velocidade_mph)
            print(f"Velocidade: {velocidade_mph:.2f} MPH / {velocidade_kmh:.2f} KM/H")

            # Verifica se a velocidade ultrapassa o limite
            if velocidade_kmh > velocidade_limite:
                save_snapshot(frame, objectID, velocidade_kmh)

        # Mostra o frame com as detecções
        cv2.imshow('Detecção de Carros', frame)

        if cv2.waitKey(1) == ord('q'):  # Pressione 'q' para sair
            break

    video.release()
    cv2.destroyAllWindows()

# Inicia a captura de vídeo
def main():
    mode = input("Digite 'c' para usar a câmera ou 'v' para usar um vídeo: ")
    
    try:
        if mode.lower() == 'c':
            video = cv2.VideoCapture(0)  # Webcam padrão
            print("[INFO] Inicializando webcam...")
        elif mode.lower() == 'v':
            video_path = r"C:\Users\Revlo-Marketing\Pictures\Camera Roll\WIN_20241010_11_28_19_Pro.mp4"
            video = cv2.VideoCapture(video_path)
            print("[INFO] Inicializando vídeo de teste...")
        else:
            raise ValueError("Modo inválido. Digite 'c' para câmera ou 'v' para vídeo.")

        simulator(video)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
