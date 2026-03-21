#!/usr/bin/env python
"""
Arista Bulk Deployment - Generate configs for multiple devices

This demonstrates the power of automation:
- Read switch data from CSV
- Use Jinja2 templates to generate Arista EOS configurations
- Apply to many devices simultaneously
- Reduce 100s of hours of manual work to minutes

Networking Use Case:
- Deploy 100 leaf switches in data center
- Each needs unique hostname, IP, VLAN config
- Template ensures consistency across all devices
- Easy to audit and version control

Author: Network Automation Engineer
"""

import csv
from jinja2 import Template
import json


# ============================================================================
# PART 1: JINJA2 TEMPLATE FOR ARISTA DEVICES
# ============================================================================

ARISTA_CONFIG_TEMPLATE = """
! Generated Arista EOS Configuration
! Hostname: {{ hostname }}
! Role: {{ role }}
! Generated: {{ timestamp }}

! ============================================================================
! SYSTEM CONFIGURATION
! ============================================================================
hostname {{ hostname }}
ip name-server {{ name_server1 }} {{ name_server2 }}

! ============================================================================
! INTERFACE: MANAGEMENT (out-of-band)
! ============================================================================
interface Management1
   description Out-of-band Management
   ip address {{ mgmt_ip }}/{{ mgmt_mask }}
   no shutdown

! ============================================================================
! INTERFACE: LOOPBACK (Router ID for BGP/OSPF)
! ============================================================================
interface Loopback0
   description Device Loopback Interface
   ip address {{ loopback_ip }}/32
   no shutdown

! ============================================================================
! PHYSICAL INTERFACES
! ============================================================================
{% for interface in interfaces %}

interface {{ interface['name'] }}
   description {{ interface['description'] }}
   {% if interface['enabled'] %}
   no shutdown
   {% else %}
   shutdown
   {% endif %}
   {% if interface['mtu'] %}
   mtu {{ interface['mtu'] }}
   {% endif %}
   {% if interface['speed'] %}
   speed {{ interface['speed'] }}
   {% endif %}

{% endfor %}

! ============================================================================
! VLAN CONFIGURATION (Layer 2 Segmentation)
! ============================================================================
{% for vlan in vlans %}
vlan {{ vlan['vlan_id'] }}
   name {{ vlan['name'] }}
   
{% endfor %}

! ============================================================================
! ROUTING CONFIGURATION (IP Routing)
! ============================================================================
ip routing

! ============================================================================
! SPANNING TREE (Prevents Layer 2 Loops)
! ============================================================================
spanning-tree mode rapid
spanning-tree vlan {{ primary_vlan }} priority {{ span_tree_priority }}

! ============================================================================
! END OF CONFIGURATION
! ============================================================================
"""


# ============================================================================
# PART 2: DEVICE DATA (Would normally come from source of truth)
# ============================================================================

DEVICES = [
    {
        'hostname': 'leaf-01',
        'role': 'Leaf Switch (Access Layer)',
        'timestamp': '2024-03-21T10:00:00Z',
        'mgmt_ip': '10.200.1.101',
        'mgmt_mask': 24,
        'loopback_ip': '10.0.0.1',
        'name_server1': '8.8.8.8',
        'name_server2': '8.8.4.4',
        'interfaces': [
            {
                'name': 'Ethernet1',
                'description': 'Uplink to Spine-01 (40G)',
                'enabled': True,
                'speed': '40G',
                'mtu': 1500
            },
            {
                'name': 'Ethernet2',
                'description': 'Uplink to Spine-02 (40G)',
                'enabled': True,
                'speed': '40G',
                'mtu': 1500
            },
            {
                'name': 'Ethernet3-24',
                'description': 'Access ports for servers',
                'enabled': True,
                'speed': '10G',
                'mtu': 1500
            }
        ],
        'vlans': [
            {'vlan_id': 1, 'name': 'default'},
            {'vlan_id': 10, 'name': 'Management'},
            {'vlan_id': 100, 'name': 'Production'},
            {'vlan_id': 200, 'name': 'Development'},
        ],
        'primary_vlan': 1,
        'span_tree_priority': 16384
    },
    {
        'hostname': 'leaf-02',
        'role': 'Leaf Switch (Access Layer)',
        'timestamp': '2024-03-21T10:00:00Z',
        'mgmt_ip': '10.200.1.102',
        'mgmt_mask': 24,
        'loopback_ip': '10.0.0.2',
        'name_server1': '8.8.8.8',
        'name_server2': '8.8.4.4',
        'interfaces': [
            {
                'name': 'Ethernet1',
                'description': 'Uplink to Spine-01 (40G)',
                'enabled': True,
                'speed': '40G',
                'mtu': 1500
            },
            {
                'name': 'Ethernet2',
                'description': 'Uplink to Spine-02 (40G)',
                'enabled': True,
                'speed': '40G',
                'mtu': 1500
            },
            {
                'name': 'Ethernet3-24',
                'description': 'Access ports for servers',
                'enabled': True,
                'speed': '10G',
                'mtu': 1500
            }
        ],
        'vlans': [
            {'vlan_id': 1, 'name': 'default'},
            {'vlan_id': 10, 'name': 'Management'},
            {'vlan_id': 100, 'name': 'Production'},
            {'vlan_id': 200, 'name': 'Development'},
        ],
        'primary_vlan': 1,
        'span_tree_priority': 16384
    },
]


# ============================================================================
# PART 3: CONFIGURATION GENERATION & DEPLOYMENT LOGIC
# ============================================================================

