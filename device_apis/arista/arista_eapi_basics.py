#!/usr/bin/env python
"""
Arista eAPI Basics - Connect and retrieve device information

This script demonstrates:
1. Connecting to Arista EOS devices via eAPI (JSON-RPC over HTTP/HTTPS)
2. Retrieving device information (hostname, model, serial number)
3. Getting interface status (networking basics - Layer 1/Layer 2 info)
4. Understanding network terminology: interfaces, VLANs, IP addressing

Arista eAPI Documentation: https://aristanetworks.github.io/EosSdk/docs/

Author: Network Automation Engineer
Date: 2024
"""

# For testing without actual Arista device - Mock example
# In production, install: pip install jsonrpc

# Mock implementation for learning (works without Arista device)
class MockArista:
    """Mock Arista device for learning"""
    
    def __init__(self, host, username="admin", password="arista"):
        self.host = host
        self.username = username
        self.password = password
        print(f"[MOCK] Connected to Arista device at {host}")
        
    def runCmds(self, version, commands, ofmt='json'):
        """Mock eAPI runCmds method"""
        # Simulate Arista responses
        responses = {
            'show version': {
                'modelName': 'DCS-7050SX3-48YC8',
                'systemMacAddress': '00:1c:73:12:34:56',
                'serialNumber': 'ABC123456789',
                'version': '4.28.3F',
                'architecture': 'i686',
                'internalVersion': '4.28.3F-28885132.4283F',
                'bootupTimestamp': 1646400000
            },
            'show interfaces': {
                'interfaces': {
                    'Ethernet1': {
                        'name': 'Ethernet1',
                        'interfaceStatus': 'up',
                        'lineProtocolStatus': 'up',
                        'description': 'Link to Core Switch',
                        'mtu': 1500,
                        'bandwidth': 40000000
                    },
                    'Ethernet2': {
                        'name': 'Ethernet2',
                        'interfaceStatus': 'down',
                        'lineProtocolStatus': 'down',
                        'description': 'Spare Link',
                        'mtu': 1500,
                        'bandwidth': 40000000
                    }
                }
            },
            'show vlan': {
                'vlans': {
                    '1': {'name': 'default', 'status': 'active'},
                    '10': {'name': 'Management', 'status': 'active'},
                    '20': {'name': 'Production', 'status': 'active'},
                    '100': {'name': 'Guest', 'status': 'suspended'}
                }
            },
            'show ip interface': {
                'interfaces': {
                    'Management1': {
                        'ipAddress': '10.1.1.100',
                        'mask': 24,
                        'addressOrigin': 'static',
                        'interfaceStatus': 'up'
                    }
                }
            },
            'show running-config': {
                'output': '''
! Arista EOS Configuration
hostname MySwitch
!
interface Ethernet1
   description Link to Core
   no shutdown
!
interface Ethernet2
   shutdown
!
vlan 10
   name Management
!
ip routing
                '''
            }
        }
        
        # Return matching responses
        for cmd in commands:
            if cmd in responses:
                return [responses[cmd]]
        return [{}]


# ============================================================================
# PART 1: BASIC CONNECTION & DEVICE INFORMATION
# ============================================================================

def get_device_info(device):
    """
    Get basic device information
    
    Networking Concept: Device identification
    - Hostname: Unique identifier for the device
    - Model: Hardware information (throughput, port count, power)
    - Serial Number: For RMA/warranty tracking
    - Software Version: Critical for bug fixes and features
    
    Args:
        device: Device object (MockArista or JsonRpcClient)
    """
    try:
        # EOS command: show version
        # This returns comprehensive device information including OS version
        response = device.runCmds(1, ["show version"])
        
        if response and response[0]:
            info = response[0]
            
            print("\n" + "="*60)
            print("ARISTA DEVICE INFORMATION")
            print("="*60)
            print(f"Hostname:         {device.host}")
            print(f"Model:            {info.get('modelName', 'Unknown')}")
            print(f"Serial Number:    {info.get('serialNumber', 'Unknown')}")
            print(f"EOS Version:      {info.get('version', 'Unknown')}")
            print(f"System MAC:       {info.get('systemMacAddress', 'Unknown')}")
            print("="*60 + "\n")
            
            return info
    except Exception as e:
        print(f"Error getting device info: {e}")
        return None


