import json
from utils.logger import setup_logger
from utils.docker_client import DockerClient

logger = setup_logger("test_connectivity")
client = DockerClient(logger)

def run_tests(inventory_file):
    logger.info("=== CONNECTIVITY SWEEP ===")
    with open(inventory_file) as f:
        inventory = json.load(f).get('devices', [])
        
    # Aggregate all expected IPs across topology
    target_ips = [d['ip'] for d in inventory if d.get('ip')]
    
    for device in inventory:
        name = device['name']
        logger.info(f"[{name}] Initiating ping sweeps...")
        
        for target in target_ips:
            if target == device['ip']:
                continue
                
            # TCP/IP verification via single ICMP echo request, 1-sec timeout
            ok, out = client.execute(name, f"ping -c 1 -W 1 {target}")
            if ok:
                logger.info(f"[{name}] -> {target} : SUCCESS Reachable")
            else:
                logger.error(f"[{name}] -> {target} : FAILED Unreachable")
                
    logger.info("=== CONNECTIVITY SWEEP FINISHED ===\n")
