import json
from shelter.crypto import encrypt, decrypt
from shelter.models import ShelterEntry
from shelter.constants import get_shelter_path, DEFAULT_SHELTER_NAME, SHELTER_DIR

def _load_raw(password:str, shelter_name:str) -> dict:
    path = get_shelter_path(shelter_name)

    if not path.exists():
        return {} 
    
    token = path.read_bytes()
    plain_text= decrypt(token, password)
    return json.loads(plain_text.decode())

def _save_raw(data: dict, password: str, shelter_name:str) -> None:
    path = get_shelter_path(shelter_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    plaintext = json.dumps(data).encode()
    token = encrypt(plaintext, password)
    path.write_bytes(token)

def _entry(name:str, e:dict) -> ShelterEntry:
    return ShelterEntry(
            name=name,
            value=e["value"],
            type = e["type"],
            filename= e["filename"],
            created_at = e["created_at"]
        )

def add_entry(entry:ShelterEntry, password:str, shelter_name:str = DEFAULT_SHELTER_NAME):
    data = _load_raw(password, shelter_name)
    data[entry.name] = {
        "value" : entry.value,
        "type" : entry.type,
        "filename" : entry.filename,
        "created_at": entry.created_at
    }
    _save_raw(data, password, shelter_name)

def get_entry(name:str, password:str, shelter_name:str = DEFAULT_SHELTER_NAME) -> ShelterEntry | None:
    data = _load_raw(password, shelter_name)

    if name not in data:
        return None
    
    e = data[name]

    return _entry(name, e)

def list_shelters() -> list[str]:
    #f.stem - filename without extension
    return [f.stem for f in SHELTER_DIR.glob("*.dontfwithme")]


def list_entries(password:str, shelter_name:str = DEFAULT_SHELTER_NAME) -> list[ShelterEntry]:
    data = _load_raw(password, shelter_name)
    return [
        _entry(name, e)
        for name, e in data.items()
    ]


def remove_entry(name:str, passwd:str, shelter_name:str = DEFAULT_SHELTER_NAME):
    data = _load_raw(passwd, shelter_name)

    if name not in data:
        print(f"Error: '{name}' not found")
        return

    data.pop(name)
    _save_raw(data, passwd, shelter_name)

def update_entry(name:str, passwd:str, secret:str = None,  new_name:str=None, shelter_name:str = DEFAULT_SHELTER_NAME):
    data = _load_raw(passwd,shelter_name)

    if name not in data:
        print(f"Error: '{name}' not found")
        return

    if secret is not None:
        data[name]["value"] = secret

    if new_name is not None:
        data[new_name] = data.pop(name) #renaming key

    _save_raw(data, passwd, shelter_name)

def change_password(old_password:str, new_password:str, shelter_name:str = DEFAULT_SHELTER_NAME):
    data = _load_raw(old_password, shelter_name)
    _save_raw(data, new_password, shelter_name)