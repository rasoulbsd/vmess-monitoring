# Vmess Monitoring Script

This script checks the health and latency of multiple Vmess configs and reports their status to Uptime Kuma.

## Features
- Reads a pool of Vmess configs from a JSON file
- Pings each config and parses average latency
- Reports status and ping to Uptime Kuma monitoring

## Setup
1. Clone the repository and enter the directory.
2. Install dependencies:
   ```bash
   pip install -r req.txt
   ```
3. Prepare your `vmess_pool.json` file (see `vmess_pool.example.json` for format).
4. Make sure the `vmessping` binary is present and executable in the project directory.

## Configuration
- **vmess_pool.json**: List of configs, each with:
  - `name`: Friendly name for the config
  - `vmess`: The vmess:// link
  - `url`: The test URL (e.g., https://www.gstatic.com/generate_204)
  - `uptime_kuma_url`: The base Uptime Kuma push URL (without query params)

Example:
```json
[
  {
    "name": "SampleConfig1",
    "vmess": "vmess://example1",
    "url": "https://www.gstatic.com/generate_204",
    "uptime_kuma_url": "http://128.140.83.6:3001/api/push/EXAMPLEKEY1"
  }
]
```

## Usage
Run the monitor script:
```bash
python monitor.py
```

## Notes
- The script will print the result and also notify Uptime Kuma for each config.
- Make sure your Uptime Kuma push URLs are correct and unique per monitor.

## License
MIT