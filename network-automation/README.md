 REAL DOCKER NETWORK AUTOMATION LAB

This is a REAL project that automates actual Docker containers.

 What You Have

✅ Docker containers running real router OS (FRR - Free Range Routing)  
✅ SSH access to each container  
✅ Python automation script that makes REAL configuration changes  
✅ Live, verifiable proof that your code works  

---

 QUICK START (10 minutes)

 Step 1: Start Docker Containers

```bash
cd .\python_networking
docker-compose up -d
```

Wait 30 seconds for containers to boot and SSH to start.

Verify:
```bash
docker ps
```

You should see:
```
router1    (port 2201)
router2    (port 2202)
```

---

 Step 2: Test SSH Connection (Manual)

Test that you can connect to a router:

```bash
ssh -p 2201 root@localhost
 Password: root
 Type: exit
```

---

 Step 3: Install Python Dependencies

```bash
.\venv\Scripts\Activate
pip install paramiko
```

---

 Step 4: Run the Deployment

```bash
cd network-automation
python deploy.py
```

WHAT YOU'LL SEE:

```
╔════════════════════════════════════════════════════════╗
║        NETWORK AUTOMATION DEPLOYMENT SYSTEM             ║
║       Real Docker Container Configuration               ║
╚════════════════════════════════════════════════════════╝

PHASE 1: CONNECTING TO DEVICES
============================================================
[router1] Connecting to localhost:2201...
[router1] ✓ Connected successfully
[router2] Connecting to localhost:2202...
[router2] ✓ Connected successfully

PHASE 2: PRE-DEPLOYMENT CHECKS
============================================================
[router1] Current Configuration:
(shows current interfaces)

PHASE 3: DEPLOYING CONFIGURATIONS
============================================================
[router1] Deploying configuration...
[router1] Configuring eth0 with 172.20.0.2/24
[router1] ✓ Interface configured

PHASE 4: POST-DEPLOYMENT VERIFICATION
============================================================
[router1] Verification Results:
inet 172.20.0.2/24 scope global eth0
(shows new configuration)

DEPLOYMENT REPORT
============================================================
✓ Deployment completed successfully!
```

---

 WHAT JUST HAPPENED?

1. ✅ Connected to real Docker containers via SSH
2. ✅ Retrieved current device configuration
3. ✅ Applied real network configuration changes
4. ✅ Verified the changes took effect

---

 PROOF THIS IS REAL

Manually verify the change:

```bash
docker exec -it router1 ip addr show eth0
```

You should see:
```
inet 172.20.0.2/24 scope global eth0
```

This matches what your Python script configured!

---

 FOR YOUR INTERVIEW (Live Demo Script)

 Demo Sequence (5 minutes):

Step 1: Show Containers Running
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Step 2: Show Current Config (Before)
```bash
docker exec -it router1 vtysh -c "show running-config" | head -20
```

Step 3: Run Python Deployment
```bash
python deploy.py
```
> "Notice the script connects, checks current state, deploys real config changes, and verifies them."

Step 4: Show New Config (After)
```bash
docker exec -it router1 vtysh -c "show running-config" | head -20
```

---

 PROJECT STRUCTURE

```
network-automation/
├── deploy.py                 Main deployment script
├── devices.json             Device inventory
├── utils/
│   └── ssh_client.py        Reusable SSH connection class
├── templates/               Jinja2 templates (for future)
├── logs/                    Deployment logs
└── README.md               This file
```

---

 KEY FILES EXPLAINED

 `deploy.py`
- What it does: Connects to real Docker containers, deploys configs, verifies changes
- Phases:
  1. Load inventory from devices.json
  2. SSH to each device
  3. Check current state
  4. Apply new configuration
  5. Verify changes took effect
  6. Generate report with timestamps

 `utils/ssh_client.py`
- What it does: Reusable library for SSH connections
- Key capabilities:
  - Connect securely to devices
  - Execute commands
  - Configure interfaces with IP addresses
  - Show running configs, interfaces, routes
  - Works with ANY SSH-enabled device (real switches, Docker, etc.)

 `devices.json`
- Device inventory
- Connection details (hostname, port, credentials)
- What to configure (interfaces, IPs)

---

 REAL INTERVIEW TALKING POINTS

What makes this impressive:

1. It's REAL - Not simulated, not mocked. Real SSH connections to real containers.
2. It's PRODUCTION-READY - Uses paramiko (industry standard), proper error handling, logging
3. It's SCALABLE - One script configures 2 devices. Same script configures 100 devices.
4. It DEMONSTRATES - You understand:
   - Network automation (SSH, CLI commands)
   - Python best practices (logging, error handling, context managers)
   - Real deployment workflows (pre-checks, deploy, verify)
   - Infrastructure-as-Code (configs from data, not manual)

---

 TROUBLESHOOTING

 "Connection refused"
Problem: Containers not ready  
Solution: Wait 30 seconds, then try again. SSH daemon takes time to start.

```bash
docker-compose up -d
 Wait 30 seconds
python deploy.py
```

 "Authentication failed"
Problem: Container SSH not initialized  
Solution: Containers might not be fully booted. Wait, then restart:

```bash
docker-compose restart
 Wait 30 seconds
python deploy.py
```

 "paramiko not installed"
Solution: 
```bash
.\venv\Scripts\Activate
pip install paramiko
```

---

 WHAT YOU CAN DO NEXT

 Immediate:
- ✅ Run the demo (5 min total)
- ✅ Modify devices.json to add more interfaces
- ✅ Test with 10 devices (same code, just modify JSON)

 Short-term:
- Add BGP routing setup
- Add VLAN configuration
- Add firewall rules
- Add monitoring/health checks

 Interview preparation:
- Know this script inside-out
- Be ready to explain each phase
- Be ready to modify it on the fly if asked
- Have talking points about scalability

---

 REAL VS. MOCK

Old approach (mock):
```python
def get_device_info():
    return MockArista().info()   Simulated, no real device
```

This approach (real):
```python
ssh_client = SSHClient("localhost", 2201, "root", "root")
output = ssh_client.show_interfaces()   Real SSH output
```

Interview value:
- Interviewer can see: "This is real SSH, real commands, real containers"
- Not: "This is a mock simulator"

---

 READY?

```bash
docker-compose up -d
python deploy.py
```

Your real network automation is running. 🚀
