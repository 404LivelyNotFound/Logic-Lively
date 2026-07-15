import platflorm
import psutil
def get_system_info():
    """Get basic system information."""
    print_header("SYSTEM INFORMATION")
    print(f"Hostname: {platform.node()}")
    print(f"Operating System: {platform.system()}")
    print(f"OS Version: {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Cores: {psutil.cpu_count(logical=False)} (Physical), {psutil.cpu_count(logical=True)} (Logical)")