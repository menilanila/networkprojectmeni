#!/usr/bin/env python3
"""
REAL Docker Network Automation - Simplified
Uses only basic Linux tools available in any container
"""

import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f'deployment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

import sys

# Windows UTF-8 console output fix
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DockerNetworkAutomation:
    """Deploy and verify configurations in Docker containers"""

    def __init__(self, devices_file: str):
        self.devices_file = Path(devices_file)
        self.devices = []
        self.results = []

    def load_devices(self):
        """Load device inventory"""
        with open(self.devices_file) as f:
            self.devices = json.load(f).get('devices', [])
        
        print(f"\n[INVENTORY] Loaded {len(self.devices)} devices")
        for d in self.devices:
            print(f"  - {d['name']} @ {d['hostname']}:{d['port']}")

    def exec_cmd(self, container: str, cmd: str) -> tuple[bool, str]:
        """Execute command in container"""
        try:
            result = subprocess.run(
                f'docker exec {container} sh -c "{cmd}"',
                shell=True, capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    def deploy_to_device(self, device):
        name = device['name']
        print(f"[{name}] Applying configurations:")
        
        # Show current state
        ok, hostname = self.exec_cmd(name, "hostname")
        if not ok:
            print(f"[{name}] STATUS: FAILED")
            print(f"  Reason: Device is DOWN or unreachable")
            print(f"  Action: Skipping deployment\n")
            
            self.results.append({
                'device': name,
                'status': 'FAILED',
                'reason': 'Device offline'
            })
            return
            
        print(f"  Current hostname: {hostname.strip()}")
        
        # Create a simple configuration by writing to a file
        # Using printf to avoid quoting issues
        config_cmd = f"printf 'Device: {name}\\nConfig deployed at: ' > /etc/config-{name}.txt && date >> /etc/config-{name}.txt"
        
        ok, out = self.exec_cmd(name, config_cmd)
        if not ok:
            raise Exception(f"Command execution failed - {out[:100].strip()}")
            
        print(f"[{name}] STATUS: SUCCESS")
        print(f"  Configuration deployed successfully")
        self.results.append({'device': name, 'status': 'SUCCESS'})
        
        # Verify
        ok, config = self.exec_cmd(name, f"cat /etc/config-{name}.txt")
        if ok:
            print(f"  VERIFIED: Configuration created")
            print(f"    {config.strip()}")

    def deploy(self):
        """Deploy configurations"""
        print("\n[DEPLOYMENT] Starting configuration deployment...\n")
        
        for device in self.devices:
            name = device['name']
            try:
                self.deploy_to_device(device)
                print()
            except Exception as e:
                print(f"  STATUS: Failed - {e}\n")
                self.results.append({'device': name, 'status': 'FAILED'})
                continue

    def report(self):
        """Show deployment report"""
        print("\n" + "="*60)
        print("DEPLOYMENT REPORT")
        print("="*60)
        
        for r in self.results:
            if r['status'] == 'SUCCESS':
                print(f"{r['device']} → SUCCESS")
            else:
                print(f"{r['device']} → FAILED ({r.get('reason', 'Unknown')})")

        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'SUCCESS')

        print(f"\nTotal devices: {total}")
        print(f"Successful: {success}")
        print(f"Failed: {total - success}")
        print(f"\nLog saved: {log_file}")

    def run(self):
        """Execute deployment workflow"""
        try:
            print("\n" + "="*60)
            print("REAL DOCKER NETWORK AUTOMATION")
            print("="*60)
            
            self.load_devices()
            self.deploy()
            self.report()
            return True
        except Exception as e:
            print(f"ERROR: {e}")
            return False


if __name__ == '__main__':
    deployer = DockerNetworkAutomation('devices.json')
    deployer.run()
