import pygame


SPEED_PX = 1.67
IMAGE_SIZE_PX = 100


class Arrow:
    def __init__(self, x, y, speed_x, speed_y, image_path) -> None:
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (IMAGE_SIZE_PX, IMAGE_SIZE_PX))
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class UpArrow(Arrow):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, 0, -SPEED_PX, "public/assets/up-arrow.png")


class DownArrow(Arrow):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, 0, SPEED_PX, "public/assets/down-arrow.png")


class LeftArrow(Arrow):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, -SPEED_PX, 0, "public/assets/left-arrow.png")


class RightArrow(Arrow):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, SPEED_PX, 0, "public/assets/right-arrow.png")
