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
            # Check live physical/virtual data state vs intent payload
            ok, out = client.execute(name, f"ip -o -4 addr show {intf} | awk '{{print $4}}'")
            if not ok:
                logger.error(f"[{name}] Audit execution failed: missing daemon or broken command.")
                continue
                
            actual_ip = out.strip()
            if actual_ip == expected_ip:
                logger.info(f"[{name}] MATCH: {intf} correctly configured with {expected_ip}")
            else:
                logger.warning(f"[{name}] DRIFT DETECTED: {intf} expected {expected_ip}, found '{actual_ip}'")
                
    logger.info("=== AUDIT FINISHED ===\n")
