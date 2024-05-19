import cv2
import mediapipe as mp
import numpy as np
import pygame


class Motion:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

    def run(self):
        cap = cv2.VideoCapture(0)
        pygame.init()
        screen = pygame.display.set_mode()
        pygame.display.set_caption("OpenCV camera stream on Pygame")

        with self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                image = self.process_hand(image, hands)
                image = cv2.flip(image, 1)

                # Convert the image from OpenCV to Pygame format
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb = np.rot90(image_rgb)
                frame_surface = pygame.surfarray.make_surface(image_rgb)
                screen.blit(frame_surface, (0, 0))

                # Add any Pygame overlay elements here
                # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, 100, 50), 2)
                # font = pygame.font.Font(None, 36)
                # text_surface = font.render("Direction Overlay", True, (255, 255, 255))
                # screen.blit(text_surface, (120, 10))

                pygame.display.update()

                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        pygame.quit()

    def process_hand(self, image, hands):
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

                # Extract the coordinates and flip them
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                wrist_coords = (1 - wrist.x, 1 - wrist.y)
                index_finger_tip_coords = (
                    1 - index_finger_tip.x,
                    1 - index_finger_tip.y,
                )

                direction = self._calculate_direction(wrist_coords, index_finger_tip_coords)

                # Add the direction text to the image
                cv2.putText(
                    image,
                    f"Direction: {direction}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

        return image

    # Calculate direction of hand based on the wrist and index finger tip coordinates
    def _calculate_direction(self, wrist, index_finger_tip):
        vector = np.array([index_finger_tip[0] - wrist[0], index_finger_tip[1] - wrist[1]])
        angle = np.arctan2(vector[1], vector[0]) * 180 / np.pi

        if -45 <= angle <= 45:
            return "Right"
        elif 45 < angle <= 135:
            return "Up"
        elif -135 <= angle < -45:
            return "Down"
        else:
            return "Left"
