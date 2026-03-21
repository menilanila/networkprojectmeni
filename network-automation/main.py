import argparse
import sys
from pathlib import Path

# Ensure local imports work reliably
sys.path.append(str(Path(__file__).parent))

from modules.deploy import deploy_configurations
from modules.test_connectivity import run_tests
from modules.monitor import check_status
from modules.troubleshoot import analyze
from modules.audit import run_audit

INVENTORY = "inventory/devices.json"

def main():
    parser = argparse.ArgumentParser(
        description="Enterprise Network Automation Platform (TSE Demo)",
        epilog="Use 'python main.py <command> -h' for more info."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Network Operations")
    subparsers.required = True

    subparsers.add_parser("deploy", help="Deploy configurations (IPs, Routes) to infrastructure using IaC patterns.")
    subparsers.add_parser("monitor", help="Poll devices for uptime and daemon availability.")
    subparsers.add_parser("troubleshoot", help="Analyze failure root causes for unreachable devices.")
    subparsers.add_parser("test-connectivity", help="Execute ICMP reachability limits across the topology.")
    subparsers.add_parser("audit", help="Detect configuration drift: Compare physical state to intent specifications.")

    args = parser.parse_args()
    
    if args.command == "deploy":
        deploy_configurations(INVENTORY)
    elif args.command == "monitor":
        check_status(INVENTORY)
    elif args.command == "troubleshoot":
        analyze(INVENTORY)
    elif args.command == "test-connectivity":
        run_tests(INVENTORY)
    elif args.command == "audit":
        run_audit(INVENTORY)

if __name__ == "__main__":
    main()