def generate_configurations(devices, output_dir="arista_configs"):
    """
    Generate Arista EOS configurations from device data and Jinja2 template
    
    This demonstrates:
    - Template rendering (filling variables into template)
    - Bulk configuration generation
    - Output to files (ready for deployment or review)
    
    Args:
        devices: List of device dictionaries
        output_dir: Directory where configs will be saved
    
    Returns:
        Dictionary with generation results
    """
    
    print(f"\n{'='*70}")
    print("ARISTA BULK CONFIGURATION GENERATION")
    print(f"{'='*70}")
    print(f"Template-based generation: 1 template + {len(devices)} devices")
    print(f"Output directory: {output_dir}\n")
    
    # Create Jinja2 template object
    template = Template(ARISTA_CONFIG_TEMPLATE, keep_trailing_newline=True)
    
    configurations = {}
    
    for device in devices:
        hostname = device['hostname']
        
        print(f"[{len(configurations)+1}/{len(devices)}] Generating config for {hostname}...", end="")
        
        try:
            # Render template with device data
            config = template.render(device)
            configurations[hostname] = config
            
            # Save to file
            filename = f"{output_dir}/{hostname}.eos"
            with open(filename, 'w') as f:
                f.write(config)
            
            print(" ✓ SUCCESS")
            
        except Exception as e:
            print(f" ✗ ERROR: {e}")
            configurations[hostname] = None
    
    return configurations


def generate_deployment_report(configurations):
    """
    Generate a deployment report showing what would be configured
    
    Useful for:
    - Change review and approval
    - Compliance checking
    - Documentation
    - Dry-run validation
    
    Args:
        configurations: Dictionary of generated configs
    """
    
    print(f"\n{'='*70}")
    print("DEPLOYMENT REPORT - Configuration Summary")
    print(f"{'='*70}\n")
    
    for hostname, config in configurations.items():
        if config:
            # Extract key information
            lines = config.split('\n')
            
            print(f"Device: {hostname}")
            print("-" * 50)
            
            # Show first few configuration lines
            config_lines = [l for l in lines if l and not l.startswith('!')]
            for line in config_lines[:10]:
                print(f"  {line}")
            
            print(f"  ... ({len(config_lines)} total configuration lines) ...\n")


def compare_configs(config1, config2, device1="Device1", device2="Device2"):
    """
    Compare two configurations to find differences
    
    Useful for:
    - Validating template consistency
    - Auditing configuration drift
    - Understanding what changes between devices
    
    Args:
        config1, config2: Configuration strings
        device1, device2: Device names for display
    """
    
    print(f"\n{'='*70}")
    print(f"CONFIGURATION COMPARISON: {device1} vs {device2}")
    print(f"{'='*70}\n")
    
    lines1 = config1.split('\n')
    lines2 = config2.split('\n')
    
    differences = 0
    for i, (line1, line2) in enumerate(zip(lines1, lines2)):
        if line1 != line2:
            differences += 1
            if differences <= 5:  # Show first 5 differences
                print(f"Line {i+1} differs:")
                print(f"  {device1}: {line1}")
                print(f"  {device2}: {line2}")
                print()
    
    if differences > 5:
        print(f"... and {differences - 5} more differences\n")
    
    print(f"Total differences: {differences}")


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Main demonstration of bulk configuration generation"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║     ARISTA BULK DEPLOYMENT - Configuration Generation         ║
║                                                                ║
║  Demonstrates network automation at scale:                    ║
║  • One Jinja2 template                                        ║
║  • Multiple devices with unique data                          ║
║  • Generates complete EOS configurations                      ║
║  • Ready for deployment or review                             ║
║                                                                ║
║  Real-world use case:                                         ║
║  • Deploy 100 leaf switches in data center                    ║
║  • Generate consistency checked configs in minutes            ║
║  • Vs. 100 hours of manual CLI entry                          ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Generate configurations
    configs = generate_configurations(DEVICES, output_dir=".")
    
    # Show generation results
    print(f"\n{'='*70}")
    print("GENERATION RESULTS")
    print(f"{'='*70}")
    print(f"Total devices processed: {len(DEVICES)}")
    print(f"Successful: {sum(1 for c in configs.values() if c)}")
    print(f"Failed: {sum(1 for c in configs.values() if not c)}")
    
    # Generate and show deployment report
    generate_deployment_report(configs)
    
    # Compare two generated configs
    if len(configs) >= 2:
        hostnames = list(configs.keys())
        config1 = configs[hostnames[0]]
        config2 = configs[hostnames[1]]
        
        if config1 and config2:
            compare_configs(config1, config2, hostnames[0], hostnames[1])
    
    # Show example of one generated configuration
    first_hostname = list(configs.keys())[0]
    if configs[first_hostname]:
        print(f"\n{'='*70}")
        print(f"EXAMPLE CONFIGURATION: {first_hostname}")
        print(f"{'='*70}\n")
        print(configs[first_hostname])
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    AUTOMATION BENEFITS                         ║
║                                                                ║
║  Without Automation:                                          ║
║  • 100 switches × 30 minutes each = 3000 minutes (50 hours)   ║
║  • Manual errors and inconsistencies                          ║
║  • No audit trail of changes                                  ║
║  • Risk of network outages from typos                         ║
║                                                                ║
║  With Automation (This Script):                               ║
║  • 100 switches in < 1 minute                                 ║
║  • Guaranteed consistency via template                        ║
║  • Full audit trail (version control)                         ║
║  • Testable and reviewable before deployment                  ║
║                                                                ║
║  Business Impact: Save ~50 hours per deployment!              ║
║  Across 365 days, that's 18,250 hours = 8+ FTE engineers     ║
╚════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
