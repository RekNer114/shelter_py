import argparse
import getpass
import base64
from shelter.vault import add_entry, get_entry, list_entries
from shelter.models import ShelterEntry
from pathlib import Path

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="shelter",
        description="Local encrypted secrets manager"
    )
    
    subparser = parser.add_subparsers(dest="command", required=True)

    add_parser = subparser.add_parser("add", help="Add a secret")
    add_parser.add_argument("name", help="Secret name, e.g. github")
    add_parser.add_argument("--secret", required=True, help="The secret value")

    get_parser = subparser.add_parser("get", help="Get a secret")
    get_parser.add_argument("name", help="Secret name")

    subparser.add_parser('list', help="list secret names")

    return parser.parse_args()


def process_add(args : argparse.Namespace, password:str):
    if args.secret:
        entry = ShelterEntry(name=args.name, value=args.secret, type="text")
    else:
        print("Error: provide --secret or --file")
        return
    
    add_entry(entry, password)
    print(f"Stored: {args.name}")


def process_get(args : argparse.Namespace, password:str):
    entry = get_entry(args.name, password)
    if entry is None:
        print(f"Not found: {args.name}")
        return
    if entry.type == "file":
        out = Path(args.output) if args.output else Path(entry.filename)
        out.write_bytes(base64.b64decode(entry.value))
        print(f"Written to: {out}")
    else:
        print(entry.value)

def process_list(args : argparse.Namespace, password:str):
    entries = list_entries(password)
    if not entries:
        print("Vault is empty")
        return
    for e in entries:
        tag = f"[{e.type}]"
        print(f"{tag:8} {e.name:20} {e.created_at}")

def main():
    
    args = _parse_args()
    
    #to hide what currently typed
    password = getpass.getpass("Master password: ")

    match args.command:
        case "add":
            process_add(args, password)
        case "get":
            process_get(args, password)
        case "list":
            process_list(args, password)
        case _:
            print("wrong command")