import subprocess
import time

class DockerClient:
    def __init__(self, logger):
        self.logger = logger
        
    def execute(self, container_name, command, retries=2, delay=2, timeout=5):
        """
        Executes a command inside a docker container.
        Includes retry logic, backoff delay, and timeout protections.
        """
        for attempt in range(1, retries + 1):
            try:
                result = subprocess.run(
                    f'docker exec {container_name} sh -c "{command}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                if result.returncode == 0:
                    return True, result.stdout.strip()
                else:
                    error_msg = result.stderr.strip() or result.stdout.strip()
                    
                    # Hard failure if container is missing/not running
                    if "is not running" in error_msg or "No such container" in error_msg:
                        self.logger.error(f"[{container_name}] Critical: Container offline.")
                        return False, "Container is offline"
                    
                    self.logger.debug(f"[{container_name}] Attempt {attempt} failed: {error_msg}")
                    last_error = error_msg
                    
            except subprocess.TimeoutExpired:
                self.logger.warning(f"[{container_name}] Timeout expired (attempt {attempt}/{retries}).")
                last_error = "Timeout expired"
            except Exception as e:
                self.logger.error(f"[{container_name}] Host execution error: {e}")
                last_error = str(e)
                
            if attempt < retries:
                time.sleep(delay)
                
        return False, f"Failed after {retries} attempts: {last_error}"
