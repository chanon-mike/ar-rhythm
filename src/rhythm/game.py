import random
from typing import Literal
import cv2
import numpy as np
import pygame

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
        self.arrow_timer = 0

        self.init_heart()
        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text: str, position: tuple):
        text_surface = self.font.render(text, True, (255, 255, 255))  # テキストを描画
        self.screen.blit(text_surface, position)  # 画面にテキストを描画

    def init_heart(self):
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.heart = Heart(frame_width // 2, frame_height // 2)  # Center the heart

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

                # Convert the image from OpenCV to Pygame format
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb = np.rot90(image_rgb)
                frame_surface = pygame.surfarray.make_surface(image_rgb)
                self.screen.blit(frame_surface, (0, 0))

                # Detect the direction of the hand
                direction = self.motion.calculate_direction(wrist_coords, index_finger_tip_coords)
                self.detect_and_collide(direction)

                self.update_arrows()
                self.draw_arrows()
                self.heart.draw(self.screen)

                self.draw_text(f"Combo: {self.combo}", (10, 10))  # コンボ数を画面の左上に描画
                self.draw_text(f"Score: {self.score}", (10, 50))  # スコアを画面の左上から50px下に描画

                pygame.display.update()
                self.update_arrow_timer()
                self.clock.tick(60)  # Limit to 60 frames per second

                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self._quit()

    def add_arrow(self):
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        arrow_type = random.choice([UpArrow, DownArrow, LeftArrow, RightArrow])
        if arrow_type == UpArrow:
            arrow = UpArrow(frame_width // 2, frame_height)
        elif arrow_type == DownArrow:
            arrow = DownArrow(frame_width // 2, 0)
        elif arrow_type == LeftArrow:
            arrow = LeftArrow(frame_width, frame_height // 2)
        else:
            arrow = RightArrow(0, frame_height // 2)

        self.arrows.append(arrow)

    def update_arrow_timer(self):
        self.arrow_timer += self.clock.get_time()
        if self.arrow_timer >= 2000:
            self.add_arrow()
            self.arrow_timer = 0

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
        if (
            len(self.arrows) > 0
            and self.arrows[0].rect.colliderect(self.heart.rect)
            and (
                (direction == "UP" and isinstance(self.arrows[0], DownArrow))
                or (direction == "DOWN" and isinstance(self.arrows[0], UpArrow))
                or (direction == "LEFT" and isinstance(self.arrows[0], RightArrow))
                or (direction == "RIGHT" and isinstance(self.arrows[0], LeftArrow))
            )
        ):
            self.remove_arrow()

    def _quit(self):
        self.cap.release()
        pygame.quit()
