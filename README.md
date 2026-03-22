 Enterprise Network Automation Platform



 🌟 Project Purpose & Architecture
This is my personal project demonstrating a Production-Grade Infrastructure-as-Code (IaC) Network Platform. I built this to learn and showcase my networking skills, exploring how to automate network device configuration, auditing, troubleshooting, and monitoring. Instead of manually configuring devices or running standalone scripts, this system uses a modular, scalable architecture to manage an entire simulated data center topology.

It demonstrates skills required for a Technical Solutions Engineer (TSE) at companies like Arista Networks by showing deep understanding of TCP/IP, SSH transports, error isolation, declarative JSON intent, and Python ecosystem engineering.

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
 System Design: I've separated data (`inventory/devices.json`), transport (`utils/docker_client.py`), and business logic (`modules/deploy.py`).
 Resilience: The code anticipates real-world breaks. If `router1`'s hardware fails, the script elegantly logs it and proceeds to configure `router2`.
 Visibility: Every action generates a timestamped artifact in `logs/` just like an enterprise CI/CD pipeline.

---

 📥 Cloning and Running the Project

To explore and run this project on your own machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/networking-automation-project.git
   cd networking-automation-project/python_networking
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Docker topology:
   ```bash
   docker-compose up -d
   ```

4. Run the automation commands:
   ```bash
   cd network-automation
   python main.py deploy
   python main.py monitor
   python main.py test-connectivity
   python main.py audit
   python main.py troubleshoot
   ```

5. View logs:
   ```bash
   ls logs/
   cat logs/deploy_*.log
   ```

---

 🧠 Concepts Learned from This Project

Through building this project, I learned and demonstrated:

1. **Infrastructure as Code (IaC)**: Declarative configuration using JSON instead of imperative scripting
2. **Modular Architecture**: Separating concerns into utils, modules, and CLI layers
3. **Error Handling & Resilience**: Retry logic, timeouts, and graceful failure handling
4. **Network Automation**: Control plane management, data plane verification, and drift detection
5. **Docker Containerization**: Simulating real network topologies without physical hardware
6. **SSH and Transport Protocols**: Secure remote execution with paramiko and docker exec
7. **Logging & Auditing**: Enterprise-grade logging for compliance and troubleshooting
8. **Python Ecosystem**: Libraries like paramiko, subprocess, json, and logging
9. **Network Protocols**: TCP/IP, ICMP, static routing, and interface configuration
10. **DevOps Practices**: Version control, modular code, and CI/CD-ready structure

---

 🌐 Real-World Applications and Scalability

This project showcases skills applicable to large-scale network operations:

**Enterprise Use Cases:**
- **Data Center Provisioning**: Automate configuration of hundreds of switches and routers
- **Network Monitoring**: Continuous health checks and alerting for network infrastructure
- **Compliance Auditing**: Regular verification that configurations match security policies
- **Troubleshooting Automation**: Rapid root cause analysis for network issues
- **Zero-Touch Provisioning**: Deploy new network devices without manual intervention

**Scalability Features:**
- **Parallel Execution**: Can be extended to deploy to thousands of devices simultaneously
- **Multi-Cloud Support**: Adaptable to AWS, Azure, GCP network automation
- **Integration Ready**: Can connect to ServiceNow, Splunk, or other enterprise tools
- **Production Hardening**: Add authentication, encryption, and role-based access

**Real-Time Problem Solving:**
- **Emergency Response**: Quickly audit and fix configuration issues during outages
- **Capacity Planning**: Monitor network utilization and predict scaling needs
- **Security Incidents**: Automated response to detect and isolate compromised devices
- **Change Management**: Track all network changes with full audit trails

This project demonstrates how to build production-ready network automation tools that scale from small labs to enterprise data centers.
