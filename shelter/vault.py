import json
from shelter.crypto import encrypt, decrypt
from shelter.models import ShelterEntry
from shelter.constants import SHELTER_FILE_PATH

def _load_raw(password:str) -> dict:
    if not SHELTER_FILE_PATH.exists():
        return {} 
    
    token = SHELTER_FILE_PATH.read_bytes()
    plain_text= decrypt(token, password)
    return json.loads(plain_text.decode())

def _save_raw(data: dict, password: str) -> None:
    SHELTER_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    plaintext = json.dumps(data).encode()
    token = encrypt(plaintext, password)
    SHELTER_FILE_PATH.write_bytes(token)

def _entry(name:str, e:dict) -> ShelterEntry:
    return ShelterEntry(
            name=name,
            value=e["value"],
            type = e["type"],
            filename= e["filename"],
            created_at = e["created_at"]
        )

def add_entry(entry:ShelterEntry, password:str):
    data = _load_raw(password)
    data[entry.name] = {
        "value" : entry.value,
        "type" : entry.type,
        "filename" : entry.filename,
        "created_at": entry.created_at
    }
    _save_raw(data, password)

def get_entry(name:str, password:str) -> ShelterEntry | None:
    data = _load_raw(password)

    if name not in data:
        return None
    
    e = data[name]

    return _entry(name, e)

def list_entries(password:str) -> list[ShelterEntry]:
    data = _load_raw(password)
    return [
        _entry(name, e)
        for name, e in data.items()
    ]


def remove_entry(name:str, passwd:str):
    data = _load_raw(passwd)

    if name not in data:
        print(f"Error: '{name}' not found")
        return

    data.pop(name)
    _save_raw(data, passwd)

def update_entry(name:str, secret:str, passwd:str):
    data = _load_raw(passwd)
    if name not in data:
        print(f"Error: '{name}' not found")
        return
    data[name]["value"] = secret
    _save_raw(data, passwd)

def change_password(old_password:str, new_password:str):
    data = _load_raw(old_password)
    _save_raw(data, new_password)