import argparse
import getpass
import base64
from argparse import Namespace

from shelter.constants import CONFIG_FILE
from shelter.vault import add_entry, get_entry, list_entries, change_password, remove_entry, update_entry
from shelter.models import ShelterEntry
from pathlib import Path
import shelter.config as config
from shelter.args import parse_args


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

def process_list( password:str):
    entries = list_entries(password)
    if not entries:
        print("Vault is empty")
        return
    for e in entries:
        tag = f"[{e.type}]"
        print(f"{tag:8} {e.name:20} {e.created_at}")


def process_config(args : argparse.Namespace):
    match args.config_command:
        case "list":
            settings = config.load_config()
            print("[defaults]")
            for key, value in settings.items():
                print(f" {key} : {value}")
        case "get":
            value = config.get_setting(args.key)

            if value is None:
                print(f"There's no such option {value}")
            else:
                print(f"{args.key} = {value}")
        case "set":
            try:
                config.set_setting(args.key, args.value)
            except ValueError as e:
                print(f"Error: {e}")
        case "path":
            print(CONFIG_FILE)
        case "reset":
            confirmation = input("Reset all settings to defaults? [y/n] ")

            if confirmation.lower() == "y":
                config.reset_config()
                print("Config reset")
            else:
                print("Canceled config reseting")


def process_passwd(old : str):
    new = getpass.getpass("New password: ")
    new_confirm = getpass.getpass("Confirm new password: ")

    if new != new_confirm:
        print("Error: pawsswords doesn't match")
        return

    try:
        change_password(old, new)
        print("Password changed")
    except Exception:
        print("Error: invalid password")


def process_remove(args:argparse.Namespace, password : str):
    remove_conf = input("Are you sure you want to remove the password? [y/n] ")

    if remove_conf.lower() != 'y':
        print("removing canceled")
        return

    remove_entry(args.name, password)
    print(f"Secret {args.name} was removed.")


def process_update(args, password):
    update_conf = input("Are you sure you want to update the password? [y/n] ")

    if update_conf.lower() != 'y':
        print("updating canceled")
        return

    if args.secret:
        update_entry(args.name, args.secret, password)
        print(f"Entry {args.name} was update successfully")
    else:
        print("Error: provide --secret or --file")
    return

def main():
    
    args = parse_args()

    if args.command == "config":
        process_config(args)
        return

    #to hide what currently typed
    password = getpass.getpass("Master password: ")

    match args.command:
        case "add":
            process_add(args, password)
        case "get":
            process_get(args, password)
        case "list":
            process_list(password)
        case "passwd":
            process_passwd(password)
        case "remove":
            process_remove(args, password)
        case "update":
            """updating only a secret and nothing else. Creation date will be the same"""
            process_update(args, password)
        case _:
            print("wrong command")