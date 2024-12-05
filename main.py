import tkinter as tk
from tkinter import scrolledtext
import platform
import subprocess
import ttkbootstrap as ttk

def get_wifi_passwords_windows():
    passwords = []
    try:
        profiles = subprocess.check_output("netsh wlan show profiles", shell=True).decode().split('\n')
        profiles = [profile.split(":")[1].strip() for profile in profiles if "All User Profile" in profile]
        for profile in profiles:
            try:
                profile_info = subprocess.check_output(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True).decode()
                password_line = [line for line in profile_info.split('\n') if "Key Content" in line]
                if password_line:
                    password = password_line[0].split(":")[1].strip()
                    passwords.append(f"SSID: {profile}, Password: {password}")
            except subprocess.CalledProcessError:
                passwords.append(f"SSID: {profile}, Password: [Error retrieving password]")
    except subprocess.CalledProcessError:
        passwords.append("Error retrieving Wi-Fi profiles")
    return passwords


def get_wifi_passwords_mac():
    passwords = []
    try:
        profiles = subprocess.check_output("security find-generic-password -D 'AirPort network password' -a $(whoami) -s", shell=True).decode()
        passwords.append(profiles)
    except subprocess.CalledProcessError:
        passwords.append("Error retrieving Wi-Fi profiles")
    return passwords


def get_wifi_passwords_linux():
    passwords = []
    try:
        network_manager = subprocess.check_output("nmcli -f NAME connection show", shell=True).decode().split('\n')
        profiles = [profile.strip() for profile in network_manager if profile]
        for profile in profiles:
            try:
                profile_info = subprocess.check_output(f"nmcli connection show \"{profile}\"", shell=True).decode()
                password_line = [line for line in profile_info.split('\n') if "802-11-wireless-security.psk" in line]
                if password_line:
                    password = password_line[0].split(":")[1].strip()
                    passwords.append(f"SSID: {profile}, Password: {password}")
            except subprocess.CalledProcessError:
                passwords.append(f"SSID: {profile}, Password: [Error retrieving password]")
    except subprocess.CalledProcessError:
        passwords.append("Error retrieving Wi-Fi profiles")
    return passwords


def retrieve_passwords():
    os_type = platform.system()
    if os_type == "Windows":
        passwords = get_wifi_passwords_windows()
    elif os_type == "Darwin":
        passwords = get_wifi_passwords_mac()
    elif os_type == "Linux":
        passwords = get_wifi_passwords_linux()
    else:
        passwords = ["Unsupported OS"]
    
    # Display the results in the text box
    result_text.delete(1.0, tk.END)
    for password in passwords:
        result_text.insert(tk.END, password + "\n")
        
def format_text():
    # Apply bold formatting for SSID and Password
    result_text.tag_configure("bold", font=("Helvetica", 12, "bold"))
    pos = '1.0'
    while True:
        pos = result_text.search("SSID:", pos, nocase=1, stopindex=tk.END)
        if not pos:
            break
        end_pos = f"{pos} + {len('SSID:')}c"
        result_text.tag_add("bold", pos, end_pos)
        pos = end_pos

    pos = '1.0'
    while True:
        pos = result_text.search("Password:", pos, nocase=1, stopindex=tk.END)
        if not pos:
            break
        end_pos = f"{pos} + {len('Password:')}c"
        result_text.tag_add("bold", pos, end_pos)
        pos = end_pos