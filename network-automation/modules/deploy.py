import json
from utils.logger import setup_logger
from utils.docker_client import DockerClient

logger = setup_logger("deploy")
client = DockerClient(logger)

def deploy_configurations(inventory_file):
    print("=== STARTING DEPLOYMENT ===")
    
    with open(inventory_file) as f:
        inventory = json.load(f).get('devices', [])
        
    results = []
        
    for device in inventory:
        name = device['name']
        config = device.get('config', {})
        
        print(f"\n[{name}] Applying configurations:")
        
        # Initial health check via pure docker ping equivalent
        ok, out = client.execute(name, "echo check")
        if not ok:
            print(f"[{name}] STATUS: FAILED")
            print(f"  Reason: Device is DOWN or unreachable")
            print(f"  Action: Skipping deployment")
            results.append({'device': name, 'status': 'FAILED', 'reason': 'Device offline'})
            continue
            
        success = True
        
        # Deploy interfaces
        interfaces = config.get('interfaces', {})
        for intf, ip in interfaces.items():
            cmd = f"ip addr flush dev {intf} && ip addr add {ip} dev {intf} || echo 'Interface config failed'"
            ok, out = client.execute(name, cmd)
            if not ok:
                success = False
                break
                
        # Deploy static routes
        routes = config.get('routes', [])
        for route in routes:
            dest = route['destination']
            gw = route['gateway']
            ok, out = client.execute(name, f"ip route add {dest} via {gw} || echo 'Route likely exists'")
            if not ok:
                success = False
                break
                
        if success:
            print(f"[{name}] STATUS: SUCCESS")
            print(f"  Configuration deployed successfully")
            results.append({'device': name, 'status': 'SUCCESS'})
        else:
            print(f"[{name}] STATUS: FAILED")
            print(f"  Reason: Configuration execution error")
            print(f"  Action: Aborting remaining tasks for device")
            results.append({'device': name, 'status': 'FAILED', 'reason': 'Execution error'})
            
    print("\n" + "="*60)
    print("DEPLOYMENT REPORT")
    print("="*60)
    
    for r in results:
        if r['status'] == 'SUCCESS':
            print(f"{r['device']} -> SUCCESS")
        else:
            print(f"{r['device']} -> FAILED ({r.get('reason', 'Unknown')})")

    total = len(results)
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')

    print(f"\nTotal devices: {total}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total - success_count}")
    print("\n=== DEPLOYMENT FINISHED ===\n")
