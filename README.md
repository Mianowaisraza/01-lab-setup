# 🔬 Ethical Hacking Lab Setup
### CEH Journey — Week 1 | Assessment 1

![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)
![Tools](https://img.shields.io/badge/Tools-VMware_|_ParrotOS_|_Metasploitable2-blue?style=flat-square)
![Level](https://img.shields.io/badge/Level-Beginner-orange?style=flat-square)

> ⚠️ All testing performed in a completely isolated lab environment. No real-world systems were targeted.

---

## 📌 Objective

Build a fully functional, isolated ethical hacking lab environment from scratch — with an attacker machine, a vulnerable target machine, and a private network between them. This is the foundation for all future penetration testing work.

---

## 🗺️ Network Diagram

```
┌─────────────────────────────────────────────────┐
│                  VMNet1 (Host-Only)              │
│                  150.1.7.0/24                    │
│                                                  │
│   ┌──────────────┐         ┌──────────────────┐  │
│   │  Parrot OS   │         │  Metasploitable2 │  │
│   │  (Attacker)  │◄───────►│    (Target)      │  │
│   │ 150.1.7.101  │         │  150.1.7.104     │  │
│   └──────────────┘         └──────────────────┘  │
│                                                  │
│         Host Machine: 150.1.7.100                │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Tools Used

| Tool | Purpose | Version |
|------|---------|---------|
| VMware Workstation | Virtualization platform | Pro 17+ |
| Parrot OS | Attacker machine (Linux) | Latest |
| Metasploitable 2 | Intentionally vulnerable target | 2.0 |
| VMNet1 | Isolated host-only network | — |

---

## 📋 Key Concepts Covered

### CIA Triad
| Concept | Definition |
|---------|-----------|
| **Confidentiality** | Protecting information from unauthorized access — only authorized users can view sensitive data |
| **Integrity** | Ensuring data remains accurate and unchanged during storage or transmission |
| **Authentication** | Verifying the identity of a user, system, or device before granting access |

### CEH Methodology — 5 Phases
```
1. RECONNAISSANCE  →  Collecting info about target (passive & active)
2. SCANNING        →  Identifying live systems, open ports, vulnerabilities
3. GAINING ACCESS  →  Exploiting vulnerabilities to enter the system
4. MAINTAINING     →  Creating backdoors to keep access
   ACCESS
5. CLEARING TRACKS →  Removing logs and evidence to avoid detection
```

### Key Terminology
| Term | Simple Explanation |
|------|--------------------|
| **Vulnerability** | A weakness or open window in a system |
| **Exploit** | The tool or method used to break through that weakness |
| **Zero-Day** | A brand new vulnerability the creators don't know about yet |
| **Payload** | The harmful part of an attack (e.g., malware, ransomware) |
| **Daisy Chaining** | Hacking one system to hop into another connected to it |
| **Hack Value** | How valuable a target is to an attacker |
| **Bot** | A computer controlled remotely to perform automated tasks |

### Hacking vs Ethical Hacking vs Penetration Testing
| | Hacking | Ethical Hacking | Penetration Testing |
|--|---------|----------------|-------------------|
| **Intent** | Steal/damage | Find & fix weaknesses | Test specific defenses |
| **Permission** | No consent | Full consent | Legal contract |
| **Legality** | Illegal | Legal | Legal |
| **Scope** | Unlimited | Broad | Narrow & defined |

---

## ⚙️ Lab Setup — Step by Step

### Step 1 — Configure VMNet1 (Isolated Network)
```
VMware → Edit → Virtual Network Editor
→ Select VMnet1
→ Set to: Host-only
→ Subnet IP: 150.1.7.0
→ Subnet Mask: 255.255.255.0
→ Disable DHCP (we use static IPs)
→ Click Apply
```

### Step 2 — Configure Parrot OS (Attacker) Static IP
```bash
# Edit network interfaces file
sudo nano /etc/network/interfaces

# Add these lines for ens34:
auto ens34
iface ens34 inet static
address 150.1.7.101
netmask 255.255.255.0

# Save and restart networking
sudo systemctl restart networking

# Verify with:
ifconfig
```

### Step 3 — Configure Host Machine (Windows)
```
Control Panel → Network Adapters
→ VMware Network Adapter VMnet1
→ Properties → IPv4
→ IP Address: 150.1.7.100
→ Subnet Mask: 255.255.255.0
→ Click OK
```

### Step 4 — Allow ICMP Through Windows Firewall
```
Windows Defender Firewall → Advanced Security
→ Inbound Rules → New Rule
→ Custom → Protocol: ICMPv4
→ Action: Allow the connection
→ Apply
```

### Step 5 — Verify Connectivity
```bash
# From Windows host → ping Parrot OS
ping 150.1.7.101

# From Parrot OS → ping Windows host
ping 150.1.7.100

# Expected result: 0% packet loss
```

---

## ✅ Results

```
HOST → PARROT OS:
Packets: Sent=4, Received=4, Lost=0 (0% loss)
Round trip: Minimum=0ms, Maximum=0ms, Average=0ms ✓

PARROT OS → HOST:
64 bytes from 150.1.7.100: icmp_seq=1 ttl=128 time=0.358ms ✓

STATUS: Lab fully operational and ready for penetration testing
```

---

## 🐍 Automation Script

A Python script is included to automatically verify your lab configuration.

```bash
# Run the lab verifier
sudo python3 lab_verifier.py
```

See [`lab_verifier.py`](./lab_verifier.py) for full source code.

---

## 💡 What I Learned

- How to build a completely isolated network for safe security testing
- The importance of static IP addressing in lab environments
- Why host-only networking prevents accidental exposure to real networks
- The foundational CEH methodology that guides all ethical hacking work
- How the sophistication of hacking tools has increased while technical knowledge required has decreased — meaning defenders need to be smarter than ever

---

## 🔗 Connect

**Muhammad Owais Raza**
- GitHub: [Mianowaisraza](https://github.com/Mianowaisraza)
- LinkedIn: [muhammad-owais-raza](https://www.linkedin.com/in/muhammad-owais-raza-8693753a7)

---

*Part of my CEH learning journey — documented weekly on LinkedIn and GitHub*
