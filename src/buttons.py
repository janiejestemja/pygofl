class Btn():
    def __init__(self, pygame, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(
            image,
            (
                int(width * scale),
                int(height * scale)
            )
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    def draw(self, pygame, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if not self.clicked and pygame.mouse.get_pressed()[0] == 1:
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
    def make_surface(pygame, size, color):
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
