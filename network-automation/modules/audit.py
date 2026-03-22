import json
from utils.logger import setup_logger
from utils.docker_client import DockerClient

logger = setup_logger("audit")
client = DockerClient(logger)

def run_audit(inventory_file):
    logger.info("=== CONFIGURATION DRIFT AUDIT ===")
    with open(inventory_file) as f:
        inventory = json.load(f).get('devices', [])
        
    for device in inventory:
        name = device['name']
        config = device.get('config', {})
        interfaces = config.get('interfaces', {})
        
        if not interfaces:
            logger.info(f"[{name}] No expected interface configurations assigned.")
            continue
            
        for intf, expected_ip in interfaces.items():
            # Check live physical/virtual data state vs intent payload using pure python to avoid OS shell escaping conflicts
            ok, out = client.execute(name, f"ip -o -4 addr show {intf}")
            if not ok:
                print(f"[{name}] Audit execution failed: missing daemon or broken command. Error: {out.strip()}")
                continue
                
            # Extract the IP address carefully
            actual_ip = ""
            for line in out.splitlines():
                if intf in line and "inet " in line:
                    parts = line.split()
                    try:
                        idx = parts.index("inet")
                        actual_ip = parts[idx + 1]
                    except ValueError:
                        pass
                        
            if actual_ip == expected_ip:
                print(f"[{name}] MATCH: {intf} correctly configured with {expected_ip}")
            else:
                print(f"[{name}] DRIFT DETECTED: {intf} expected {expected_ip}, found '{actual_ip}'")
                
    logger.info("=== AUDIT FINISHED ===\n")
