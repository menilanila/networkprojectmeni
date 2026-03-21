#!/usr/bin/env python
"""
Arista eAPI Configuration - Programmatic Device Management

This script demonstrates:
1. Configuring interfaces (enable/disable, descriptions, settings)
2. Configuring VLANs
3. Configuring IP addresses
4. Validating configurations
5. Best practices for safe configuration

Key Concepts:
- eAPI uses commands just like CLI but delivered over HTTP/JSON
- Multiple commands can be sent in one request (efficient)
- Dry-run mode allows testing before committing
- Error handling is critical for network changes

Author: Network Automation Engineer
"""

class MockArista:
    """Mock Arista device for learning"""
    
    def __init__(self, host, username="admin", password="arista"):
        self.host = host
        self.username = username
        self.password = password
        self.config_mode = False
        print(f"[MOCK] eAPI Session established to {host}")
        
    def runCmds(self, version, commands, ofmt='json'):
        """Mock eAPI with command simulation"""
        responses = []
        
        for cmd in commands:
            if cmd == "configure":
                self.config_mode = True
                responses.append({"result": "Success", "message": "Enter config mode"})
            elif cmd in ["exit", "end"]:
                self.config_mode = False
                responses.append({"result": "Success", "message": "Exit config mode"})
            elif "interface" in cmd:
                responses.append({
                    "result": "Success",
                    "message": f"Configured: {cmd}"
                })
            elif "vlan" in cmd:
                responses.append({
                    "result": "Success", 
                    "message": f"VLAN configured: {cmd}"
                })
            elif "ip address" in cmd:
                responses.append({
                    "result": "Success",
                    "message": f"IP configured: {cmd}"
                })
            else:
                responses.append({"result": "Success", "message": f"Executed: {cmd}"})
        
        return responses


# ============================================================================
# PART 1: INTERFACE CONFIGURATION
# ============================================================================

def configure_interface(device, interface_name, description, enabled=True, 
                       port_speed=None, mtu=1500, dry_run=False):
    """
    Configure a single interface with best practices
    
    Networking Concepts:
    - Interface naming: Ethernet1, Ethernet2 (physical ports)
    - Port speed: Auto, 1G, 10G, 25G, 40G, 100G (depends on hardware)
    - MTU: Data packet size (1500 default, 9000 for jumbo frames)
    - Description: Critical for troubleshooting and documentation
    - shutdown command: Disables interface (best practice: disable unused ports)
    
    Args:
        device: Device object
        interface_name: Interface to configure (e.g., "Ethernet1")
        description: Interface description (required for audit trail)
        enabled: True to enable, False to shutdown
        port_speed: Optional port speed configuration
        mtu: Maximum transmission unit (default 1500)
        dry_run: If True, show what would be done without executing
    """
    
    # Build configuration commands
    config_commands = [
        "configure",
        f"interface {interface_name}",
        f"description {description}",
        f"mtu {mtu}",
    ]
    
    # Add speed configuration if specified
    if port_speed:
        config_commands.append(f"speed {port_speed}")
    
    # Add shutdown/no shutdown
    if enabled:
        config_commands.append("no shutdown")
    else:
        config_commands.append("shutdown")
    
    config_commands.extend(["exit", "end"])
    
    print(f"\n{'='*70}")
    print(f"INTERFACE CONFIGURATION: {interface_name}")
    print(f"{'='*70}")
    print(f"Description: {description}")
    print(f"Status: {'ENABLED' if enabled else 'DISABLED'}")
    print(f"MTU: {mtu}")
    if port_speed:
        print(f"Speed: {port_speed}")
    
    print(f"\nEOS Commands to execute:")
    print("-"*70)
    for cmd in config_commands:
        print(f"  {cmd}")
    print("-"*70)
    
    # Execute or dry-run
    if dry_run:
        print(f"\n[DRY-RUN] Configuration NOT applied (preview only)")
        return {"status": "preview", "commands": config_commands}
    else:
        try:
            responses = device.runCmds(1, config_commands)
            print(f"\n✓ Configuration applied successfully")
            return {"status": "success", "responses": responses}
        except Exception as e:
            print(f"\n✗ Configuration failed: {e}")
            return {"status": "failed", "error": str(e)}


# ============================================================================
# PART 2: VLAN CONFIGURATION
# ============================================================================

