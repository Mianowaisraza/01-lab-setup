#!/usr/bin/env python3
"""
============================================================
  Lab Environment Verifier
  CEH Journey — Week 1 | Assessment 1
  Author : Muhammad Owais Raza
  GitHub : https://github.com/Mianowaisraza
  
  Description:
  Automatically verifies your ethical hacking lab setup
  by checking network interfaces, IP configuration,
  and connectivity between lab machines.
  
  Usage: sudo python3 lab_verifier.py
============================================================
"""

import subprocess
import platform
import ipaddress
import sys
import os
from datetime import datetime

# ── COLORS ──────────────────────────────────────────────
R  = "\033[91m"   # Red
G  = "\033[92m"   # Green
Y  = "\033[93m"   # Yellow
B  = "\033[94m"   # Blue
C  = "\033[96m"   # Cyan
W  = "\033[97m"   # White
M  = "\033[95m"   # Magenta
RS = "\033[0m"    # Reset

# ── LAB CONFIGURATION ───────────────────────────────────
LAB_CONFIG = {
    "network"      : "150.1.7.0/24",
    "host_ip"      : "150.1.7.100",
    "attacker_ip"  : "150.1.7.101",
    "target_ip"    : "150.1.7.104",
    "subnet_mask"  : "255.255.255.0",
    "machines": {
        "150.1.7.100": "Windows Host",
        "150.1.7.101": "Parrot OS (Attacker)",
        "150.1.7.102": "Windows 10 (Victim #1)",
        "150.1.7.103": "EVE-NG (Cisco IOS)",
        "150.1.7.104": "Metasploitable2 (Target)",
    }
}

# ── RESULTS TRACKER ─────────────────────────────────────
results = {
    "passed": 0,
    "failed": 0,
    "warnings": 0
}

# ── HELPERS ─────────────────────────────────────────────
def banner():
    os.system("clear" if platform.system() != "Windows" else "cls")
    print(f"""{C}
╔══════════════════════════════════════════════════════════╗
║         ETHICAL HACKING LAB VERIFIER                    ║
║         CEH Journey — Week 1 | Assessment 1             ║
║         Author: Muhammad Owais Raza                     ║
╚══════════════════════════════════════════════════════════╝{RS}
    """)
    print(f"{W}  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RS}")
    print(f"{W}  Platform : {platform.system()} {platform.release()}{RS}")
    print(f"{W}  Network  : {LAB_CONFIG['network']}{RS}\n")

def divider(title):
    print(f"\n{M}{'─'*55}{RS}")
    print(f"{W}  {title}{RS}")
    print(f"{M}{'─'*55}{RS}")

def passed(msg):
    results["passed"] += 1
    print(f"  {G}[✓] PASS{RS} — {msg}")

def failed(msg):
    results["failed"] += 1
    print(f"  {R}[✗] FAIL{RS} — {msg}")

def warning(msg):
    results["warnings"] += 1
    print(f"  {Y}[!] WARN{RS} — {msg}")

def info(msg):
    print(f"  {B}[i]{RS} — {msg}")

# ── CHECK 1: OPERATING SYSTEM ───────────────────────────
def check_os():
    divider("CHECK 1 — Operating System")
    os_name = platform.system()
    info(f"Detected OS: {os_name} {platform.release()}")
    
    if os_name == "Linux":
        passed("Running on Linux — ideal for penetration testing")
        # Check if Kali or Parrot
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
            if "parrot" in content:
                passed("Parrot OS detected — attacker machine confirmed")
            elif "kali" in content:
                passed("Kali Linux detected — attacker machine confirmed")
            else:
                warning("Linux detected but not Parrot/Kali — verify this is correct")
        except:
            warning("Could not read OS release info")
    elif os_name == "Windows":
        warning("Running on Windows — this may be the host machine")
    else:
        warning(f"Unexpected OS: {os_name}")

# ── CHECK 2: NETWORK INTERFACES ─────────────────────────
def check_interfaces():
    divider("CHECK 2 — Network Interfaces")
    
    try:
        if platform.system() == "Linux":
            result = subprocess.run(
                ["ip", "addr", "show"],
                capture_output=True, text=True
            )
            output = result.stdout
            info("Network interfaces found:")
            
            # Parse interfaces
            current_iface = None
            lab_ip_found = False
            
            for line in output.splitlines():
                if ": " in line and not line.startswith(" "):
                    parts = line.split(": ")
                    if len(parts) >= 2:
                        current_iface = parts[1].split("@")[0]
                        print(f"  {C}  Interface: {current_iface}{RS}")
                
                if "inet " in line:
                    ip = line.strip().split()[1].split("/")[0]
                    print(f"  {W}    IP: {ip}{RS}")
                    
                    # Check if lab IP
                    try:
                        if ipaddress.ip_address(ip) in ipaddress.ip_network(LAB_CONFIG["network"], strict=False):
                            passed(f"Lab network IP found: {ip}")
                            lab_ip_found = True
                            
                            # Check if it matches expected attacker IP
                            if ip == LAB_CONFIG["attacker_ip"]:
                                passed(f"Attacker IP correctly configured: {ip}")
                            else:
                                warning(f"IP {ip} is in lab network but not the expected attacker IP ({LAB_CONFIG['attacker_ip']})")
                    except ValueError:
                        pass
            
            if not lab_ip_found:
                failed(f"No IP found in lab network {LAB_CONFIG['network']}")
                info(f"Expected attacker IP: {LAB_CONFIG['attacker_ip']}")
                info("Fix: sudo nano /etc/network/interfaces")
                
        elif platform.system() == "Windows":
            result = subprocess.run(
                ["ipconfig"],
                capture_output=True, text=True
            )
            print(result.stdout[:500])
            
    except Exception as e:
        failed(f"Could not check interfaces: {e}")

