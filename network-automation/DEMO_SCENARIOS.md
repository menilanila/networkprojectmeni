 Network Automation Platform - Demos

These demo scenarios are designed for a live technical interviewing session (TSE, DevOps, SRE roles).

 🚀 Scenario 1: Normal Enterprise Deployment (Full Success)
Goal: Show that the system can read desired state (intent) from JSON and push it successfully to entirely distinct simulated network functions (routers, switches, servers).

1. Start fresh topology:
   ```bash
   cd "e:\networking project\python_networking"
   docker-compose up -d
   ```
2. Execute the deployment module:
   ```bash
   cd network-automation
   python main.py deploy
   ```
Talking Points: Mention the Idempotency (if you run it twice, it safely passes) and the declarative IaC approach (JSON -> Python -> Network).

 💥 Scenario 2: One Device Failure (Partial Success & Resilience)
Goal: Prove the platform doesn't crash when elements of the network go down, mimicking real-world outages.

1. Stop a core node:
   ```bash
   docker stop router1
   ```
2. Re-run deployment:
   ```bash
   python main.py deploy
   ```
Expected Outcome: System successfully configures `router2`, `switch1`, `server1`, while properly flagging `router1` as offline and logging the exception without breaking the workflow. 

 🩺 Scenario 3: Monitoring & Troubleshooting
Goal: Prove TSE-Level diagnostic insights.

1. Check up/down status:
   ```bash
   python main.py monitor
   ```
   Outcome: Accurately shows `router1` as DOWN.
   
2. Deep-dive into root cause:
   ```bash
   python main.py troubleshoot
   ```
   Outcome: Script isolates the failure plane (e.g. data-plane link vs control-plane host daemon).

 🔍 Scenario 4: Audit / Compliance Draft
Goal: Validate ongoing configuration drift.
1. Run audit module:
   ```bash
   python main.py audit
   ```
Expected Outcome: Compares physical container IP state to `devices.json` expected IPs and returns cleanly. 
