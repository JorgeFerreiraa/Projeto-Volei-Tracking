import cv2
import numpy as np
from ultralytics import YOLO
import time
import csv


def main(videopath):
    # Carregar o modelo YOLO
    model = YOLO('yolov8n.pt')

    # Abrir o arquivo de vídeo
    video_path = videopath
    cap = cv2.VideoCapture(video_path)

    # Criar a janela

    # Histórico de rastreamento dos jogadores e da bola
    player_track_history = {}
    ball_track_history = {}

    # Função para calcular a distância Euclidiana entre dois pontos
    def euclidean_distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Função para calcular a velocidade média entre dois pontos
    escala_video = 0.031  # Ajuste conforme necessário

    def calculate_speed(p1, p2, time_diff):
        distance = euclidean_distance(p1, p2) * escala_video
        speed = distance / time_diff  # Velocidade em metros por segundo
        return speed

    # Arquivos CSV
    player_csv_file = open('player_positions.csv', mode='w', newline='')
    player_csv_writer = csv.writer(player_csv_file)
    player_speed_csv = open('player_speed.csv', mode='w', newline='')
    player_speed_csv_writer = csv.writer(player_speed_csv)

    ball_csv_file = open('ball_positions.csv', mode='w', newline='')
    ball_csv_writer = csv.writer(ball_csv_file)
    ball_speed_csv = open('ball_speed.csv', mode='w', newline='')
    ball_speed_csv_writer = csv.writer(ball_speed_csv)

    # Loop pelos frames do vídeo
    prev_frame_time = time.time()
    while cap.isOpened():
        # Incluir no início do código
        start_time = time.time()

        # Dentro do loop principal, antes de processar cada frame
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 10:
            break
        success, frame = cap.read()
        if success:
            current_frame_time = time.time()
            time_diff = current_frame_time - prev_frame_time
            prev_frame_time = current_frame_time

            results = model.track(frame, persist=True)

            # Guardar as caixas e os track IDs dos jogadores
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Convertendo frame para o espaço de cores HSV
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Definindo intervalo de cor para a bola (amarelo)
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            # Criar máscara para a bola
            mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

            # Encontrar contornos na máscara para detecção da bola
            contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Processar cada contorno para detecção da bola
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    center = (int(x + w / 2), int(y + h / 2))
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

                    if len(ball_track_history) > 0:
                        prev_position = list(ball_track_history.values())[0][-1]
                        speed = calculate_speed(prev_position, center, time_diff)
                        speed_kmph = speed * 3.6
                        print("Ball Speed:", speed_kmph, "kilometres/hour")
                        break

                    if len(ball_track_history) == 0:
                        ball_track_history[0] = []
                    ball_track_history[0].append(center)

                    # Escrever a posição da bola no arquivo CSV
                    ball_csv_writer.writerow([center[0], center[1]])

            # Processar cada jogador detectado
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                x_center = int(x + w / 2)
                y_center = int(y + h / 2)
                x1 = int(x - w / 2)
                y1 = int(y - h / 2)
                x2 = int(x + w / 2)
                y2 = int(y + h / 2)

                if track_id in player_track_history and len(player_track_history[track_id]) > 0:
                    prev_position = player_track_history[track_id][-1]
                    speed = calculate_speed(prev_position, (x_center, y_center), time_diff)
                    player_speed_csv_writer.writerow([track_id, speed])
                    print("Player ID:", track_id, "Speed:", speed, "meters/second")

                if track_id not in player_track_history:
                    player_track_history[track_id] = []
                player_track_history[track_id].append((x_center, y_center))

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, str(track_id), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Escrever a posição do jogador no arquivo CSV
                player_csv_writer.writerow([track_id, x_center, y_center])

            # Exibir o frame
            cv2.imshow("Video", frame)

            # Sair do loop se 'q' for pressionado
            if cv2.waitKey(100) & 0xFF == ord("q"):
                break

            time.sleep(0.03)
        else:
            break

    # Fechar os arquivos CSV após a escrita
    player_csv_file.close()
    ball_csv_file.close()

    cap.release()
    cv2.destroyAllWindows()
