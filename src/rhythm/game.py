from typing import Literal
import cv2
import numpy as np
import pygame
import random

from motion.motion import Motion
from rhythm.arrow import DownArrow, LeftArrow, RightArrow, UpArrow
from rhythm.heart import Heart

SPEED_PX = 3.67
IMAGE_SIZE_PX = 100


class Game:
    def __init__(self, motion: Motion):
        self.motion = motion

        self.combo = 0
        self.score = 0
        self.missed = 0
        self.arrows = []

        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

        pygame.init()
        pygame.display.set_caption("OpenCV camera stream on Pygame")

        # self.screen = pygame.display.set_mode((640, 640), pygame.SCALED)
        self.screen = pygame.display.set_mode()
        self.clock = pygame.time.Clock()

        self.init_arrows()
        self.init_heart()

    def init_heart(self):
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.heart = Heart(frame_width // 2, frame_height // 2)  # Center the heart

    # TODO: Generate arrows method
    def init_arrows(self):
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        arrow_list = [
            UpArrow(frame_width // 2, frame_height),  # Bottom
            DownArrow(frame_width // 2, 0),  # Top
            LeftArrow(frame_width, frame_height // 2),  # Right
            RightArrow(0, frame_height // 2),  # Left
        ]

        for arrow in arrow_list:
            self.arrows.append(arrow)

    def run(self):
        with self.motion.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    continue

                image, wrist_coords, index_finger_tip_coords = self.motion.process_hand(image, hands)
                image = cv2.flip(image, 1)

                # Convert the image from OpenCV to Pygame format
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb = np.rot90(image_rgb)
                frame_surface = pygame.surfarray.make_surface(image_rgb)
                self.screen.blit(frame_surface, (0, 0))

                # Get the dimensions of the frame
                # frame_rect = frame_surface.get_rect()
                # # Calculate the position to place the frame at the center of the screen
                # frame_x = (640 - frame_rect.width) // 2
                # frame_y = (640 - frame_rect.height) // 2
                # # Fill the screen with black color
                # self.screen.blit(frame_surface, (frame_x, frame_y))

                # Detect the direction of the hand
                direction = self.motion.calculate_direction(wrist_coords, index_finger_tip_coords)
                self.detect_and_collide(direction)

                self.update_arrows()
                self.draw_arrows()
                self.heart.draw(self.screen)

                pygame.display.update()

                self.clock.tick(60)  # Limit to 60 frames per second

                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self._quit()

    def update_arrows(self):
        for arrow in self.arrows:
            arrow.update()

    def draw_arrows(self):
        for arrow in self.arrows:
            arrow.draw(self.screen)

    def remove_arrow(self):
        self.arrows.pop(0)
        self.combo += 1
        self.score += 1

    def detect_and_collide(self, direction: Literal["UP", "DOWN", "LEFT", "RIGHT"]):
        try:
            if (
                (direction == "UP" and isinstance(self.arrows[0], DownArrow))
                or (direction == "DOWN" and isinstance(self.arrows[0], UpArrow))
                or (direction == "LEFT" and isinstance(self.arrows[0], RightArrow))
                or (direction == "RIGHT" and isinstance(self.arrows[0], LeftArrow))
            ) and self.arrows[0].rect.colliderect(self.heart.rect):
                self.remove_arrow()
            print(f"Combo: {self.combo}, Score: {self.score}")
        except IndexError:
            print("Arrow list is empty.")

    def _quit(self):
        self.cap.release()
        pygame.quit()

