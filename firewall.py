import subprocess
from pathlib import Path

# ---------------------------------------
# Project Paths
# ---------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

PLAYBOOK = PROJECT_DIR / "playbooks" / "firewall.yml"
INVENTORY = PROJECT_DIR / "inventory.ini"

# ---------------------------------------
# Run Firewall Playbook
# ---------------------------------------

def configure_firewall():

    command = [
        "ansible-playbook",
        "-i",
        str(INVENTORY),
        str(PLAYBOOK)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return True


# ---------------------------------------
# Testing
# ---------------------------------------

if __name__ == "__main__":

    try:

        configure_firewall()

        print("=" * 50)
        print("Firewall configured successfully.")
        print("=" * 50)
        print()
        print("Please run 'Run Security Scan' again to refresh the firewall status and reports.")

    except Exception as e:

        print("=" * 50)
        print("Firewall configuration failed.")
        print("=" * 50)
        print()
        print(e)
