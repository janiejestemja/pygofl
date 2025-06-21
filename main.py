import sys
import pygame
import time

bmargin = 32
screen_width = 1280 # 1024 # 1280
screen_height = 640 + bmargin # 512 + bmargin # 640

cell_size = (7, 7)

board_width = 127  + 32
board_height = 63  + 16

black = (0, 0, 0)
white = (255, 255, 255)

color_awoken = (10, 10, 220)
color_stillalive = (40, 160, 80)

color_dead = (30, 30, 30)
color_stilldead = (0, 0, 0)

bg_grid = (20, 20, 20)
bg_nav = (10, 10, 10)

# Basic Button
class Btn():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

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

class CellBtn(Btn):
    def __init__(self, x, y, image, scale=1):
        super().__init__(x, y, image, scale)

        self.past_state = False
        self.state = False
        self.next_state = False

    def set_states(self, new_state):
        self.past_state = new_state
        self.state = new_state
        self.next_state = new_state

    @staticmethod
    def get_alive_neighbors(indices, btns, board_width, board_height):
        x, y = indices
        x_range = [i for i in range(x - 1, x + 2)]
        y_range = [j for j in range(y - 1, y + 2)]

        grid = [[(i, j) for j in y_range if (i, j) != (x, y)] for i in x_range]
        neighbors = [ele for row in grid for ele in row]

        living = []
        for flower in neighbors:
            i, j = flower

            if i < 0 or i >= board_width:
                continue
            if j < 0 or j >= board_height:
                continue

            living.append(btns[i][j].state)

        return sum(living)

    @staticmethod
    def make_surface(size, color):
        surface  = pygame.Surface(size)
        surface.fill(color)
        return surface

def draw_text(screen, text, font_size, text_col, x, y):
    font = pygame.font.SysFont("Helvetica", font_size)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def main():
    game_started = False

    pygame.init()
    # Init screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyGame of Life")
    screen.fill(bg_grid)

    # Setting framerates 
    clock = pygame.time.Clock()
    fps = 60

    # Creating Cells
    btn_img = CellBtn.make_surface(cell_size, color_stilldead)
    btns = []
    for i in range(board_width):
        row = []
        for j in range(board_height):
            btn = CellBtn(4 + i * (cell_size[0] + 1) , 4 + j * (cell_size[1] + 1), btn_img)
            row.append(btn)
        btns.append(row)

    # Starting animation loop
    frame = 0
    game_state = "paused" # "running", "over"
    while True:
        # Navbar at the bottom
        pygame.draw.rect(screen, bg_nav, (0, screen_height - bmargin, screen_width, screen_height))

        match game_state:
            case "paused":
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        if btn.draw(screen):
                            if btn.state == True:
                                btn.set_states(False)
                                btn.image.fill(color_stilldead)
                            else:
                                btn.set_states(True)
                                btn.image.fill(color_stillalive)
            case "running":
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        # Get alive neighbors
                        alive_neighbors = CellBtn.get_alive_neighbors((i, j), btns, board_width, board_height)

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

                        btn.draw(screen)

            case "over":
                score = 0
                for row in btns:
                    for btn in row:

                        if btn.state == True:
                            score += 1
                        if btn.past_state == True:
                            score += 1

                        btn.draw(screen)


                draw_text(screen, "Game Over" , 12, white, 200, screen_height - bmargin + 1)
                draw_text(screen, "Press ESC to restart." , 12, white, 0, screen_height - bmargin//2 + 1)
                draw_text(screen, f"Time: {end_time - start_time:.2f}" , 12, white, 300, screen_height - bmargin + 1)

                if end_time - start_time < 3:
                    draw_text(screen, f"No Score if game shorter than 3 seconds" , 12, white, 300, screen_height - bmargin//2 + 1)
                else:
                    draw_text(screen, f"Score: {score}" , 12, white, 300, screen_height - bmargin//2 + 1)

        # Keep track of time
        clock.tick(fps)
        frame += 1
        if frame >= fps:
            frame = 0

        # Print games state
        draw_text(screen, game_state.capitalize() , 12, white, 0, screen_height - bmargin + 1)

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

                        if game_state == "over":
                            print("Restarting...")
                            pygame.quit()
                            main()

                        elif game_started:
                            game_state = "over"
                            end_time = time.time()

                        else:
                            game_state = "paused"
                            
                    elif game_state == "over":
                        pass

                    else:
                        if game_started == False:
                            start_time = time.time()
                            game_started = True
                        else:
                            game_state = "running"

                # While paused
                elif game_state == "paused":

                    # Reset Board 
                    if event.key == pygame.K_SPACE:
                        for row in btns:
                            for btn in row:
                                btn.set_states(False)
                                btn.image.fill(color_stilldead)

                    # Set horizontal line
                    elif event.key == pygame.K_1:
                        for i, row in enumerate(btns):
                            for j, btn in enumerate(row):
                                if j == board_height//2:
                                    btn.set_states(True)
                                    btn.image.fill(color_stillalive)

                    # Set vertical line
                    elif event.key == pygame.K_2:
                        for i, row in enumerate(btns):
                            for j, btn in enumerate(row):
                                if i == board_width//2:
                                    btn.set_states(True)
                                    btn.image.fill(color_stillalive)

                    # Set loose grid (points)
                    elif event.key == pygame.K_3:
                        for i, row in enumerate(btns):
                            for j, btn in enumerate(row):
                                if i % 8 == 3 and j % 8 == 3:
                                    btn.set_states(True)
                                    btn.image.fill(color_stillalive)

                    # Set loose grid (lines)
                    elif event.key == pygame.K_4:
                        for i, row in enumerate(btns):
                            for j, btn in enumerate(row):
                                if i % 8 == 3 or j % 8 == 3:
                                    btn.set_states(True)
                                    btn.image.fill(color_stillalive)

                    # Set tight grid (points)
                    elif event.key == pygame.K_5:
                        for i, row in enumerate(btns):
                            for j, btn in enumerate(row):
                                if i % 4 == 1 and j % 4 == 1:
                                    btn.set_states(True)
                                    btn.image.fill(color_stillalive)

                    # Set tight grid (lines)
                    elif event.key == pygame.K_6:
                        for i, row in enumerate(btns):
                            for j, btn in enumerate(row):
                                if i % 4 == 1 or j % 4 == 1:
                                    btn.set_states(True)
                                    btn.image.fill(color_stillalive)

                    # Glider from top
                    elif event.key == pygame.K_s:
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
                    elif event.key == pygame.K_a:
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
                    elif event.key == pygame.K_x:
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
                    elif event.key == pygame.K_y:
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