# ── CHECK 3: PING CONNECTIVITY ───────────────────────────
def check_connectivity():
    divider("CHECK 3 — Network Connectivity")
    
    machines_to_check = {
        LAB_CONFIG["host_ip"]    : "Windows Host",
        LAB_CONFIG["target_ip"]  : "Metasploitable2 (Target)",
    }
    
    for ip, name in machines_to_check.items():
        info(f"Pinging {name} ({ip})...")
        try:
            if platform.system() == "Linux":
                cmd = ["ping", "-c", "3", "-W", "2", ip]
            else:
                cmd = ["ping", "-n", "3", "-w", "2000", ip]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Extract packet loss
                output = result.stdout
                if "0%" in output or "0 received" not in output:
                    passed(f"{name} ({ip}) — reachable ✓")
                else:
                    failed(f"{name} ({ip}) — 100% packet loss")
            else:
                failed(f"{name} ({ip}) — unreachable")
                info(f"Make sure {name} VM is powered on")
                
        except subprocess.TimeoutExpired:
            failed(f"{name} ({ip}) — ping timed out")
        except Exception as e:
            failed(f"Could not ping {name}: {e}")

# ── CHECK 4: REQUIRED TOOLS ──────────────────────────────
def check_tools():
    divider("CHECK 4 — Required Security Tools")
    
    tools = {
        "nmap"      : "Network scanner — required for CEH labs",
        "hping3"    : "TCP/IP packet assembler — required for Assessment 4",
        "wireshark" : "Packet analyzer — required for Assessment 3",
        "python3"   : "Python runtime — required for automation scripts",
        "git"       : "Version control — required for GitHub uploads",
    }
    
    for tool, description in tools.items():
        try:
            result = subprocess.run(
                ["which", tool],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                path = result.stdout.strip()
                passed(f"{tool} — found at {path}")
            else:
                failed(f"{tool} — NOT installed | {description}")
                info(f"Fix: sudo apt install {tool} -y")
        except Exception as e:
            warning(f"Could not check {tool}: {e}")

# ── CHECK 5: LAB NETWORK RANGE ───────────────────────────
def check_network_range():
    divider("CHECK 5 — Lab Network Validation")
    
    network = LAB_CONFIG["network"]
    info(f"Expected lab network: {network}")
    
    try:
        net = ipaddress.ip_network(network, strict=False)
        info(f"Network address : {net.network_address}")
        info(f"Broadcast       : {net.broadcast_address}")
        info(f"Total hosts     : {net.num_addresses - 2}")
        info(f"Subnet mask     : {net.netmask}")
        
        # Validate all lab IPs are in range
        for ip, name in LAB_CONFIG["machines"].items():
            try:
                if ipaddress.ip_address(ip) in net:
                    passed(f"{name} ({ip}) — in correct network range")
                else:
                    failed(f"{name} ({ip}) — NOT in network range {network}")
            except ValueError:
                failed(f"Invalid IP in config: {ip}")
                
    except ValueError as e:
        failed(f"Invalid network configuration: {e}")

# ── SUMMARY ──────────────────────────────────────────────
def print_summary():
    total = results["passed"] + results["failed"] + results["warnings"]
    
    print(f"\n{C}{'═'*55}{RS}")
    print(f"{W}  LAB VERIFICATION SUMMARY{RS}")
    print(f"{C}{'═'*55}{RS}")
    print(f"  {G}Passed   : {results['passed']}{RS}")
    print(f"  {R}Failed   : {results['failed']}{RS}")
    print(f"  {Y}Warnings : {results['warnings']}{RS}")
    print(f"  {W}Total    : {total}{RS}")
    print(f"{C}{'═'*55}{RS}")
    
    if results["failed"] == 0:
        print(f"\n  {G}✓ LAB IS FULLY OPERATIONAL{RS}")
        print(f"  {G}  Ready for penetration testing!{RS}")
    elif results["failed"] <= 2:
        print(f"\n  {Y}⚠ LAB PARTIALLY CONFIGURED{RS}")
        print(f"  {Y}  Fix the failed checks above{RS}")
    else:
        print(f"\n  {R}✗ LAB SETUP INCOMPLETE{RS}")
        print(f"  {R}  Review failed checks and reconfigure{RS}")
    
    print(f"\n  {B}GitHub : github.com/Mianowaisraza{RS}")
    print(f"  {B}Author : Muhammad Owais Raza{RS}\n")

# ── MAIN ─────────────────────────────────────────────────
def main():
    banner()
    check_os()
    check_interfaces()
    check_connectivity()
    check_tools()
    check_network_range()
    print_summary()

if __name__ == "__main__":
    main()
