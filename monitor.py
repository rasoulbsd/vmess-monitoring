import subprocess
import json
import requests
import re

VMESSPING_BIN = "./vmessping"
MAX_PING = 5
INTERVAL = 2


def parse_avg_ping(output):
    # Try to find avg ping from output (look for 'rtt min/avg/max' or 'avg = ... ms')
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


def test_vmess(link, dest_url):
    try:
        result = subprocess.run(
            [
                VMESSPING_BIN,
                "-c",
                str(MAX_PING),
                "-i",
                str(INTERVAL),
                "-dest",
                dest_url,
                link,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
        )
        output = result.stdout.decode()
        if "latency" in output.lower() or "avg" in output.lower():
            avg_ping = parse_avg_ping(output)
            return True, output, avg_ping
        return False, output, 0.0
    except Exception as e:
        return False, str(e), 0.0


def notify_uptime_kuma(base_url, status, msg, ping=None):
    params = {"status": status, "msg": msg}
    if ping is not None:
        params["ping"] = ping
    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(f"Uptime Kuma notified: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Failed to notify Uptime Kuma: {e}")


def main():
    with open("vmess_pool.json", "r") as f:
        configs = json.load(f)

    for idx, entry in enumerate(configs):
        name = entry.get("name", f"Config #{idx+1}")
        link = entry["vmess"]
        dest_url = entry["url"]
        uptime_kuma_url = entry["uptime_kuma_url"]
        print(f"\n🔍 Checking {name}...")
        print(f"Uptime Kuma URL: {uptime_kuma_url}")
        success, log, avg_ping = test_vmess(link, dest_url)
        if success and avg_ping > 0:
            print("✅ SUCCESS")
            print(f"Avg ping: {avg_ping} ms")
            notify_uptime_kuma(uptime_kuma_url, "up", "OK", avg_ping)
        else:
            print("❌ FAILED")
            notify_uptime_kuma(uptime_kuma_url, "down", "NotOK")
        print(log)


if __name__ == "__main__":
    main()