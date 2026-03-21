import json
from utils.logger import setup_logger
from utils.docker_client import DockerClient

logger = setup_logger("troubleshoot")
client = DockerClient(logger)

def analyze(inventory_file):
    logger.info("=== DEEP DIAGNOSTIC ANALYSIS ===")
    with open(inventory_file) as f:
        inventory = json.load(f).get('devices', [])
        
    for device in inventory:
        name = device['name']
        
        # Check basic transport daemon
        ok, out = client.execute(name, "echo 'hello'")
        if not ok:
            logger.error(f"[{name}] ROOT CAUSE: Node offline or management plane (Docker) is unreachable.")
            continue
            
        # Check data plane interfaces
        ok, out = client.execute(name, "ip link show eth0")
        if ok and "state DOWN" in out:
            logger.warning(f"[{name}] WARNING: Expected interface eth0 is Administratively DOWN.")
            
        # Check control plane routes
        ok, out = client.execute(name, "ip route")
        if ok and "default" not in out and "172.20" not in out:
            logger.warning(f"[{name}] WARNING: Critical routing table entries missing.")
            
        logger.info(f"[{name}] Check complete. No critical faults identified.")
        
    logger.info("=== DIAGNOSTIC FINISHED ===\n")
