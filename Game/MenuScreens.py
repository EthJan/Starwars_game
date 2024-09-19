import pygame
pygame.init()

# Setup
WIDTH, HEIGHT = 700, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Menu Button Sprites
start_img = pygame.image.load('Playbutton.png').convert_alpha()

# Mouse Tracking
mouseCords = pygame.mouse.get_pos()


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        # Put Button on the Screen
        win.blit(self.image, (self.rect.x, self.rect.y))


def title():
    start_button = Button(100, 200, start_img, 1.2)
    run = True
    while run:
        win.fill((202, 228, 241))

        start_button.draw()

        if start_button.collidepoint(mouseCords):
            if pygame.mouse.get_pressed()[0]:
                print("Start clicked")
        # go to game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


title()
pygame.quit()