# ============================================================================
# PART 2: INTERFACE INFORMATION (NETWORKING BASICS)
# ============================================================================

def get_interface_status(device):
    """
    Get interface information - NETWORKING FUNDAMENTALS
    
    Networking Concepts:
    - Interface: Physical port on network device (Ethernet1, Ethernet2, etc.)
    - Interface Status: Physical layer (Layer 1) - up/down
    - Line Protocol Status: Data link layer (Layer 2) - up/down
    - Both must be UP for traffic to flow
    - MTU: Maximum Transmission Unit (default 1500 bytes for Ethernet)
    - Bandwidth: Port speed (1G, 10G, 25G, 40G, 100G, 400G)
    
    Arista port naming:
    - Ethernet1-48: 1G/10G/25G ports (typical leaf)
    - Ethernet49-52: 40G/100G ports (typical uplinks to spine)
    
    Args:
        device: Device object
    """
    try:
        response = device.runCmds(1, ["show interfaces"])
        interfaces = response[0].get('interfaces', {})
        
        print("\n" + "="*80)
        print("INTERFACE STATUS (Layer 1 & Layer 2)")
        print("="*80)
        print(f"{'Interface':<15} {'Status':<10} {'Protocol':<10} {'Description':<30}")
        print("-"*80)
        
        for interface_name, interface_data in interfaces.items():
            status = interface_data.get('interfaceStatus', 'unknown')
            protocol = interface_data.get('lineProtocolStatus', 'unknown')
            description = interface_data.get('description', 'No description')
            
            # Color coding for status (in production, use colorama)
            status_symbol = "✓" if status == "up" else "✗"
            
            print(f"{interface_name:<15} {status:<10} {protocol:<10} {description:<30} {status_symbol}")
        
        print("="*80 + "\n")
        
        return interfaces
        
    except Exception as e:
        print(f"Error getting interface status: {e}")
        return None


# ============================================================================
# PART 3: VLAN INFORMATION
# ============================================================================

def get_vlan_info(device):
    """
    Get VLAN information - LAYER 2 NETWORKING
    
    Networking Concepts:
    - VLAN (Virtual LAN): Logical segmentation of network
    - VLAN ID: Number 1-4094 (1 is default, 1002-1005 reserved)
    - VLAN Name: Description of VLAN purpose
    - VLAN Status: active/suspended
    
    Why VLANs matter:
    - Separate broadcast domains
    - Improve security (don't see other VLANs' traffic)
    - Improve performance (broadcast storms contained)
    - Enable efficient IP space usage
    
    Args:
        device: Device object
    """
    try:
        response = device.runCmds(1, ["show vlan"])
        vlans = response[0].get('vlans', {})
        
        print("\n" + "="*60)
        print("VLAN CONFIGURATION (Layer 2 Segmentation)")
        print("="*60)
        print(f"{'VLAN ID':<10} {'Name':<20} {'Status':<15}")
        print("-"*60)
        
        for vlan_id, vlan_data in vlans.items():
            name = vlan_data.get('name', 'Unknown')
            status = vlan_data.get('status', 'Unknown')
            
            print(f"{vlan_id:<10} {name:<20} {status:<15}")
        
        print("="*60 + "\n")
        
        return vlans
        
    except Exception as e:
        print(f"Error getting VLAN info: {e}")
        return None


# ============================================================================
# PART 4: IP INTERFACE CONFIGURATION
# ============================================================================

