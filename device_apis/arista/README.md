 Arista eAPI Network Automation - Complete Guide

 Overview

This folder demonstrates how to automate Arista EOS (Extensible Operating System) devices using eAPI - Arista's JSON-RPC over HTTP/HTTPS API.

 What You'll Learn

- ✅ How Arista switches are configured programmatically
- ✅ Network fundamentals (Layers 1-3 of the OSI model)
- ✅ eAPI connectivity patterns (compared to CLI)
- ✅ Bulk configuration generation for enterprise deployments
- ✅ Best practices for network automation

---

 Files in This Package

 1. arista_eapi_basics.py - START HERE
What it teaches: Network fundamentals + Arista device connectivity

Covers:
- OSI Layer 1: Physical interfaces (Ethernet1, Ethernet2, etc.)
- OSI Layer 2: VLANs (network segmentation)
- OSI Layer 3: IP addressing and routing
- Device management via out-of-band interface

Topics:
- Interface status (up/down, line protocol)
- VLAN configuration and purpose
- IP addressing and subnetting
- Device identification (model, serial number, version)

Run it:
```bash
python arista_eapi_basics.py
```

Output: Shows device info, interface status, VLAN config, IP interfaces

---

 2. arista_eapi_config.py - Configuration Management
What it teaches: How to configure Arista devices programmatically

Covers:
- Interface configuration (description, speed, MTU, shutdown)
- VLAN creation and management
- Interface VLAN membership (access vs trunk modes)
- IP address configuration

Key Functions:
- `configure_interface()` - Set port speed, MTU, description
- `configure_vlan()` - Create and name VLANs
- `set_interface_vlan()` - Assign ports to VLANs
- `configure_ip_address()` - Layer 3 addressing

Run it:
```bash
python arista_eapi_config.py
```

Output: Shows configuration commands in dry-run mode (preview only)

---

 3. arista_bulk_deploy.py - Infrastructure as Code
What it teaches: Scalable configuration for 1000s of devices

Covers:
- Jinja2 templating for device configurations
- Bulk generation from data + template
- Configuration consistency across many devices
- Deployment reporting and comparison

Key Concepts:
- One template + many device data = many unique configs
- Similar to Infrastructure as Code (IaC) principles
- Enables version control of network configurations

Run it:
```bash
python arista_bulk_deploy.py
```

Output: Generates individual config files for each device

---

 Network Fundamentals & Networking Concepts

 OSI Model & What Each Layer Does

| Layer | Name | What Happens | Examples |
|-------|------|--------------|----------|
| 1 | Physical | Electrical signals on cables | Ethernet cables, fiber optics |
| 2 | Data Link | Moving data between directly connected devices | VLANs, MAC addresses, switching |
| 3 | Network | Moving data across different networks | IP addresses, routing |
| 4 | Transport | End-to-end connections | TCP, UDP |
| 7 | Application | User-facing services | HTTP, SSH, APIs |

 This Project Focuses on Layers 1-3

 Layer 1 - Physical Connectivity
```
Ethernet1 [Physical Port] --- Cable --- Other Device
```
- Interface Status: Is the cable plugged in? (Physical layer)
- Line Protocol: Can we exchange data? (Data link layer)
- Link Speed: 1G, 10G, 25G, 40G, 100G, 400G

 Layer 2 - VLAN (Virtual LAN)
```
Device A (VLAN 10) --- Logical Network --- Device B (VLAN 10)
Device C (VLAN 20) --- Separate Network --- Device D (VLAN 20)
```
- Purpose: Segment network into broadcast domains
- Benefit: Security, performance, logical separation
- Types:
  - Access VLAN: Single VLAN per port (end devices)
  - Trunk VLAN: Multiple VLANs on one port (switch-to-switch)

 Layer 3 - IP Routing
```
Network A (10.1.0.0/24) --- Router --- Network B (10.2.0.0/24)
```
- IP Address: Unique network identifier (e.g., 10.1.1.100)
- Subnet Mask: How big is the network? (/24 = 256 addresses)
- Routing: How to send packets between networks

 Why This Matters for Arista TSE

Arista Technical Solution Engineers must understand:

1. Device Hardware - What ports/speeds are available
2. Layer 2 Design - VLAN strategy, spanning tree
3. Layer 3 Design - IP addressing, routing protocols
4. Automation - How to programmatically deploy at scale
5. Business Value - Save time, reduce errors, enable scale

---

 Arista eAPI vs Traditional CLI

 Traditional (Manual SSH)
```bash
ssh admin@10.1.1.100
configure
interface Ethernet1
  description Data Center Uplink
  speed 40G
  no shutdown
exit
exit
```
- Pros: Everyone knows CLI
- Cons: Slow, error-prone, hard to automate

 Modern (eAPI - REST/JSON)
```python
from jsonrpc import JsonRpcClient

device = JsonRpcClient(host="10.1.1.100")
device.runCmds(1, [
    "configure",
    "interface Ethernet1",
    "description Data Center Uplink",
    "speed 40G",
    "no shutdown",
    "end"
])
```
- Pros: Programmable, scalable, returns structured JSON
- Cons: Requires understanding APIs and JSON

 Why eAPI Wins
- Single request for multiple commands
- Structured response (JSON) vs raw text parsing
- No SSH session overhead - lightweight HTTP
- Easy to parse - standard JSON libraries
- Enables bulk operations - deploy 1000s of devices in parallel

---

 Arista Networking Architecture

 Typical Data Center Design

```
                    [Spine Switches]
                   /      |      \
              40G /   40G |   40G \
                 /         |         \
         [Leaf-01]--[Leaf-02]--[Leaf-03]
           /    \    /    \    /    \
        25G     25G 25G  25G 25G   25G
        /         \  /     \  /       \
    [Server]  [Server]  [Server] [Storage]
```

 Device Roles

| Device | Purpose | Connectivity |
|--------|---------|--------------|
| Spine | Core switching fabric | 40G/100G uplinks, ports to all leaves |
| Leaf | Access layer for servers | 10G/25G server connections, 40G to spine |
| Server | Application hosts | 10G/25G to leaf switch |
| Storage | Data storage systems | 25G/40G to leaf switch |

 Why This Matters
- Each device needs unique configuration
- Manual configuration = 100s of hours
- Automation = minutes
- Consistency = fewer network issues

---

 Key Networking Concepts You'll See

 1. Interface Naming
- `Ethernet1` through `Ethernet48` - 1G/10G/25G ports (typical leaf)
- `Ethernet49` through `Ethernet52` - 40G/100G ports (typical uplinks)
- `Management1` - Out-of-band management port
- `Loopback0` - Virtual interface for routing protocols

 2. Interface Modes
- Access: One VLAN, used for servers/end devices
- Trunk: Multiple VLANs, used for switch-to-switch links
- Routed: Layer 3 IP interface (typical for spine)

 3. Port Speed Configuration
- `speed 1G` - 1 Gigabit
- `speed 10G` - 10 Gigabit
- `speed 25G` - 25 Gigabit
- `speed 40G` - 40 Gigabit
- `speed 100G` - 100 Gigabit

 4. MTU (Maximum Transmission Unit)
- Default: 1500 bytes (standard Ethernet)
- Jumbo frames: 9000 bytes (for high-speed data centers)
- Important for performance tuning

 5. Spanning Tree Protocol
- Prevents Layer 2 loops
- Arista uses "rapid" spanning tree (RSTP)
- Faster convergence than legacy STP

---

 Real-World The Scenarios

 Scenario 1: New Data Center Deployment
- Deploy 50 leaf switches + 2 spine switches
- Each needs: hostname, management IP, interface config, VLAN setup
- Without automation: 100+ hours of manual work
- With automation: 5 minutes of script execution + 5 minutes of validation

 Scenario 2: Configuration Update
- Change spanning tree priority on 50 devices
- Without automation: SSH to each device, 10 minutes each = 500 minutes
- With automation: 1 script executes to all devices in parallel = 5 minutes

 Scenario 3: Disaster Recovery
- Hardware failure on core switch
- Need to rebuild 100 device configurations
- Without automation: Manual entry of 100 configs = 50+ hours
- With automation: Regenerate from templates = 1 minute

---

 Interview Questions You Might Get

 Q: "How do you scale network automation?"