def configure_vlan(device, vlan_id, vlan_name, vlan_description, dry_run=False):
    """
    Create and configure VLAN
    
    Networking Concepts:
    - VLAN ID: 1-4094 (1 is default, avoid 1002-1005 which are reserved for legacy)
    - VLAN Name: Short identifier for the VLAN
    - Member ports: Which interfaces belong to this VLAN
    - Trunk vs Access: 
      * Access: Single VLAN per port (typical end devices)
      * Trunk: Multiple VLANs on one port (between switches)
    
    Args:
        device: Device object
        vlan_id: VLAN number (1-4094)
        vlan_name: Human-readable name
        vlan_description: Purpose of this VLAN
        dry_run: Preview without executing
    """
    
    # Validate VLAN ID
    if not (1 <= vlan_id <= 4094):
        print(f"✗ Error: VLAN ID {vlan_id} out of range (1-4094)")
        return {"status": "failed", "error": "Invalid VLAN ID"}
    
    config_commands = [
        "configure",
        f"vlan {vlan_id}",
        f"name {vlan_name}",
        "exit",
        "end"
    ]
    
    print(f"\n{'='*70}")
    print(f"VLAN CONFIGURATION")
    print(f"{'='*70}")
    print(f"VLAN ID: {vlan_id}")
    print(f"Name: {vlan_name}")
    print(f"Purpose: {vlan_description}")
    
    print(f"\nEOS Commands:")
    print("-"*70)
    for cmd in config_commands:
        print(f"  {cmd}")
    print("-"*70)
    
    if dry_run:
        print(f"\n[DRY-RUN] VLAN configuration NOT applied")
        return {"status": "preview", "commands": config_commands}
    else:
        try:
            responses = device.runCmds(1, config_commands)
            print(f"\n✓ VLAN {vlan_id} configured successfully")
            return {"status": "success", "responses": responses}
        except Exception as e:
            print(f"\n✗ VLAN configuration failed: {e}")
            return {"status": "failed", "error": str(e)}


# ============================================================================
# PART 3: INTERFACE VLAN MEMBERSHIP
# ============================================================================

def set_interface_vlan(device, interface_name, vlan_id, mode="access", dry_run=False):
    """
    Set interface to specific VLAN
    
    Networking Concepts:
    - Access mode: Single VLAN (typical for end-user devices)
      * Only traffic from that VLAN flows on port
      * Example: Server port in VLAN 10
    
    - Trunk mode: Multiple VLANs (inter-switch links)
      * All VLANs tagged and sent over link
      * Example: Uplink between leaf and spine
    
    Args:
        device: Device object
        interface_name: Interface to configure
        vlan_id: VLAN number
        mode: "access" or "trunk"
        dry_run: Preview without executing
    """
    
    config_commands = [
        "configure",
        f"interface {interface_name}",
        f"switchport mode {mode}",
    ]
    
    if mode == "access":
        config_commands.append(f"switchport access vlan {vlan_id}")
    elif mode == "trunk":
        config_commands.append(f"switchport trunk allowed vlan {vlan_id}")
    
    config_commands.extend(["exit", "end"])
    
    print(f"\n{'='*70}")
    print(f"INTERFACE VLAN MEMBERSHIP")
    print(f"{'='*70}")
    print(f"Interface: {interface_name}")
    print(f"Mode: {mode.upper()}")
    print(f"VLAN: {vlan_id}")
    
    print(f"\nEOS Commands:")
    print("-"*70)
    for cmd in config_commands:
        print(f"  {cmd}")
    print("-"*70)
    
    if dry_run:
        print(f"\n[DRY-RUN] VLAN membership NOT applied")
        return {"status": "preview", "commands": config_commands}
    else:
        try:
            responses = device.runCmds(1, config_commands)
            print(f"\n✓ Interface {interface_name} set to VLAN {vlan_id} ({mode} mode)")
            return {"status": "success", "responses": responses}
        except Exception as e:
            print(f"\n✗ Configuration failed: {e}")
            return {"status": "failed", "error": str(e)}


# ============================================================================
# PART 4: IP ADDRESS CONFIGURATION
# ============================================================================

