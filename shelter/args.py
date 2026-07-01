import argparse

def parse_args() -> argparse.Namespace:
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

    # config commands
    config_parser = subparser.add_parser("config", help="Manage settings")
    config_subparser = config_parser.add_subparsers(dest="config_command", required=True)

    config_subparser.add_parser("list", help="Show all settings")

    # config get key
    cg = config_subparser.add_parser("get", help="Get one setting")
    cg.add_argument("key", help="Setting name")

    # config set key value
    cs = config_subparser.add_parser("set", help="Change a setting")
    cs.add_argument("key", help="Setting name")
    cs.add_argument("value", help="New value")

    subparser.add_parser('list', help="list secret names")

    config_subparser.add_parser("path", help="Show config file location")

    config_subparser.add_parser("reset", help="Reset config to defaults")

    subparser.add_parser("passwd", help="Change master password")

    remove_parser = subparser.add_parser("remove", help="Remove entry")
    remove_parser.add_argument("name", help="Secret name")

    update_parser = subparser.add_parser("update", help="Updates only a secret, but not entry metadata")
    update_parser.add_argument("name", help="Secrets name")
    update_parser.add_argument("--secret", required=True, help="The secret value")

    run_parser = subparser.add_parser("run", help="Run command with secrets injected as env vars")
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run, e.g. -- python app.py")
    return parser.parse_args()