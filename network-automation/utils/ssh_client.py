"""
SSH Client for Network Device Communication
Real SSH connections to Docker containers or actual network devices
"""

import paramiko
import logging
from typing import List, Dict, Any
import time

logger = logging.getLogger(__name__)


class SSHClient:
    """
    Secure SSH connection to network devices
    Supports both real network devices and Docker containers
    """

    def __init__(self, hostname: str, port: int, username: str, password: str, device_name: str = "device"):
        """
        Initialize SSH connection parameters
        
        Args:
            hostname: IP or hostname of device
            port: SSH port (typically 22, or 2201/2202 for Docker)
            username: SSH username
            password: SSH password
            device_name: Friendly name for logging
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.device_name = device_name
        self.client = None
        self.connected = False

    def connect(self, timeout: int = 10) -> bool:
        """
        Establish SSH connection to device
        
        Args:
            timeout: Connection timeout in seconds
            
        Returns:
            True if connected, False otherwise
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            logger.info(f"[{self.device_name}] Connecting to {self.hostname}:{self.port}")
            
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=timeout,
                look_for_keys=False,
                allow_agent=False
            )
            
            self.connected = True
            logger.info(f"[{self.device_name}] ✓ Connected successfully")
            return True
            
        except paramiko.AuthenticationException:
            logger.error(f"[{self.device_name}] ✗ Authentication failed")
            return False
        except paramiko.SSHException as e:
            logger.error(f"[{self.device_name}] ✗ SSH error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"[{self.device_name}] ✗ Connection error: {str(e)}")
            return False

    def execute_command(self, command: str, wait_time: float = 1.0) -> str:
        """
        Execute single command on device
        
        Args:
            command: Command to execute
            wait_time: Time to wait for command completion
            
        Returns:
            Command output as string
        """
        if not self.connected or self.client is None:
            logger.error(f"[{self.device_name}] Not connected")
            return ""

        try:
            logger.debug(f"[{self.device_name}] Executing: {command}")
            
            stdin, stdout, stderr = self.client.exec_command(command)
            time.sleep(wait_time)
            
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            
            if error and "Warning" not in error:
                logger.warning(f"[{self.device_name}] Error: {error}")
            
            return output
            
        except Exception as e:
            logger.error(f"[{self.device_name}] Command failed: {str(e)}")
            return f"ERROR: {str(e)}"

    def execute_commands(self, commands: List[str], wait_time: float = 1.0) -> Dict[str, str]:
        """
        Execute multiple commands
        
        Args:
            commands: List of commands to execute
            wait_time: Time to wait between commands
            
        Returns:
            Dictionary mapping commands to outputs
        """
        results = {}
        for cmd in commands:
            time.sleep(wait_time)
            results[cmd] = self.execute_command(cmd, wait_time)
        return results

    def configure_interface(self, interface: str, ip_address: str, description: str = "") -> bool:
        """
        Configure interface with IP address
        
        Args:
            interface: Interface name (e.g., 'eth0')
            ip_address: IP address with CIDR (e.g., '192.168.1.1/24')
            description: Interface description
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"[{self.device_name}] Configuring {interface} with {ip_address}")
            
            commands = [
                f"vtysh -c 'configure terminal' -c 'interface {interface}' -c 'ip address {ip_address.split('/')[0]} 255.255.255.0' -c 'description {description}' -c 'no shutdown'"
            ]
            
            for cmd in commands:
                output = self.execute_command(cmd)
                if "error" in output.lower():
                    logger.error(f"[{self.device_name}] Config error: {output}")
                    return False
            
            logger.info(f"[{self.device_name}] ✓ Interface configured")
            return True
            
        except Exception as e:
            logger.error(f"[{self.device_name}] Configuration failed: {str(e)}")
            return False

    def show_running_config(self) -> str:
        """Get running configuration"""
        return self.execute_command("vtysh -c 'show running-config'")

    def show_interfaces(self) -> str:
        """Get interface status"""
        return self.execute_command("vtysh -c 'show interface'")

    def show_ip_route(self) -> str:
        """Get routing table"""
        return self.execute_command("vtysh -c 'show ip route'")

    def get_interface_status(self, interface: str) -> str:
        """Get status of specific interface"""
        return self.execute_command(f"ip addr show {interface}")

    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info(f"[{self.device_name}] Disconnected")

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
