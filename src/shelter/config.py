from shelter.constants import CONFIG_FILE, SHELTER_DIR
import tomlkit


VALID_KEYS = {
    "auth" : ["password", "key", "key+password"],
    "ssh-key" : None,
    "vault": None #todo add possibility to add a few vaults
}

DEFAULT_CONFIG = """\
[defaults]
auth = "password"
"""


def ensure_config():
    SHELTER_DIR.mkdir(mode=0o700, exist_ok=True)

    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(DEFAULT_CONFIG)
        CONFIG_FILE.chmod(0o600)


def _load_raw() -> tomlkit.TOMLDocument:
    ensure_config()
    return tomlkit.parse(CONFIG_FILE.read_text())

def _save_raw(conf : tomlkit.TOMLDocument):
    CONFIG_FILE.write_text(tomlkit.dumps(conf))

def load_config() -> dict:
    doc = _load_raw()
    return dict(doc.get("defaults", {}))



def get_setting(key: str) -> str | None:
    return load_config().get(key)

def set_setting(key:str, value:str):
    if key not in VALID_KEYS:
        raise ValueError(f"There's no such option \"{key}\". Valid config options: {''.join(VALID_KEYS)}")

    allowed = VALID_KEYS[key]
    if allowed is not None and value not in allowed:
        raise ValueError(f"Invalid value '{value}'. Allowed: {', '.join(allowed)}")

    doc = _load_raw()
    doc["defaults"][key] = value
    _save_raw(doc)


def reset_config():
    CONFIG_FILE.write_text(DEFAULT_CONFIG)
    CONFIG_FILE.chmod(0o600)
