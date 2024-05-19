import cv2
import mediapipe as mp
import numpy as np


class Motion:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

    def extract_hand_coords(self, hand_landmarks):
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        wrist_coords = (1 - wrist.x, 1 - wrist.y)
        index_finger_tip_coords = (
            1 - index_finger_tip.x,
            1 - index_finger_tip.y,
        )
        return wrist_coords, index_finger_tip_coords

    def process_hand(self, image, hands):
        wrist_coords = (0, 0)
        index_finger_tip_coords = (0, 0)

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

        return image, wrist_coords, index_finger_tip_coords

    # Calculate direction of hand based on the wrist and index finger tip coordinates
    def calculate_direction(self, wrist, index_finger_tip):
        vector = np.array([index_finger_tip[0] - wrist[0], index_finger_tip[1] - wrist[1]])
        angle = np.arctan2(vector[1], vector[0]) * 180 / np.pi

        if -45 <= angle <= 45:
            return "RIGHT"
        elif 45 < angle <= 135:
            return "UP"
        elif -135 <= angle < -45:
            return "DOWN"
        else:
            return "LEFT"
