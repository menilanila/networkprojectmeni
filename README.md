 Enterprise Network Automation Platform

Status: ✅ READY FOR INTERVIEWS (V2)

 🌟 Project Purpose & Architecture
This project demonstrates a Production-Grade Infrastructure-as-Code (IaC) Network Platform. Instead of manually configuring devices or running standalone scripts, this system uses a modular, scalable architecture to manage an entire simulated data center topology. 

It explicitly demonstrates skills required for a Technical Solutions Engineer (TSE) at companies like Arista Networks by showing deep understanding of TCP/IP, SSH transports, error isolation, declarative JSON intent, and Python ecosystem engineering.

---

 🏗️ Topology & Infrastructure
The lab is entirely built using Docker to instantly simulate a 5-node network without needing $50k+ in physical hardware:
- `router1` & `router2`: Core routing nodes running Free Range Routing (FRR) on Ubuntu.
- `switch1`: A simulated transit switch bridging communication.
- `server1`: An Nginx application server acting as the data-plane destination.
- `client1`: An Alpine Linux node acting as the test origination point.

---

 🛠️ Technology Stack
- Python 3.10: The core automation engine executing the TSE-level logic.
- Docker Exec Subprocess Wrapper: Inherently handles SSH-like transport with timeout protections, automatic retries, and exponential backoff.
- FRR (Free Range Routing): Provides real BGP/OSPF/Static routing control planes inside the containers.
- JSON Intent Inventory: `devices.json` acts as the source-of-truth schema.

---

 🧠 Networking Concepts Demonstrated
1. Control Plane vs. Data Plane: The script manages the Control Plane (injecting IPs and routes) to facilitate Data Plane reachability (ICMP pings).
2. Idempotency: Running deployments multiple times yields the exact same state without crashing.
3. Robust Transport Protocols: Handling edge-cases where management interfaces (SSH/Docker Exec) timeout or reject connections. 
4. Configuration Drift: Using the `audit` module to compare the live running-config against the JSON intent to detect unauthorized changes.

---

 ⚙️ Platform Modules (CLI)

The platform is operated entirely via a professional CLI (`python main.py <command>`):

 `deploy`: Pushes IP addresses and static routes to the topology based on `devices.json`. Contains partial-failure protections if a node goes offline mid-deployment.
 `monitor`: Polls devices sequentially to check daemon uptime and OS responsiveness.
 `test-connectivity`: Initiates an ICMP sweep map across the topology to prove data-plane routing.
 `audit`: "Diffs" the actual assigned IP spaces against the expected JSON schema.
 `troubleshoot`: Performs deep diagnostic checks (daemon alive? interface administratively down? routes missing?) and outputs pinpoint root causes.

---

 🚀 Getting Started & Demos

(See `DEMO_SCENARIOS.md` for complete interview workflows.)

The 60-Second Quickstart:
1. Boot the data center:
   ```bash
   cd "e:\networking project\python_networking"
   docker-compose up -d
   ```
2. Provision the network:
   ```bash
   cd network-automation
   python main.py deploy
   ```
3. Audit the configuration drift:
   ```bash
   python main.py audit
   ```

---

 💼 Why This Impresses Interviewers
A standard candidate writes a script that logs into one mock router and prints the hostname. 

This platform proves:
 System Design: You've separated data (`inventory/devices.json`), transport (`utils/docker_client.py`), and business logic (`modules/deploy.py`).
 Resilience: The code anticipates real-world breaks. If `router1`'s hardware fails, the script elegantly logs it and proceeds to configure `router2`.
 Visibility: Every action generates a timestamped artifact in `logs/` just like an enterprise CI/CD pipeline.
