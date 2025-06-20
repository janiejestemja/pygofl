import sys
import pygame 

# Defintion of colors 
black = (0, 0, 0)
white = (255, 255, 255)

# Setting screen bounds
width = 990
height = 660
board_width = 30
board_heigth = 20

def get_alive_neighbors(pos, btns):
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

def main():
    # Init screen
    screen = pygame.display.set_mode((width, height))
    screen.fill(black)

    # Setting framerates and durations
    clock = pygame.time.Clock()
    fps = 60
    duration = 3
    frames = duration * fps

    btn_img = make_surface((32, 32), (20, 20, 20))

    btns = []
    for i in range(board_width):
        row = []
        for j in range(board_heigth):
            btn = Btn(i * 33 , j * 33, btn_img)
            row.append(btn)
        btns.append(row)

    # Starting animation loop
    frame = 0
    PAUSED = True
    while frame <= frames:

        if PAUSED:

            for i, row in enumerate(btns):
                for j, btn in enumerate(row):
                    if btn.draw(screen):
                        if btn.state:
                            btn.state = False
                            btn.image.fill((20, 20, 20))
                        else:
                            btn.state = True
                            btn.image.fill((200, 200, 200))
        else:
            if frame == 0:
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        # Get alive neighbors
                        alive_neighbors = get_alive_neighbors((i, j), btns)

                        # Check living
                        if btn.state:
                            if alive_neighbors < 2:
                                btn.next_state = False
                            elif alive_neighbors > 3:
                                btn.next_state = False
                            else:
                                btn.next_state = True
                        else:
                            if alive_neighbors == 3:
                                btn.next_state = True

                for row in btns:
                    for btn in row:
                        btn.state = btn.next_state
                        if btn.state:
                            btn.image.fill((200, 200, 200))
                        else:
                            btn.image.fill((20, 20, 20))
                        btn.draw(screen)

        # Keep track of time
        clock.tick(fps)
        frame += 1            
        if frame > frames:
            frame = 0

        # Updating animation by flipping the screen
        pygame.display.flip()

        # Listening for events
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Pause the game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if PAUSED:
                    PAUSED = False
                    print("Game runs...")
                else:
                    PAUSED = True
                    print("Game paused...")

def make_surface(size, colour):
    surface  = pygame.Surface(size).convert()
    surface.fill(colour)
    return surface

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
    main()
