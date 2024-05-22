import pygame

SPEED_PX = 3.2
IMAGE_SIZE_PX = 50


class Arrow:
    def __init__(self, x: float, y: float, speed_x: float, speed_y: float, image_path: str) -> None:
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (IMAGE_SIZE_PX, IMAGE_SIZE_PX))
        self.rect = self.image.get_rect(topleft=(x - IMAGE_SIZE_PX // 2, y - IMAGE_SIZE_PX // 2))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class UpArrow(Arrow):
    def __init__(self, start_x: float, start_y: float):
        super().__init__(start_x, start_y, 0, -SPEED_PX, "public/assets/up-arrow.png")


class DownArrow(Arrow):
    def __init__(self, start_x: float, start_y: float):
        super().__init__(start_x, start_y, 0, SPEED_PX, "public/assets/down-arrow.png")


class LeftArrow(Arrow):
    def __init__(self, start_x: float, start_y: float):
        super().__init__(start_x, start_y, -SPEED_PX, 0, "public/assets/left-arrow.png")


class RightArrow(Arrow):
    def __init__(self, start_x: float, start_y: float):
        super().__init__(start_x, start_y, SPEED_PX, 0, "public/assets/right-arrow.png")
