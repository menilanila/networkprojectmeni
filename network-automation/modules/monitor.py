import json
from utils.logger import setup_logger
from utils.docker_client import DockerClient

logger = setup_logger("monitor")
client = DockerClient(logger)

def check_status(inventory_file):
    logger.info("=== MONITORING STATUS ===")
    with open(inventory_file) as f:
        inventory = json.load(f).get('devices', [])
        
    for device in inventory:
        name = device['name']
        
        # Check node availability and uptime
        ok, out = client.execute(name, "uptime -p")
        if ok:
            logger.info(f"[{name}] STATUS: UP | Uptime: {out}")
        else:
            logger.error(f"[{name}] STATUS: DOWN | Reason: {out}")
            
    logger.info("=== MONITORING FINISHED ===\n")
