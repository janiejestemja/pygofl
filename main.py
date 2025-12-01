def draw_text(screen, text, font_size, text_col, x, y):
    font = pygame.font.SysFont("Helvetica", font_size)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def main():
    # Definition of CLI
    parser = argparse.ArgumentParser(description="Naive game of life.")
    parser.add_argument("--random", type=bool, help="alternative chances")
    parser.add_argument("--scale", type=bool, help="alternative scale")
    parser.add_argument("--walls", choices=["yes", "no"], help="enable walls")
    parser.add_argument("--alt_color", type=bool, help="alternative colorscheme")
    parser.add_argument("--alt_rules", type=bool, help="alternative ruleset")
    args = parser.parse_args()

    walls = (True, False)
    match args.walls:
        case "yes":
            walls = (False, False)
        case "no":
            walls = (True, True)

    config = Config.make_config(scale=args.scale, alt_color=args.alt_color)

    pygame.init()
    # Init screen
    screen = pygame.display.set_mode(
        (config["screen"]["wid"], config["screen"]["hei"])
    )
    pygame.display.set_caption("PyGame of Life")
    screen.fill(config["colors"]["bg_grid"])

    # Setting framerates
    clock = pygame.time.Clock()
    fps = 60

    # Creating Cells
    btn_img = CellBtn.make_surface(
        pygame,
        config["cell_size"],
        config["colors"]["stilldead"]
    )
    sum_all_btns = 0
    btns = []
    for i in range(config["board"]["wid"]):
        row = []
        for j in range(config["board"]["hei"]):
            btn = CellBtn(
                pygame,
                # Grid: 4 + 79 * (7 + 1) = 636 pixels
                config["margins"]["lef"] + 4 + i * (config["cell_size"][0] + config["margins"]["cell_rig"]),
                # Grid: 4 + 159 * (7 + 1) = 1_272 pixels
                config["margins"]["top"] + 4 + j * (config["cell_size"][1] + config["margins"]["cell_bot"]),
                btn_img
            )
            sum_all_btns += 1
            row.append(btn)
        btns.append(row)

    # Starting animation loop
    frame = 0
    game_state = "paused"  # "continue"
    while True:
        match game_state:
            case "paused":
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        if btn.draw(pygame, screen):
                            if btn.state is True:
                                btn.set_states(False)
                                btn.image.fill(config["colors"]["stilldead"])
                            else:
                                btn.set_states(True)
                                btn.image.fill(config["colors"]["stillalive"])
            case "continue":
                for i, row in enumerate(btns):
                    for j, btn in enumerate(row):
                        # Get alive neighbors
                        alive_neighbors = CellBtn.get_alive_neighbors(
                            (i, j),
                            btns,
                            config["board"]["wid"],
                            config["board"]["hei"],
                            walls,
                        )

                        # Check living
                        if btn.state and args.alt_rules:
                            if alive_neighbors < 2:
                                btn.next_state = False
                            elif alive_neighbors > 4:
                                btn.next_state = False
                        elif btn.state:
                            # Default: 2
                            if alive_neighbors < 2:
                                btn.next_state = False
                            # Default: 3
                            elif alive_neighbors > 3:
                                btn.next_state = False
                        # Check dead
                        else:
                            # Default: 3
                            if args.alt_rules:
                                if alive_neighbors in [2, 3]:  # 3
                                    btn.next_state = True
                                if alive_neighbors == 3:
                                    btn.next_state = False

                            elif alive_neighbors == 3:  # 3
                                btn.next_state = True
                            # Random chance for awakening
                            elif args.random and alive_neighbors > 0:
                                if randint(-10_000, 10_000) == 0:
                                    btn.next_state = True
                        # Random chance for dying
                        if args.random and btn.next_state and alive_neighbors != 3:
                            if randint(-10_000, 10_000) == 0:
                                btn.next_state = False

                # Setting old state to new one
                for row in btns:
                    for btn in row:
                        btn.past_state = btn.state
                        btn.state = btn.next_state

                        # Coloring alive
                        if btn.state:
                            if btn.past_state == btn.state:
                                btn.image.fill(config["colors"]["stillalive"])
                            else:
                                btn.image.fill(config["colors"]["alive"])

                        # Coloring dead
                        else:
                            if btn.past_state == btn.state:
                                btn.image.fill(config["colors"]["stilldead"])
                            else:
                                btn.image.fill(config["colors"]["dead"])

                        btn.draw(pygame, screen)

        # Keep track of time
        clock.tick(fps)
        frame += 1
        if frame >= fps:
            frame = 0

        # Bar at the top
        pygame.draw.rect(
            screen,
            config["colors"]["bg_nav"],
            (
                0,
                0,
                config["screen"]["wid"],
                config["margins"]["top"],
            )
        )
        # Bar at the bottom
        pygame.draw.rect(
            screen,
            config["colors"]["bg_nav"],
            (
                0,
                config["screen"]["hei"] - config["margins"]["bot"],
                config["screen"]["wid"],
                config["screen"]["hei"],
            )
        )
        # Bar at the right
        # Calculate therefore length of bar...
        still_alive_count, alive_count, still_dead_count = 0, 0, 0
        for row in btns:
            for btn in row:
                if btn.state and btn.past_state:
                    still_alive_count += 1
                elif btn.state:
                    alive_count += 1
                else:
                    still_dead_count += 1
        alive_ratio = 1 - ((sum_all_btns - alive_count) / sum_all_btns)
        still_alive_ratio = 1 - ((sum_all_btns - still_alive_count) / sum_all_btns)
        dead_ratio = 1 - ((sum_all_btns - still_dead_count) / sum_all_btns)

        # Bar at the right
        pygame.draw.rect(
            screen,
            config["colors"]["bg_nav"],
            (
                config["screen"]["wid"] - config["margins"]["rig"],
                config["margins"]["top"],
                config["screen"]["wid"],
                config["screen"]["hei"] - config["margins"]["bot"] - config["margins"]["top"],
            )
        )
        pygame.draw.rect(
            screen,
            config["colors"]["stillalive"],
            (
                config["screen"]["wid"] - config["margins"]["rig"],
                (config["screen"]["hei"] / 2) - still_alive_ratio * (config["screen"]["hei"] / 2),
                config["screen"]["wid"],
                2 * still_alive_ratio * (config["screen"]["hei"] / 2),
            )
        )
        # Bar at the left
        pygame.draw.rect(
            screen,
            config["colors"]["bg_nav"],
            (
                0,
                config["margins"]["top"],
                config["margins"]["lef"],
                config["screen"]["hei"] - config["margins"]["bot"] - config["margins"]["top"],
            )
        )
        pygame.draw.rect(
            screen,
            config["colors"]["alive"],
            (
                0,
                (config["screen"]["hei"] / 2) - alive_ratio * (config["screen"]["hei"] / 2),
                config["margins"]["lef"],
                2 * alive_ratio * (config["screen"]["hei"] / 2),
            )
        )

        # Print Counts
        draw_text(
            screen,
            f"still: {still_alive_count:04d}",
            16,
            config["colors"]["stillalive"],
            0.4 * (config["screen"]["wid"]),
            config["screen"]["hei"] - config["margins"]["bot"] + 1,
        )
        draw_text(
            screen,
            f"alive: {alive_count:04d}",
            16,
            config["colors"]["alive"],
            0.6 * (config["screen"]["wid"]),
            config["screen"]["hei"] - config["margins"]["bot"] + 1,
        )
        draw_text(
            screen,
            f"free: {still_dead_count:04d}",
            16,
            config["colors"]["bg_grid"],
            0.8 * (config["screen"]["wid"]),
            config["screen"]["hei"] - config["margins"]["bot"] + 1,
        )
        draw_text(
            screen,
            f"total: {alive_count + still_alive_count + still_dead_count:04d}",
            # f"total: {len(btns) * len(btns[0]):04d}",
            14,
            config["colors"]["white"],
            0.9 * config["screen"]["wid"] - config["margins"]["lef"] - config["margins"]["rig"],
            1,
        )
        # Print games state
        draw_text(
            screen,
            game_state.capitalize(),
            14,
            config["colors"]["white"],
            0,
            1,
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
                        game_state = "continue"

                # While paused
                elif game_state == "paused":

                    match event.key:
                        # Reset Board
                        case pygame.K_SPACE:
                            for row in btns:
                                for btn in row:
                                    btn.set_states(False)
                                    btn.image.fill(config["colors"]["stilldead"])

                        # Set horizontal line
                        case pygame.K_1:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == config["board"]["hei"]//2:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])

                        # Set vertical line
                        case pygame.K_2:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i == config["board"]["wid"]//2:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])

                        # Diagonals
                        case pygame.K_3:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j - i == 0:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        case pygame.K_4:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i + 1 == len(row) - j:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])

                        # Glider from top
                        case pygame.K_q:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == 0 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == 1 and i % 6 == 5:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == 2 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        case pygame.K_w:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == 0 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == 1 and i % 6 == 3:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == 2 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])

                        # Glider from bottom
                        case pygame.K_e:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == config["board"]["hei"] - 1 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == config["board"]["hei"] - 2 and i % 6 == 3:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == config["board"]["hei"] - 3 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        case pygame.K_r:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if j == config["board"]["hei"] - 1 and i % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == config["board"]["hei"] - 2 and i % 6 == 5:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if j == config["board"]["hei"] - 3 and (i % 6 == 3 or i % 6 == 4 or i % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        # Glider from left
                        case pygame.K_s:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i == 0 and j % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == 1 and j % 6 == 3:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == 2 and (j % 6 == 3 or j % 6 == 4 or j % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        case pygame.K_a:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i == 0 and j % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == 1 and j % 6 == 5:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == 2 and (j % 6 == 3 or j % 6 == 4 or j % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        # Glider from right
                        case pygame.K_d:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i == config["board"]["wid"] - 1 and j % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == config["board"]["wid"] - 2 and j % 6 == 3:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == config["board"]["wid"] - 3 and (j % 6 == 3 or j % 6 == 4 or j % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                        case pygame.K_f:
                            for i, row in enumerate(btns):
                                for j, btn in enumerate(row):
                                    if i == config["board"]["wid"] - 1 and j % 6 == 4:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == config["board"]["wid"] - 2 and j % 6 == 5:
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])
                                    if i == config["board"]["wid"] - 3 and (j % 6 == 3 or j % 6 == 4 or j % 6 == 5):
                                        btn.set_states(True)
                                        btn.image.fill(config["colors"]["stillalive"])


if __name__ == "__main__":
    import sys
    import argparse
    import pygame
    from src import CellBtn, Config
    from random import randint
    main()
