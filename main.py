from utils import *
import sys

# Defintion of colors 
black = (0, 0, 0)
white = (255, 255, 255)

color_alive = (20, 200, 200)
color_stillalive = (120, 100, 160)
color_dead = (32, 64, 128)
color_stilldead = (20, 20, 20)

# Setting board bounds
board_width = 128 + 32 + 32 + 1
board_heigth = 64 + 16 + 16 + 1
cell_size = 8

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

    btn_img = make_surface((cell_size, cell_size), color_stilldead)

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

                # Setting old state to new one
                for row in btns:
                    for btn in row:

                        old_state = btn.state 
                        btn.state = btn.next_state

                        if btn.state:
                            # Still alive
                            if btn.state == old_state:
                                btn.image.fill((120, 80, 160))

                            # Newly alive
                            else:
                                btn.image.fill(color_alive)

                        else:
                            # Still dead
                            if btn.state == old_state:
                                btn.image.fill((20, 20, 20))
                            # Just died
                            else:
                                btn.image.fill(color_dead)
                        btn.draw(screen)

        # Keep track of time
        clock.tick(fps)
        frame += 1            
        if frame >= fps // 6:
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
                            btn.image.fill(color_stilldead)
                else:
                    pass

            # Set grid
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if i % 8 == 4 and j % 8 == 4:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # Set grid
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if i % 8 == 4 or j % 8 == 4:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # Set grid
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if i % 4 == 2 and j % 4 == 2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # Set grid
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if i % 4 == 2 or j % 4 == 2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # Set vertical line
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if i == board_width//2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # Set horizontal line
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if j == board_heigth//2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # Set X
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if i - j == 0:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if i + j == board_heigth - 1:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # devel
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if j == 0 and i % 6 == 2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == 1 and i % 6 == 3:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == 2 and (i % 6 == 1 or i % 6 == 2 or i % 6 == 3):
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # devel
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if j == board_heigth - 1 and i % 6 == 2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == board_heigth - 2 and i % 6 == 3:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == board_heigth - 3 and (i % 6 == 1 or i % 6 == 2 or i % 6 == 3):
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
            # devel
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if j == 0 and i % 6 == 2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == 1 and i % 6 == 1:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == 2 and (i % 6 == 1 or i % 6 == 2 or i % 6 == 3):
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)

            # devel
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if PAUSED:
                    for i, row in enumerate(btns):
                        for j, btn in enumerate(row):
                            if j == board_heigth - 1 and i % 6 == 2:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == board_heigth - 2 and i % 6 == 1:
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)
                            if j == board_heigth - 3 and (i % 6 == 1 or i % 6 == 2 or i % 6 == 3):
                                btn.state = True
                                btn.next_state = True
                                btn.image.fill(color_alive)


                            

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
