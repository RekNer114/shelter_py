# Shelter


Simple encrypted secrets manager.

---

# Setup

- Clone the repository
- Open the project directory
- Create a virtual environment

        uv venv
* Install dependencies

        uv sync
* Install project

        uv pip install -e .

* Also, you can run without installing

        uv run shelter <command>

        
# How to use?

* Adding values to shelter

        shelter -s <shelter-name> add <secret-name> --secret <your-secret>

> [!TIP]
> The -s flag automatically creates a new shelter if it does not exist.
> When you not specifying an <code>-s</code> flag it writes to <mark>default</mark> shelter.

> [!IMPORTANT]
> Each shelter has its own password. You specify it when creating the shelter.


* Getting values

      shelter -s <shelter-name> get <secret-name>
* List secrets in shelter

      shelter -s <shelter-name> list
* List shelters
  
      shelter shelters
* Change password

      shelter -s <shelter-name> passwd
* Update existing secret

      shelter -s <shelter-name> update <secret-name> --new-name <new-name> --secret <new-secret>

* Run other apps with environment variables from shelter

      shelter -s <shelter-name> run <cmd-command>
