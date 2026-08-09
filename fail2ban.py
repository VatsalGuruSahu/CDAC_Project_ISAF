import subprocess
from pathlib import Path

# ---------------------------------------
# Project Paths
# ---------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

PLAYBOOK = PROJECT_DIR / "playbooks" / "fail2ban.yml"
INVENTORY = PROJECT_DIR / "inventory.ini"

# ---------------------------------------
# Run Fail2Ban Playbook
# ---------------------------------------

def configure_fail2ban():

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

        configure_fail2ban()

        print("=" * 50)
        print("Fail2Ban configured successfully.")
        print("=" * 50)
        print()
        print("Please run 'Run Security Scan' again to refresh the Fail2Ban status and reports.")

    except Exception as e:

        print("=" * 50)
        print("Fail2Ban configuration failed.")
        print("=" * 50)
        print()
        print(e)