def get_ip_interface_info(device):
    """
    Get IP interface information - LAYER 3 NETWORKING
    
    Networking Concepts:
    - IP Address: Unique Layer 3 identifier (IPv4/IPv6)
    - Subnet Mask: Defines network size (/24 = 256 IPs, /30 = 4 IPs)
    - Address Origin: static (manually configured) or dhcp (automatic)
    - Management Interface: Out-of-band connection for device management
    
    Arista Management:
    - Management1: Out-of-band Ethernet port
    - Used for: SSH, API, monitoring
    - Separate from data plane traffic
    
    Args:
        device: Device object
    """
    try:
        response = device.runCmds(1, ["show ip interface"])
        interfaces = response[0].get('interfaces', {})
        
        print("\n" + "="*70)
        print("IP INTERFACE CONFIGURATION (Layer 3 - Routing)")
        print("="*70)
        print(f"{'Interface':<15} {'IP Address':<20} {'Mask':<10} {'Status':<10}")
        print("-"*70)
        
        for interface_name, interface_data in interfaces.items():
            ip = interface_data.get('ipAddress', 'No IP')
            mask = interface_data.get('mask', '')
            status = interface_data.get('interfaceStatus', 'unknown')
            
            ip_info = f"{ip}/{mask}" if mask else ip
            
            print(f"{interface_name:<15} {ip_info:<20} {status:<10}")
        
        print("="*70 + "\n")
        
        return interfaces
        
    except Exception as e:
        print(f"Error getting IP interface info: {e}")
        return None


# ============================================================================
# PART 5: RUNNING CONFIGURATION
# ============================================================================

def get_running_config(device):
    """
    Get device running configuration
    
    Why this matters:
    - Current state of device configuration
    - Used for backups and disaster recovery
    - Used for change management (compare old vs new)
    - Used for compliance auditing
    
    Args:
        device: Device object
    """
    try:
        response = device.runCmds(1, ["show running-config"])
        config = response[0].get('output', '')
        
        print("\n" + "="*60)
        print("RUNNING CONFIGURATION (Current Device State)")
        print("="*60)
        print(config)
        print("="*60 + "\n")
        
        return config
        
    except Exception as e:
        print(f"Error getting running config: {e}")
        return None


# ============================================================================
# MAIN: RUN ALL EXAMPLES
# ============================================================================

def main():
    """
    Main function demonstrating Arista eAPI fundamentals
    """
    print("""
╔════════════════════════════════════════════════════════════════╗
║     ARISTA eAPI FUNDAMENTALS - NETWORK AUTOMATION             ║
║                                                                ║
║  This script demonstrates:                                    ║
║  1. Device connectivity (how to talk to Arista switches)      ║
║  2. Network basics (interfaces, VLANs, IP routing)            ║
║  3. Data retrieval (parsing JSON responses)                   ║
║  4. Automation concepts (programmatic device control)         ║
║                                                                ║
║  To use with REAL Arista device, uncomment below and         ║
║  change host/username/password                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # For LEARNING: Using MockArista (no real device needed)
    device = MockArista(host="10.1.1.100")
    
    # For PRODUCTION: Uncomment this (requires 'pip install jsonrpc')
    # from jsonrpc import JsonRpcClient
    # device = JsonRpcClient(host="10.1.1.100", username="admin", password="arista")
    
    # Run demonstrations
    device_info = get_device_info(device)
    interface_status = get_interface_status(device)
    vlan_info = get_vlan_info(device)
    ip_config = get_ip_interface_info(device)
    running_config = get_running_config(device)
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║  NETWORKING CONCEPTS LEARNED:                                 ║
║  ✓ OSI Model Layer 1 (Physical) - Interfaces, cables          ║
║  ✓ OSI Model Layer 2 (Data Link) - VLANs, MAC addresses       ║
║  ✓ OSI Model Layer 3 (Network) - IP addresses, routing        ║
║  ✓ Device Management - SSH, APIs, out-of-band access         ║
║  ✓ Automation - Programmatic device control                  ║
║                                                                ║
║  WHAT'S NEXT:                                                  ║
║  1. Try arista_eapi_config.py - Configure devices             ║
║  2. Try arista_bulk_deploy.py - Deploy to many devices        ║
║  3. Study CloudVision Platform for multi-device management    ║
╚════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
