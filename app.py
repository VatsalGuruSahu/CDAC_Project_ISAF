import streamlit as st
import json
from pathlib import Path

from main import scan
from firewall import configure_firewall
from fail2ban import configure_fail2ban

# ---------------------------------------
# Paths
# ---------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
REPORT_FILE = PROJECT_DIR / "results" / "reports.json"

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Infrastructure Security Automation Framework",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Infrastructure Security Automation Framework")

st.write("---")

# ---------------------------------------
# Run Scan Button
# ---------------------------------------

if st.button("Run Security Scan", use_container_width=True):

    with st.spinner("Scanning all clients..."):

        try:
            scan()
            st.success("Security Scan Completed Successfully.")

        except Exception as e:
            st.error(str(e))

st.write("---")

if st.button("Configure Firewall", use_container_width=True):

    with st.spinner("Configuring Firewall..."):

        try:

            configure_firewall()

            st.success(
                "Firewall configured successfully.\n\n"
                "Please click **Run Security Scan** to refresh the firewall status."
            )

        except Exception as e:

            st.error(str(e))

st.write("")

if st.button("Configure Fail2Ban", use_container_width=True):

    with st.spinner("Configuring Fail2Ban..."):

        try:

            configure_fail2ban()

            st.success(
                "Fail2Ban configured successfully.\n\n"
                "Please click **Run Security Scan** to refresh the Fail2Ban status."
            )

        except Exception as e:

            st.error(str(e))
# ---------------------------------------
# Read reports.json
# ---------------------------------------

if REPORT_FILE.exists():

    with open(REPORT_FILE, "r") as f:
        reports = json.load(f)

    for client, data in reports.items():

        st.header(client.upper())

        col1, col2 = st.columns(2)

        # ---------------------------------------
        # System Information
        # ---------------------------------------

        with col1:

            st.subheader("System Information")

            sys = data.get("systeminfo", {})

            st.write("**Hostname:**", sys.get("hostname", "-"))
            st.write("**Operating System:**", sys.get("os", "-"))
            st.write("**CPU Cores:**", sys.get("cpu_cores", "-"))
            st.write("**RAM (MB):**", sys.get("ram_mb", "-"))
            st.write("**Disk (GB):**", sys.get("disk_total_gb", "-"))
            st.write("**IP Address:**", sys.get("ip", "-"))
            st.write("**Uptime:**", sys.get("uptime", "-"))

        # ---------------------------------------
        # Firewall
        # ---------------------------------------

        with col2:

            st.subheader("Firewall")

            fw = data.get("firewall", {})

            installed = fw.get("installed", False)
            status = fw.get("status", "-")

            st.write("**Installed:**", installed)
            st.write("**Status:**", status)

            st.write("**Allowed Ports:**")

            ports = fw.get("allowed_ports", [])

            if ports:
                for port in ports:
                    st.write("•", port)
            else:
                st.write("No allowed ports found.")

        st.divider()

        #-------------------------------------------
        # Fail2Ban
        #-------------------------------------------

        st.subheader("Fail2Ban")

        f2b = data.get("fail2ban", {})

        installed = f2b.get("installed", False)
        status = f2b.get("status", "-")
        bantime = f2b.get("bantime", "-")
        findtime = f2b.get("findtime", "-")
        maxretry = f2b.get("maxretry", "-")

        st.write("**Installed:**", installed)
        st.write("**Status:**", status)
        st.write("**Ban Time:**", bantime)
        st.write("**Find Time:**", findtime)
        st.write("**Max Retry:**", maxretry)


else:

    st.info("No reports found. Click 'Run Security Scan' to generate reports.")
