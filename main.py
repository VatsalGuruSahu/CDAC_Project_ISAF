import subprocess
import json
from pathlib import Path

# ---------------------------------------
# Project Paths
# ---------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

PLAYBOOK = PROJECT_DIR / "playbooks" / "security.yml"
INVENTORY = PROJECT_DIR / "inventory.ini"
RESULTS = PROJECT_DIR / "results"
REPORT_FILE = RESULTS / "reports.json"

# ---------------------------------------
# Run Ansible Playbook
# ---------------------------------------

def run_scan():

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

# ---------------------------------------
# Read JSON
# ---------------------------------------

def load_reports():

    data = {}

    if not RESULTS.exists():
        return data

    for client in RESULTS.iterdir():

        if not client.is_dir():
            continue

        client_reports = {}

        for report in client.glob("*.json"):

            with open(report, "r") as f:
                client_reports[report.stem] = json.load(f)

        data[client.name] = client_reports

    return data

# ---------------------------------------
# Save Combined Report
# ---------------------------------------

def save_reports(data):

    with open(REPORT_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------------------
# Main Function
# ---------------------------------------

def scan():

    run_scan()

    reports = load_reports()

    save_reports(reports)

    return reports

# ---------------------------------------
# Testing
# ---------------------------------------

if __name__ == "__main__":

    reports = scan()

    print(json.dumps(reports, indent=4))