Answer from this project:
"I understand three scaling techniques:
1. Templating - One template, many devices = consistent configs
2. Parallel execution - Configure many devices simultaneously
3. API integration - Bulk commands vs serial SSH connections

This project shows all three - using Jinja2 templates to generate configs for multiple devices, which can then be applied in parallel via eAPI."

 Q: "What's the difference between Arista and Cisco automation?"
Answer from this project:
"Both use REST APIs at the core. Cisco uses RESTCONF/NETCONF, Arista uses eAPI. The principles are identical: structured JSON requests, programmatic device control, bulk deployment capability. The syntax changes but the concepts remain the same."

 Q: "How would you integrate this into a CI/CD pipeline?"
Answer from this project:
"The configuration generation produces text files that can be:
1. Committed to Git (version control)
2. Reviewed via pull requests (change approval)
3. Tested on staging devices (validation)
4. Applied to production via Ansible (orchestration)

This puts network configurations under the same rigorous control as application code."

 Q: "What are the prerequisites for network automation?"
Answer from this project:
"You need to understand:
1. OSI Model - Layers 1-3 fundamentals
2. Networking Terminology - VLANs, subnets, routing
3. Device Configuration - CLI syntax and options
4. APIs - How to send structured requests
5. Programming - Python for scripting
6. Best Practices - Error handling, dry-runs, rollback

This project covers all of these."

---

 How to Impress in Your Interview

 1. Run the Examples
```bash
python arista_eapi_basics.py            Shows networking fundamentals
python arista_eapi_config.py            Shows device configuration
python arista_bulk_deploy.py            Shows infrastructure as code
```

 2. Explain What You See
> "This shows eAPI connectivity to Arista devices. The first example demonstrates understanding of network layers - interfaces, VLANs, IP addressing. The second shows programmatic configuration. The third shows how to scale to enterprise deployments."

 3. Draw the Architecture
```
Draw a simple diagram showing:
- Spine <-> Leaf <-> Server topology
- Label ports (Ethernet1, Ethernet49, etc.)
- Explain VLAN segmentation
- Show how automation reduces manual effort
```

 4. Ask Insightful Questions
> "How do you currently manage 1000+ devices? How much time is spent on repetitive configurations? What's your change management process? How do you ensure consistency?"

---

 next Steps to Deepen Your Learning

1. Study eAPI Documentation
   - https://aristanetworks.github.io/EosSdk/docs/
   - Understand available commands and RPC methods

2. Learn CloudVision Platform
   - Arista's centralized device management platform
   - Where all these automated configs would be deployed from

3. Practice with Real Arista Devices
   - Use Arista test labs or DevNet sandboxes
   - Replace MockArista with real JsonRpcClient

4. Integrate with Orchestration
   - Ansible playbooks for broader automation
   - Terraform for infrastructure as code

5. Study Professional Use Cases
   - Data center automation case studies
   - Enterprise network deployments

---

 Common Terms You'll Encounter

| Term | Meaning | Example |
|------|---------|---------|
| eAPI | Arista's API (JSON-RPC over HTTP) | Device communication |
| EOS | Extensible Operating System (Arista's OS) | What runs on Arista switches |
| Leaf | Access layer switch | Where servers connect |
| Spine | Core switching fabric | Between leaves and WAN |
| SVI | Switched Virtual Interface (Layer 3 on VLAN) | Interface vlan 10 |
| Trunk | Link carrying multiple VLANs | Inter-switch link |
| Access | Link with single VLAN | Server connection |
| RSTP | Rapid Spanning Tree Protocol | Prevents loops |
| BGP | Border Gateway Protocol (routing) | Inter-AS routing |
| OSPF | Open Shortest Path First (routing) | Intra-AS routing |

---

 Conclusion

This project demonstrates:
1. ✅ You understand networking fundamentals (Layers 1-3)
2. ✅ You can work with network APIs (eAPI)
3. ✅ You can scale configurations (Jinja2 + Bulk)
4. ✅ You understand automation principles (Infrastructure as Code)
5. ✅ You're ready to contribute to network engineering teams

For Arista Technical Solution Engineer interviews:
- Show these examples
- Explain the networking concepts
- Demonstrate API understanding
- Ask questions about their infrastructure
- Show enthusiasm for solving problems at scale

Good luck! 🚀

