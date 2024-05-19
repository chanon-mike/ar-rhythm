import pygame

IMAGE_SIZE_PX = 100


class Heart:
    def __init__(self, x: float, y: float):
        self.image = pygame.image.load("public/assets/heart.png")
        self.image = pygame.transform.scale(self.image, (IMAGE_SIZE_PX, IMAGE_SIZE_PX))
        self.rect = self.image.get_rect(topleft=(x - IMAGE_SIZE_PX // 2, y - IMAGE_SIZE_PX // 2))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
