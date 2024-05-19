import cv2
import numpy as np
import pygame

from motion.motion import Motion


class Game:
    def __init__(self, motion: Motion):
        self.motion = motion

        self.combo = 0
        self.score = 0
        self.missed = 0

        self.cap = cv2.VideoCapture(0)
        self.screen = pygame.display.set_mode()

        pygame.init()
        pygame.display.set_caption("OpenCV camera stream on Pygame")

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

                image = self.motion.process_hand(image, hands)
                image = cv2.flip(image, 1)

                # Convert the image from OpenCV to Pygame format
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb = np.rot90(image_rgb)
                frame_surface = pygame.surfarray.make_surface(image_rgb)
                self.screen.blit(frame_surface, (0, 0))

                # Add any Pygame overlay elements here
                # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, 100, 50), 2)
                # font = pygame.font.Font(None, 36)
                # text_surface = font.render("Direction Overlay", True, (255, 255, 255))
                # screen.blit(text_surface, (120, 10))

                pygame.display.update()

                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Hands", image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        self._quit()

    def _quit(self):
        self.cap.release()
        pygame.quit()
