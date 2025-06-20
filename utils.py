import pygame

def make_surface(size, colour):
    surface  = pygame.Surface(size).convert()
    surface.fill(colour)
    return surface

def get_alive_neighbors(pos, btns, board_width, board_heigth):
    x, y = pos    
    x_range = [i for i in range(x - 1, x + 2)]
    y_range = [j for j in range(y - 1, y + 2)]

    grid = [[(i, j) for j in y_range if (i, j) != (x, y)] for i in x_range]
    neighbors = [ele for row in grid for ele in row]

    living = []
    for flower in neighbors:
        i, j = flower

        if i < 0 or i >= board_width:
            continue
        if j < 0 or j >= board_heigth:
            continue

        living.append(btns[i][j].state)

    return sum(living)

class Btn():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False
        self.state = False
        self.next_state = False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

if __name__ == "__main__":
    print("This is a utils file containing definitions")
