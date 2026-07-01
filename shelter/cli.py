import os
import subprocess # what's that?
import click
from shelter.constants import CONFIG_FILE
from shelter.vault import add_entry, get_entry, list_entries, change_password, remove_entry, update_entry
from shelter.models import ShelterEntry
import shelter.config as cfg


def _ask_password():
    return click.prompt("Master password", hide_input=True)

@click.group
def cli():
    pass

# add
@cli.command()
@click.argument("name")
@click.option("--secret", required=True, help="Secret value")
def add(name, secret):
    password = _ask_password()
    entry = ShelterEntry(name=name, value=secret, type="text")
    add_entry(entry, password)

#get
@cli.command()
@click.argument("name")
def get(name):
    password = _ask_password()
    entry = get_entry(name, password)
    if entry is None:
        click.echo(f"Not found an {name}")
        return
    click.echo(entry.value)


@cli.command("list")
def list_cmd():
    password = _ask_password()
    entries = list_entries(password)

    if not entries:
        #todo add name if not empty
        click.echo("Shelter is empty")
        return

    for entry in entries:
        tag = f"[{entry.type}]"
        click.echo(f"{tag[:8]} {entry.name} {entry.created_at}")

@cli.command()
@click.argument("name")
def remove(name):
    password = _ask_password()
    confirmation = click.confirm(f"Are ypu sure you want to remove {name}?")
    if not confirmation:
        click.echo("Cancelled")
        return

    remove_entry(name, password)
    click.echo(f"Removed {name}")

@cli.command()
@click.argument("name")
@click.option("--secret", required=False, help="New secret value")
@click.option("--new-name", required=False, help="New secret name")
def update(name, secret, new_name):
    if not secret and not new_name:
        click.echo("Error: provide --secret or --new-name")
        return

    password = _ask_password()
    confirmation = click.confirm(f"Are ypu sure you want to change {name}?")

    if not confirmation:
        click.echo("Cancelled")
        return

    update_entry(name, password, secret , new_name)
    click.echo(f"Update: {name}")

@cli.command()
def passwd():
    old = click.prompt("Current password", hide_input=True)
    new = click.prompt("New password", hide_input=True)
    confirm = click.prompt("Confirm new password", hide_input=True)

    if new != confirm:
        click.echo("Error: passwords do not match")
        return

    change_password(old, new)
    click.echo("Password changed")

@cli.command()
@click.argument("cmd", nargs=-1)
def run(cmd):
    password = _ask_password()
    entries = list_entries(password)
    if not entries:
        click.echo("Vault is empty")
        return

    env = os.environ.copy()

    for entry in entries:
        if entry.type == "text":
            env[entry.name.upper()] = entry.value

    cmd = list(cmd)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]

    if not cmd:
        print("Error: no command provided. Usage: shelter run -- python app.py")
        return

    subprocess.run(cmd, env=env)


@cli.group()
def config():
    """Config commands group"""
    pass

@config.command("list")
def config_list():
    settings = cfg.load_config()
    click.echo("[defaults]")
    for key, value in settings.items():
        print(f" {key} : {value}")

@config.command("get")
@click.argument("key")
def config_get(key):
    value = cfg.get_setting(key)

    if value is None:
        click.echo(f"There's no such option {value}")
    else:
        click.echo(f"{key} = {value}")

@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    try:
        cfg.set_setting(key, value)
        click.echo(f"{key} = {value}")
    except ValueError as e:
        click.echo(f"Error: {e}")

@config.command("path")
def config_path():
    click.echo(CONFIG_FILE)

@config.command("reset")
def config_reset():
    confirmation = click.confirm("Reset all settings to defaults?")

    if confirmation:
        cfg.reset_config()
        click.echo("Config reset")
    else:
        click.echo("Canceled config resting")


def main():
    cli()