def configure_ip_address(device, interface_name, ip_address, subnet_mask, 
                        description="", dry_run=False):
    """
    Configure IP address on interface (Layer 3)
    
    Networking Concepts:
    - IP Address: Layer 3 identifier (e.g., 192.168.1.1)
    - Subnet Mask: Network size indicator (e.g., /24 = 256 addresses)
    - CIDR notation: /24 = 255.255.255.0 (standard in modern networks)
    - SVI (Switched Virtual Interface): IP on VLAN, not physical port
    
    Use case:
    - Physical interface: Management1 (mgmt port)
    - SVI: interface vlan 10 (routed VLAN interface)
    
    Args:
        device: Device object
        interface_name: Interface or VLAN to configure
        ip_address: IP address (e.g., "10.1.1.1")
        subnet_mask: CIDR mask (e.g., 24) or dotted decimal (e.g., "255.255.255.0")
        description: Optional interface description
        dry_run: Preview only
    """
    
    # Convert subnet mask to CIDR if needed
    if subnet_mask.count('.') == 3:
        # Convert 255.255.255.0 to /24
        # This is a simplified version - use netaddr for production
        if subnet_mask == "255.255.255.0":
            cidr = 24
        elif subnet_mask == "255.255.0.0":
            cidr = 16
        else:
            cidr = subnet_mask
    else:
        cidr = subnet_mask
    
    config_commands = [
        "configure",
        f"interface {interface_name}",
    ]
    
    if description:
        config_commands.append(f"description {description}")
    
    config_commands.extend([
        f"ip address {ip_address}/{cidr}",
        "no shutdown",
        "exit",
        "end"
    ])
    
    print(f"\n{'='*70}")
    print(f"IP ADDRESS CONFIGURATION (Layer 3 Routing)")
    print(f"{'='*70}")
    print(f"Interface: {interface_name}")
    print(f"IP Address: {ip_address}/{cidr}")
    if description:
        print(f"Description: {description}")
    
    print(f"\nEOS Commands:")
    print("-"*70)
    for cmd in config_commands:
        print(f"  {cmd}")
    print("-"*70)
    
    if dry_run:
        print(f"\n[DRY-RUN] IP configuration NOT applied")
        return {"status": "preview", "commands": config_commands}
    else:
        try:
            responses = device.runCmds(1, config_commands)
            print(f"\n✓ IP address {ip_address}/{cidr} configured on {interface_name}")
            return {"status": "success", "responses": responses}
        except Exception as e:
            print(f"\n✗ Configuration failed: {e}")
            return {"status": "failed", "error": str(e)}


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate Arista configuration capabilities"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║          ARISTA PROGRAMMATIC CONFIGURATION (eAPI)             ║
║                                                                ║
║  This demonstrates how to configure Arista EOS devices        ║
║  programmatically instead of manual CLI entry.                ║
║                                                                ║
║  Benefits:                                                     ║
║  • Faster deployment (1000s of devices in minutes)            ║
║  • Consistent configurations (no typos)                       ║
║  • Version control and audit trail                            ║
║  • Integration with orchestration tools                       ║
║                                                                ║
║  NOTE: All commands shown in DRY-RUN mode (preview only)      ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Connect to device (mock in this demo)
    device = MockArista(host="10.1.1.100")
    
    # Example 1: Configure interface
    configure_interface(
        device,
        interface_name="Ethernet1",
        description="Link to Core Switch",
        enabled=True,
        mtu=1500,
        dry_run=True  # Preview only
    )
    
    # Example 2: Create VLAN
    configure_vlan(
        device,
        vlan_id=100,
        vlan_name="Production",
        vlan_description="Production servers and resources",
        dry_run=True
    )
    
    # Example 3: Set interface to VLAN (access mode)
    set_interface_vlan(
        device,
        interface_name="Ethernet2",
        vlan_id=100,
        mode="access",
        dry_run=True
    )
    
    # Example 4: Configure IP address
    configure_ip_address(
        device,
        interface_name="Management1",
        ip_address="10.1.1.100",
        subnet_mask="24",
        description="Out-of-band management interface",
        dry_run=True
    )
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    BEST PRACTICES SUMMARY                      ║
║                                                                ║
║  ✓ Always use descriptions for documentation                  ║
║  ✓ Use dry-run mode before applying to production             ║
║  ✓ Validate configuration on test device first                ║
║  ✓ Use version control for configuration scripts              ║
║  ✓ Log all configuration changes for audit trail              ║
║  ✓ Implement error handling and rollback capability           ║
║  ✓ Use configuration templates for consistency                ║
║  ✓ Integrate with change management process                   ║
║                                                                ║
║  TO USE WITH REAL DEVICE:                                     ║
║  1. Change dry_run=False in function calls                    ║
║  2. Update host IP and credentials                            ║
║  3. Install: pip install jsonrpc                              ║
║  4. Uncomment JsonRpcClient import                            ║
║  5. Test on non-production device first!                      ║
╚════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
