import cv2
import numpy as np
import os
from datetime import datetime

# Configurações iniciais
conf = {
    "max_disappear": 10,
    "distância_máxima": 175,
    "objeto_de_trilha": 4,
    "confiança": 0.9,
    "largura_do_quadro": 400,
    "zona_de_estimativa_de_velocidade": {"A": 120, "B": 160, "C": 200, "D": 240},
    "distância": 14,  # distância real em metros
    "limite_de_velocidade": 10  # em MPH
}

# Criação da pasta para salvar imagens
os.makedirs('imagens_Carros', exist_ok=True)

# Contador de carros
car_count = 0

# Função para calcular a velocidade com nova lógica (distância e tempo)
def calculate_speed_by_distance_time(start_time, end_time, distancia_real):
    time_elapsed = (end_time - start_time).total_seconds()
    if time_elapsed > 0:
        velocidade_mps = distancia_real / time_elapsed  # Velocidade em metros por segundo
        velocidade_mph = velocidade_mps * 2.23694  # Conversão para MPH
        return velocidade_mph
    return 0

# Função para converter MPH para KM/H
def convert_mph_to_kmh(speed_mph):
    return speed_mph * 1.60934  # 1 MPH = 1.60934 KM/H

# Função para registrar a velocidade em um arquivo de log
def log_speed(speed):
    with open("speed_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {speed:.2f} MPH\n")

# Função para tirar print da tela da câmera
def save_car_screenshot(frame, objectID):
    screenshot_name = f"imagens_carros/car_screenshot_{objectID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(screenshot_name, frame)
    print(f"[INFO] Print da tela salvo: {screenshot_name}")

# Função para inicializar a câmera
def initialize_camera(video_source):
    vs = cv2.VideoCapture(video_source)
    if not vs.isOpened():
        raise ValueError("Não foi possível abrir a câmera.")
    return vs

# Função para processar o quadro e desenhar o retângulo
def process_frame(frame, trackableObjects, bg_subtractor, metroPorPixel):
    global car_count  # Referencia a variável global
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fg_mask = bg_subtractor.apply(frame)
    blurred = cv2.GaussianBlur(fg_mask, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)

    # Dilatação para preencher pequenos buracos
    thresh = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = {}

    # Calculando a área da imagem para filtrar contornos
    frame_height, frame_width = frame.shape[:2]
    min_area = (frame_height * frame_width) * 0.01  # 1% da área total

    for c in contours:
        if cv2.contourArea(c) < min_area:  # Filtrando pequenos objetos/ruído
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        centroid = (int(x + w // 2), int(y + h // 2))
        objectID = len(objects) + 1
        objects[objectID] = centroid

        to = trackableObjects.get(objectID, None)
        if to is None:
            to = TrackableObject(objectID, centroid)

        # Estimativa de velocidade
        if to.lastPoint and not to.estimated:
            # Utilizando nova lógica de velocidade (tempo e distância)
            start_time = to.timestamp['A']
            end_time = to.timestamp['D']
            speed_mph = calculate_speed_by_distance_time(start_time, end_time, conf['distância'])
            speed_kmh = convert_mph_to_kmh(speed_mph)  # Conversão para KM/H
            
            to.speedMPH = speed_mph
            log_speed(to.speedMPH)  # Logar a velocidade
            to.estimated = True
            print(f"[INFO] Velocidade do veículo: {to.speedMPH:.2f} MPH | {speed_kmh:.2f} KM/H")
            if to.speedMPH > conf["limite_de_velocidade"]:
                print(f"[ALERT] Velocidade acima do limite: {to.speedMPH:.2f} MPH")
                save_car_screenshot(frame, to.objectID)  # Tirar print da tela do carro
                car_count += 1  # Incrementar contagem de carros

        trackableObjects[objectID] = to

        # Desenhar retângulo ao redor do objeto
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Desenhar o ID do objeto e o centroide
        text = f"ID {objectID}"
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # Exibir status de velocidade
        status_text = "Acima do limite" if to.speedMPH > conf["limite_de_velocidade"] else "Dentro do limite"
        cv2.putText(frame, f"Status: {status_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Exibir contagem de carros no prompt de comando
    print(f"[INFO] Carros detectados: {car_count} carros")

    return frame

# Classe para objetos rastreáveis
class TrackableObject:
    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.timestamp = {"A": datetime.now(), "B": datetime.now(), "C": datetime.now(), "D": datetime.now()}
        self.position = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.direction = None
        self.lastPoint = False
        self.estimated = False
        self.speedMPH = 0.0
        self.logged = False

# Função principal
def main():
    # Inicializando configurações e inputs
    try:
        conf["limite_de_velocidade"] = float(input("Digite o limite de velocidade em MPH: "))
        metroPorPixel = float(input("Digite a conversão de pixels para metros: "))
        camera_type = input("Digite '0' para câmera padrão ou o caminho da câmera USB: ")
        video_source = int(camera_type) if camera_type.isdigit() else camera_type
        vs = initialize_camera(video_source)
        trackableObjects = {}
        bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    contador_frames = 0  # Contador de frames

    # Loop principal
    while True:
        ret, frame = vs.read()
        if not ret:
            break

        frame = process_frame(frame, trackableObjects, bg_subtractor, metroPorPixel)

        # Exibição do quadro processado
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        contador_frames += 1  # Incrementar contador de frames

    # Finalizando
    cv2.destroyAllWindows()
    vs.release()

if __name__ == "__main__":
    main()
