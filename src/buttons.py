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
        left_right, top_down = True, True
        x, y = indices
        x_range = [i for i in range(x - 1, x + 2)]
        y_range = [j for j in range(y - 1, y + 2)]

        grid = [[(i, j) for j in y_range if (i, j) != (x, y)] for i in x_range]
        neighbors = [ele for row in grid for ele in row]

        living = []
        for flower in neighbors:
            i, j = flower
            new_i, new_j = i, j

            if i < 0:
                if left_right:
                    new_i = board_width - 1
                else:
                    continue
            elif i >= board_width:
                if left_right:
                    new_i = 0
                else:
                    continue
            if j < 0:
                if top_down:
                    new_j = board_height - 1
                else:
                    continue
            elif j >= board_height:
                if top_down:
                    new_j = 0
                else:
                    continue

            living.append(btns[new_i][new_j].state)

        return sum(living)

    @staticmethod
    def make_surface(pygame, size, color):
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
