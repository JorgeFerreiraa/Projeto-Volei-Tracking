import cv2
import numpy as np
from ultralytics import YOLO
import time
import customtkinter as tk

def main():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Open the video file
    video_path = "volei.mp4"
    cap = cv2.VideoCapture(video_path)

    # Create a Tkinter window
    root = tk.CTk()
    root.title("Volleyball Speed Tracker")
    root._set_appearance_mode("system")
    root.title("Tracking app")
    root.geometry("700x400")
    root.resizable(width=False,height=False)

    # Create a label to display ball speed
    title_label = tk.CTkLabel(root, text="Para fechar o programa clique na tecla q")
    title_label.pack()


    tabview = tk.CTkTabview(root, width=400, corner_radius=20, border_width=5, border_color="red",
                             segmented_button_selected_color="blue", segmented_button_unselected_hover_color="blue")
    tabview.pack()

    tabview.add("Jogadores")
    tabview.add("Velocidades")

    tabview.tab("Jogadores").grid_columnconfigure(0, weight=1)
    tabview.tab("Velocidades").grid_columnconfigure(0, weight=1)

    ball_speed_label = tk.CTkLabel(tabview.tab("Velocidades"), text="Ball speed: ")
    ball_speed_label.pack()

    # Store the track history for players and ball
    player_track_history = {}
    ball_track_history = {}

    # Função para calcular a distância Euclidiana entre dois pontos
    def euclidean_distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Função para calcular a velocidade média entre dois pontos
    # Escala do vídeo (metros por pixel)
    escala_video = 0.031 # Ajuste conforme necessário

    def calculate_speed(p1, p2, time_diff):
        distance = euclidean_distance(p1, p2) * escala_video
        speed = distance / time_diff  # Velocidade em metros por segundo
        return speed

    # Dictionary to store player speed labels
    player_speed_labels = {}

    # Loop through video frames
    prev_frame_time = time.time()
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            current_frame_time = time.time()
            time_diff = current_frame_time - prev_frame_time
            prev_frame_time = current_frame_time

            # Run YOLOv8 tracking on the frame
            results = model.track(frame, persist=True)

            # Get the bounding boxes and track IDs for players
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Convert frame to HSV color space for ball detection
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define range of yellow color in HSV for ball detection
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            # Threshold the HSV image to get only yellow colors for ball detection
            mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

            # Find contours in the mask for ball detection
            contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process each contour for ball detection
            for contour in contours:
                # Calculate area of contour for ball detection
                area = cv2.contourArea(contour)
                # If area is large enough, consider it as the ball for ball detection
                if area > 100:
                    # Calculate bounding box for the contour for ball detection
                    x, y, w, h = cv2.boundingRect(contour)
                    # Calculate center of the bounding box for ball detection
                    center = (int(x + w / 2), int(y + h / 2))

                    # Calculate speed if previous position exists for ball detection
                    if len(ball_track_history) > 0:
                        prev_position = list(ball_track_history.values())[0][-1]
                        speed = calculate_speed(prev_position, center, time_diff)
                        # Convertendo para quilômetros por hora
                        speed_kmph = speed * 3.6
                        ball_speed_label.configure(text="Ball Speed: {:.2f} km/h".format(speed_kmph))
                        # Atualizar apenas uma vez por quadro
                        break

                    # Update track history for ball detection
                    if len(ball_track_history) == 0:
                        ball_track_history[0] = []
                    ball_track_history[0].append(center)

            # Process each detected player
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                # Calcular as coordenadas do centro do retângulo
                x_center = int(x + w / 2)
                y_center = int(y + h / 2)

                # Calcular os cantos do retângulo em torno do centro
                x1 = int(x - w / 2)
                y1 = int(y - h / 2)
                x2 = int(x + w / 2)
                y2 = int(y + h / 2)

                # Calculate speed if previous position exists for player
                if track_id in player_track_history and len(player_track_history[track_id]) > 0:
                    prev_position = player_track_history[track_id][-1]
                    speed = calculate_speed(prev_position, (x_center, y_center), time_diff)
                    # Check if label for this player already exists
                    speed_kmph2 = speed * 3.6
                    if track_id not in player_speed_labels:

                        player_speed_labels[track_id] = tk.CTkLabel(tabview.tab("Velocidades"), text="Player {}: {:.2f} km/h".format(track_id, speed_kmph2))
                        player_speed_labels[track_id].pack()
                    else:
                        player_speed_labels[track_id].configure(text="Player {}: {:.2f} km/h".format(track_id, speed_kmph2))

                # Update track history for player
                if track_id not in player_track_history:
                    player_track_history[track_id] = []
                player_track_history[track_id].append((x_center, y_center))

            # Display the frame
            cv2.imshow("Video", frame)

            # Exit loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # Update the Tkinter window
            root.update()

            # A small delay to ensure the video is rendered properly
            time.sleep(0.03)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    root.mainloop()

if __name__ == "__main__":
    main()
