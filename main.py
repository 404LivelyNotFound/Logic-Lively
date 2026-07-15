#!/usr/bin/env python3
"""
Logic Lively - Get logistical assistance with your computer systems.
Provides comprehensive system diagnostics on startup.
"""

import os
import platform
import psutil
from datetime import datetime
from diags system import get system info
def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


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


def get_cpu_info():
    """Get CPU diagnostics."""
    print_header("CPU DIAGNOSTICS")
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    print("\nPer-core CPU Usage:")
    per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    for i, percent in enumerate(per_cpu):
        print(f"  Core {i}: {percent}%")
    
    # Get CPU frequency
    try:
        freq = psutil.cpu_freq()
        print(f"\nCPU Frequency: {freq.current:.2f} MHz")
        print(f"  Max: {freq.max:.2f} MHz")
        print(f"  Min: {freq.min:.2f} MHz")
    except Exception as e:
        print(f"CPU Frequency: Unable to retrieve ({e})")


def get_memory_info():
    """Get memory diagnostics."""
    print_header("MEMORY DIAGNOSTICS")
    memory = psutil.virtual_memory()
    print(f"Total Memory: {memory.total / (1024**3):.2f} GB")
    print(f"Available Memory: {memory.available / (1024**3):.2f} GB")
    print(f"Used Memory: {memory.used / (1024**3):.2f} GB")
    print(f"Memory Usage: {memory.percent}%")
    
    # Swap memory
    swap = psutil.swap_memory()
    print(f"\nSwap Memory Total: {swap.total / (1024**3):.2f} GB")
    print(f"Swap Memory Used: {swap.used / (1024**3):.2f} GB")
    print(f"Swap Usage: {swap.percent}%")


def get_disk_info():
    """Get disk diagnostics."""
    print_header("DISK DIAGNOSTICS")
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"\nDevice: {partition.device}")
            print(f"  Mount Point: {partition.mountpoint}")
            print(f"  File System: {partition.fstype}")
            print(f"  Total: {usage.total / (1024**3):.2f} GB")
            print(f"  Used: {usage.used / (1024**3):.2f} GB")
            print(f"  Free: {usage.free / (1024**3):.2f} GB")
            print(f"  Usage: {usage.percent}%")
        except PermissionError:
            print(f"\nDevice: {partition.device} - Permission Denied")


def get_network_info():
    """Get network diagnostics."""
    print_header("NETWORK DIAGNOSTICS")
    
    # Network interfaces
    net_if_stats = psutil.net_if_stats()
    print("Network Interfaces:")
    for interface, stats in net_if_stats.items():
        status = "Up" if stats.isup else "Down"
        print(f"  {interface}: {status}")
        print(f"    Speed: {stats.speed} Mbps")
        print(f"    MTU: {stats.mtu}")
    
    # Network I/O stats
    net_io = psutil.net_io_counters()
    print(f"\nNetwork I/O Statistics:")
    print(f"  Bytes Sent: {net_io.bytes_sent / (1024**3):.2f} GB")
    print(f"  Bytes Received: {net_io.bytes_recv / (1024**3):.2f} GB")
    print(f"  Packets Sent: {net_io.packets_sent}")
    print(f"  Packets Received: {net_io.packets_recv}")
    print(f"  Errors In: {net_io.errin}")
    print(f"  Errors Out: {net_io.errout}")
    print(f"  Dropped In: {net_io.dropin}")
    print(f"  Dropped Out: {net_io.dropout}")


def get_process_info():
    """Get top running processes."""
    print_header("TOP PROCESSES (BY CPU USAGE)")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage and display top 5
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    print(f"{'PID':<10} {'Name':<30} {'CPU %':<10}")
    print("-" * 50)
    for proc in processes[:5]:
        print(f"{proc['pid']:<10} {proc['name']:<30} {proc['cpu_percent']:<10.2f}")
    
    print("\nTOP PROCESSES (BY MEMORY USAGE)")
    processes.sort(key=lambda x: x.get('memory_percent', 0) if hasattr(psutil.Process(x['pid']), 'memory_percent') else 0, reverse=True)
    print(f"{'PID':<10} {'Name':<30} {'Memory %':<10}")
    print("-" * 50)
    for proc in processes[:5]:
        try:
            mem_percent = psutil.Process(proc['pid']).memory_percent()
            print(f"{proc['pid']:<10} {proc['name']:<30} {mem_percent:<10.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def get_boot_info():
    """Get system boot information."""
    print_header("SYSTEM BOOT INFORMATION")
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    print(f"Last Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    uptime_seconds = datetime.now().timestamp() - psutil.boot_time()
    uptime_hours = uptime_seconds / 3600
    uptime_days = uptime_hours / 24
    print(f"Uptime: {int(uptime_days)} days, {int(uptime_hours % 24)} hours")


def main():
    """Main entry point for the Logic Lively diagnostics program."""
    print("\n" + "=" * 60)
    print("  Welcome to Logic Lively!")
    print("  Get logistical assistance with your computer systems.")
    print("=" * 60)
    print(f"Diagnostic Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all diagnostics
        get_system_info()
        get_cpu_info()
        get_memory_info()
        get_disk_info()
        get_network_info()
        get_process_info()
        get_boot_info()
        
        print_header("DIAGNOSTICS COMPLETE")
        print("✓ System diagnostics successfully completed!")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during diagnostics: {e}")


if __name__ == "__main__":
    main()
