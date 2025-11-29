import sys
import pygame
from src import CellBtn

bmargin = 32
screen_width = 1280  # 1024 # 1280
screen_height = 640 + bmargin  # 512 + bmargin # 640

cell_size = (7, 7)

board_width = 127 + 32
board_height = 63 + 16

black = (0, 0, 0)
white = (255, 255, 255)

color_awoken = (10, 10, 220)
color_stillalive = (40, 160, 80)

color_dead = (30, 30, 30)
color_stilldead = (0, 0, 0)

bg_grid = (20, 20, 20)
bg_nav = (10, 10, 10)


def draw_text(screen, text, font_size, text_col, x, y):
    font = pygame.font.SysFont("Helvetica", font_size)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def main():
    pygame.init()
    # Init screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyGame of Life")
    screen.fill(bg_grid)

    # Setting framerates
    clock = pygame.time.Clock()
    fps = 60

    # Creating Cells
    btn_img = CellBtn.make_surface(pygame, cell_size, color_stilldead)
    btns = []
    for i in range(board_width):
        row = []
        for j in range(board_height):
            btn = CellBtn(
                pygame,
                4 + i * (cell_size[0] + 1) ,
                4 + j * (cell_size[1] + 1),
                btn_img
            )
            row.append(btn)
        btns.append(row)

    # Starting animation loop
    frame = 0
    game_state = "paused"  # "running"
    while True:
        # Navbar at the bottom
        pygame.draw.rect(
            screen,
            bg_nav,
            (
                0,
                screen_height - bmargin,
                screen_width, screen_height
            )
        )

        match game_state:
            case "paused":
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        if btn.draw(pygame, screen):
                            if btn.state is True:
                                btn.set_states(False)
                                btn.image.fill(color_stilldead)
                            else:
                                btn.set_states(True)
                                btn.image.fill(color_stillalive)
            case "running":
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        # Get alive neighbors
                        alive_neighbors = CellBtn.get_alive_neighbors(
                            (i, j),
                            btns,
                            board_width,
                            board_height
                        )

                        # Check living
                        if btn.state:
                            if alive_neighbors < 2:
                                btn.next_state = False
                            elif alive_neighbors > 3:
                                btn.next_state = False
                            else:
                                btn.next_state = True

                        # Check dead
                        else:
                            if alive_neighbors == 3:
                                btn.next_state = True

                # Setting old state to new one
                for row in btns:
                    for btn in row:
                        btn.past_state = btn.state
                        btn.state = btn.next_state

                        # Coloring alive
                        if btn.state:
                            if btn.past_state == btn.state:
                                btn.image.fill(color_stillalive)
                            else:
                                btn.image.fill(color_awoken)

                        # Coloring dead
                        else:
                            if btn.past_state == btn.state:
                                btn.image.fill(color_stilldead)
                            else:
                                btn.image.fill(color_dead)

                        btn.draw(pygame, screen)

        # Keep track of time
        clock.tick(fps)
        frame += 1
        if frame >= fps:
            frame = 0

        # Print games state
        draw_text(
            screen,
            game_state.capitalize(),
            12,
            white,
            0,
            screen_height - bmargin + 1
        )

        # Updating animation by flipping the screen
        pygame.display.flip()

        # Listening for events
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check keyboard input
            elif event.type == pygame.KEYDOWN:

                # Pause game
                if event.key == pygame.K_ESCAPE:
                    if game_state != "paused":
                        game_state = "paused"
                    else:
                        game_state = "running"

                # While paused
                elif game_state == "paused":

                    match event.key:
                        # Reset Board
                        case pygame.K_SPACE:
                            for row in btns:
                                for btn in row:
                                    btn.set_states(False)
                                    btn.image.fill(color_stilldead)

                        # Set horizontal line
                        case pygame.K_1:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == board_height//2:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)

                        # Set vertical line
                        case pygame.K_2:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i == board_width//2:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)

                        # Glider from top
                        case pygame.K_3:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == 0 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == 1 and i % 6 == 5:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == 2 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)

                        # Glider from top
                        case pygame.K_4:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == 0 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == 1 and i % 6 == 3:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == 2 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)

                        # Glider from bottom
                        case pygame.K_5:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == board_height - 1 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == board_height - 2 and i % 6 == 5:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == board_height - 3 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)

                        # Glider from bottom
                        case pygame.K_6:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == board_height - 1 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == board_height - 2 and i % 6 == 3:
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)
                                    if j == board_height - 3 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(color_stillalive)


if __name__ == "__main__":
    main()
