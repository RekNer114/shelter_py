from pathlib import Path

DEFAULT_SHELTER_NAME = "default"



HIDDEN_DIR_NAME = ".shelter"
SHELTER_FILENAME = "shelter.dontfwithme"
CONFIG_FILENAME = "config.toml"

SHELTER_DIR = Path.home() / HIDDEN_DIR_NAME
CONFIG_FILE = SHELTER_DIR / CONFIG_FILENAME

def get_shelter_path(name:str) -> Path:
    return SHELTER_DIR / f"{name}.dontfwithme"

def get_shelter_meta_path(name:str) -> Path:
    return SHELTER_DIR / f"{name}.meta"
