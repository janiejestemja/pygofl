from utils import *
import sys

# Defintion of colors 
black = (0, 0, 0)
white = (255, 255, 255)

color_alive = (200, 200, 200)
color_dead = (20, 20, 20)

# Setting board bounds
board_width = 50
board_heigth = 30
cell_size = 32

# Setting screen bounds
width = board_width * (cell_size + 1)
height = board_heigth * (cell_size + 1)

def main():
    # Init screen
    screen = pygame.display.set_mode((width, height))
    screen.fill(black)

    # Setting framerates and durations
    clock = pygame.time.Clock()
    fps = 60
    duration = 3

    btn_img = make_surface((cell_size, cell_size), color_dead)

    btns = []
    for i in range(board_width):
        row = []
        for j in range(board_heigth):
            btn = Btn(i * (cell_size + 1) , j * (cell_size + 1), btn_img)
            row.append(btn)
        btns.append(row)

    # Starting animation loop
    frame = 0
    PAUSED = True
    while True:

        if PAUSED:

            for i, row in enumerate(btns):
                for j, btn in enumerate(row):
                    if btn.draw(screen):
                        if btn.state:
                            btn.state = False
                            btn.next_state = False
                            btn.image.fill(color_dead)
                        else:
                            btn.state = True
                            btn.next_state = True
                            btn.image.fill(color_alive)
        else:
            if frame == 0:
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        # Get alive neighbors
                        alive_neighbors = get_alive_neighbors((i, j), btns, board_width, board_heigth)

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
                            btn.image.fill(color_alive)
                        else:
                            btn.image.fill(color_dead)
                        btn.draw(screen)

        # Keep track of time
        clock.tick(fps)
        frame += 1            
        if frame > fps // 4:
            frame = 0

        # Updating animation by flipping the screen
        pygame.display.flip()

        # Listening for events
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Reset board
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if PAUSED:
                    for row in btns:
                        for btn in row:
                            btn.state = False
                            btn.next_state = False
                            btn.image.fill(color_dead)
                else:
                    pass

            # Pause the game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if PAUSED:
                    PAUSED = False
                    print("Game runs...")
                else:
                    PAUSED = True
                    print("Game paused...")

if __name__ == "__main__":
    main()
