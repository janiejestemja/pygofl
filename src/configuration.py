class Config:
    margins = {
        "top": 16,
        "bot": 32,
        "lef": 8,
        "rig": 8,
        "cell_bot": 1,
        "cell_rig": 1,
    }

    # actual cell size (8 - 1 = 7)
    cell_size = (8, 8)

    # 80-1 * 160-1 = 12_561
    board = {
        "hei": 7,
        "wid": 11,
        "scale": (20, 10),
    }

    # 8 * 80 = 640 and 8 * 160 = 1280
    screen = {
        "hei": 64,
        "wid": 64,
    }

    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),

        "alive": (10, 10, 220),
        "stillalive": (40, 160, 80),

        "dead": (20, 20, 20),
        "stilldead": (0, 0, 0),

        "bg_grid": (20, 20, 20),
        "bg_nav": (10, 10, 10),
    }

    @classmethod
    def make_config(cls, scale=False):
        # initialise
        config = {
            "margins": cls.margins,
            "cell_size": cls.cell_size,
            "board": cls.board,
            "screen": cls.screen,
            "colors": cls.colors,
        }

        # selfscale board and screen
        if scale:
            config["board"]["hei"] = config["board"]["scale"][1]
            config["board"]["wid"] = config["board"]["scale"][0]

        # scale screen up from board...
        config["screen"]["hei"] *= cls.board["hei"]
        config["screen"]["wid"] *= cls.board["wid"]
        # ...and add margins for bars around the board
        config["screen"]["hei"] += cls.margins["bot"] + cls.margins["top"]
        config["screen"]["wid"] += cls.margins["lef"] + cls.margins["rig"]

        # scale up board from cell size...
        config["board"]["hei"] *= cls.cell_size[1]
        config["board"]["wid"] *= cls.cell_size[0]
        # ...and subtract one cell margin
        config["board"]["hei"] -= cls.margins["cell_bot"]
        config["board"]["wid"] -= cls.margins["cell_rig"]

        # subtract cell margin from cell size to match their surface pixel
        config["cell_size"] = (
            config["cell_size"][0] - cls.margins["cell_rig"],
            config["cell_size"][1] - cls.margins["cell_bot"]
        )
        return config
