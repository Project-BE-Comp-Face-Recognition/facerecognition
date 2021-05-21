from pathlib import Path
def homedirectory():
    home=Path().resolve()
    return home

home=homedirectory()