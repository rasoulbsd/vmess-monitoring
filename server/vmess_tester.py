import subprocess
import re
from .config import Config


def parse_avg_ping(output):
    """Parse average ping from vmessping output"""
    # Try to find avg ping from output (look for 'rtt min/avg/max' or 
    # 'avg = ... ms')
    # Example: rtt min/avg/max/mdev = 1.23/4.56/7.89/0.12 ms
    match = re.search(
        r"rtt min/avg/max(?:/mdev)? = [^/]+/([^/]+)/",
        output
    )
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    # Try another pattern: avg = ... ms
    match = re.search(r"avg\s*=\s*([\d.]+)", output)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return 0.0


def parse_vmess_info(output):
    """Parse VMess connection information from output"""
    info = {}
    
    # Parse connection details
    patterns = {
        'network': r'Net:\s*(\w+)',
        'address': r'Addr:\s*([^\n]+)',
        'port': r'Port:\s*(\d+)',
        'uuid': r'UUID:\s*([a-f0-9-]+)',
        'type': r'Type:\s*(\w+)',
        'tls': r'TLS:\s*([^\n]*)',
        'path': r'PS:\s*([^\n]+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            info[key] = match.group(1).strip()
    
    return info


def parse_ping_statistics(output):
    """Parse ping statistics from output"""
    stats = {}
    
    # Parse individual ping results
    ping_results = re.findall(
        r'Ping.*?seq=(\d+).*?time=(\d+) ms', output
    )
    if ping_results:
        stats['pings'] = []
        for seq, time in ping_results:
            stats['pings'].append({
                'sequence': int(seq),
                'time_ms': int(time)
            })
    
    # Parse summary statistics
    summary_match = re.search(r'(\d+) requests made, (\d+) success', output)
    if summary_match:
        stats['total_requests'] = int(summary_match.group(1))
        stats['successful_requests'] = int(summary_match.group(2))
        stats['failed_requests'] = stats['total_requests'] - stats['successful_requests']
    
    # Parse RTT statistics
    rtt_match = re.search(
        r'rtt min/avg/max(?:/mdev)? = ([\d.]+)/([\d.]+)/([\d.]+)', 
        output
    )
    if rtt_match:
        stats['rtt'] = {
            'min_ms': float(rtt_match.group(1)),
            'avg_ms': float(rtt_match.group(2)),
            'max_ms': float(rtt_match.group(3))
        }
    
    return stats


def test_vmess_connection(vmess_link, dest_url=None):
    """
    Test a VMess connection
    
    Args:
        vmess_link (str): The VMess link to test
        dest_url (str): Destination URL to test against (optional)
    
    Returns:
        dict: Structured test results with detailed information
    """
    if not dest_url:
        dest_url = Config.DEFAULT_DEST_URL
    
    try:
        result = subprocess.run(
            [
                Config.VMESSPING_BIN,
                "-c",
                str(Config.MAX_PING),
                "-i",
                str(Config.INTERVAL),
                "-dest",
                dest_url,
                vmess_link,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
        )
        output = result.stdout.decode()
        
        # Check if test was successful
        success = "latency" in output.lower() or "avg" in output.lower()
        
        # Parse detailed information
        vmess_info = parse_vmess_info(output)
        ping_stats = parse_ping_statistics(output)
        avg_ping = parse_avg_ping(output)
        
        return {
            'success': success,
            'connection_info': vmess_info,
            'ping_statistics': ping_stats,
            'summary': {
                'average_ping_ms': avg_ping,
                'destination_url': dest_url,
                'test_duration_seconds': 20,  # timeout value
                'packets_sent': ping_stats.get('total_requests', 0),
                'packets_received': ping_stats.get('successful_requests', 0),
                'packet_loss_percent': (
                    (ping_stats.get('failed_requests', 0) / 
                     max(ping_stats.get('total_requests', 1), 1)) * 100
                )
            },
            'raw_output': output
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Test timed out after 20 seconds',
            'summary': {
                'average_ping_ms': 0.0,
                'destination_url': dest_url,
                'test_duration_seconds': 20,
                'packets_sent': 0,
                'packets_received': 0,
                'packet_loss_percent': 100.0
            },
            'raw_output': 'Test timed out'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'summary': {
                'average_ping_ms': 0.0,
                'destination_url': dest_url,
                'test_duration_seconds': 0,
                'packets_sent': 0,
                'packets_received': 0,
                'packet_loss_percent': 100.0
            },
            'raw_output': str(e)
        } 