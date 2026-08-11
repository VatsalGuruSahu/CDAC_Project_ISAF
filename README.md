# Infrastructure Security Automation Framework (ISAF)

## Project Description

Infrastructure Security Automation Framework (ISAF) is a small centralized security automation project for managing Ubuntu client machines from one administrator computer.

The project uses **Python, Ansible, SSH, UFW, Fail2Ban, JSON and Streamlit**.

From the Streamlit dashboard, the administrator can:

- Run a security scan on all client machines
- Check system information
- Check UFW firewall status and allowed ports
- Check Fail2Ban status and configuration
- Configure the firewall when required
- Configure Fail2Ban when required
- View the collected results through the dashboard

The current setup uses **one Admin/Control machine and two Ubuntu 24.04 client machines**.

---

## 1. Machine Setup

Use the following setup:

```text
Admin Computer
Ubuntu 24.04
IP: <ADMIN-IP>
        |
        | SSH
        |
        +-------------------+
        |                   |
        v                   v
   Client 1               Client 2
   Ubuntu 24.04           Ubuntu 24.04
   IP: <CLIENT-IP>        IP: <CLIENT-IP>
```

The Admin computer runs Python, Ansible and Streamlit.

The two client computers only need SSH access and the required sudo privileges.

---

# 2. Setup the Admin Computer

Open a terminal on the Admin computer.

### Update packages

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Python, pip, venv, vim, SSH and Ansible

```bash
sudo apt install -y python3 python3-pip python3-venv vim openssh-client ansible
```

Check the installations:

```bash
python3 --version
pip3 --version
ansible --version
ssh -V
```

---

# 3. Create the Project Environment

Go to the project directory:

```bash
cd ~/CDAC_Project_ISAF
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

After activation, the terminal should show something similar to:

```text
(venv) user@admin:~/CDAC_Project_ISAF$
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install Streamlit inside the virtual environment:

```bash
pip install streamlit
```

---

# 4. Setup the Client Machines

Perform these steps on **Client 1 and Client 2**.

### Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

### Install SSH server

```bash
sudo apt install -y openssh-server
```

Enable and start SSH:

```bash
sudo systemctl enable --now ssh
```

Check SSH:

```bash
sudo systemctl status ssh
```

The client machines must have reachable IP addresses.

For this project:

```text
Client 1: <CLIENT1-IP>
Client 2: <CLIENT2-IP>
```

Verify the IP on each client:

```bash
ip addr
```

---

# 5. Configure SSH Access from Admin to Clients

On the Admin computer, create an SSH key if you do not already have one:

```bash
ssh-keygen -t ed25519
```

Press Enter for the default file location. A passphrase can be left empty for this project setup.

Copy the public key to Client 1:

```bash
ssh-copy-id username@<CLIENT1-IP>
```

Copy it to Client 2:

```bash
ssh-copy-id username@<CLIENT2-IP>
```

Test both connections:

```bash
ssh username@<CLIENT1-IP>
```

```bash
ssh username@<CLIENT2-IP>
```

If both logins work without asking for the SSH password, the SSH setup is ready.

Replace `username` with the actual username used on the client machines.

---

# 6. Configure Passwordless Sudo with visudo

Ansible needs sudo privileges on the client machines to perform security checks and configuration tasks.

On **each client machine**, run:

```bash
sudo visudo
```

Add the following line at the end:

```text
username ALL=(ALL) NOPASSWD:ALL
```

Replace `username` with the client user's actual username.


Save and exit.

Using `visudo` is recommended because it checks the sudoers file for syntax errors before saving.

### Test passwordless sudo

On the client:

```bash
sudo -n whoami
```

The expected output is:

```text
root
```

Do this on both Client 1 and Client 2.

---

# 7. Configure the Ansible Inventory

On the Admin computer, open:

```bash
vim inventory.ini
```

Use:

```ini
[all]
client1 ansible_host=<CLIENT1-IP>
client2 ansible_host=<CLIENT2-IP>
```

---

# 8. Test Ansible Connection

From the Admin computer:

```bash
ansible -i inventory.ini all -m ping
```

Expected result:

```text
client1 | SUCCESS => {
    "ping": "pong"
}

client2 | SUCCESS => {
    "ping": "pong"
}
```

If both clients return `SUCCESS`, the Admin computer can communicate with both clients through Ansible.

---

# 9. Run the Project

Make sure the virtual environment is active:

```bash
cd ~/CDAC_Project_ISAF
source venv/bin/activate
```

Run the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will display the local address in the terminal. Open that address in a browser on the Admin computer.

---

# 10. Basic Usage

From the dashboard:

### Run Security Scan

The scan checks the client machines for:

- System information
- UFW firewall status
- Allowed firewall ports
- Fail2Ban status
- Fail2Ban configuration

The results are saved under the project's `results/` directory and consolidated into the project report used by the dashboard.

### Configure Firewall

Use this when the security scan shows that the firewall needs to be configured.

After configuration, run **Security Scan** again to verify the result.

### Configure Fail2Ban

Use this when Fail2Ban needs to be installed or configured.

After configuration, run **Security Scan** again to verify the result.

---

## Important

The recommended order is:

```text
1. Set up Admin computer
2. Set up both Client computers
3. Configure SSH
4. Configure passwordless sudo using visudo
5. Configure inventory.ini
6. Test SSH
7. Test Ansible
8. Activate venv
9. Start Streamlit
10. Run Security Scan
11. Configure Firewall / Fail2Ban if required
12. Run Security Scan again to verify
```

This project is currently intended for **Ubuntu 24.04 client machines** and is designed as a simple academic Linux Infrastructure Security Automation Framework.

