from cx_Freeze import setup, Executable

setup(
    name="GofL",
    version="1.0",
    description="Simple game",
    executables=[Executable("main.py")]
)
