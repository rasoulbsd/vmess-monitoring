# VMess Monitoring Web Server

A simple Flask-based web server for testing VMess connections via REST API with authentication.

## Features

- **REST API** for testing VMess connections
- **Multiple authentication methods**: API key and Basic Auth
- **Environment-based configuration**
- **Modular design** for easy maintenance
- **Structured response format** with detailed connection information

## Installation

1. Install dependencies:
```bash
pip install -r server/requirements.txt
```

2. Copy the environment example and configure:
```bash
cp env.example .env
# Edit .env with your settings
```

## Configuration

Edit the `.env` file with your settings:

```env
# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8765
DEBUG=False

# Authentication
API_KEY=your-secret-api-key-here
USERNAME=admin
PASSWORD=your-secure-password-here

# VMess Testing Configuration
VMESSPING_BIN=./vmessping
MAX_PING=5
INTERVAL=2
DEFAULT_DEST_URL=https://www.gstatic.com/generate_204
```

## Running the Server

```bash
# Option 1: Run from server directory
cd server
python run.py

# Option 2: Run from project root
python -m server.run
```

## API Endpoints

### Health Check
- `GET /` - Service status
- `GET /health` - Health check

### Test VMess Connection

#### API Key Authentication
```bash
curl -X POST http://localhost:8765/api/test-vmess \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "vmess_link": "vmess://your-vmess-link-here",
    "dest_url": "https://www.gstatic.com/generate_204"
  }'
```

#### Basic Authentication
```bash
curl -X POST http://localhost:8765/api/test-vmess-basic \
  -H "Content-Type: application/json" \
  -u "admin:your-secure-password-here" \
  -d '{
    "vmess_link": "vmess://your-vmess-link-here",
    "dest_url": "https://www.gstatic.com/generate_204"
  }'
```

#### Flexible Authentication
```bash
curl -X POST http://localhost:8765/api/test-vmess-auth \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "vmess_link": "vmess://your-vmess-link-here",
    "dest_url": "https://www.gstatic.com/generate_204"
  }'
```

## Response Format

The API now returns a structured response with detailed information:

```json
{
  "success": true,
  "connection_info": {
    "network": "ws",
    "address": "rhvpvip1.angrydevs.ir",
    "port": "80",
    "uuid": "8d3b7029-d458-4c27-87b8-166cfd545642",
    "type": "none",
    "tls": "",
    "path": "432080595@RHVP-IR1-DE"
  },
  "ping_statistics": {
    "pings": [
      {"sequence": 1, "time_ms": 1637},
      {"sequence": 2, "time_ms": 1675},
      {"sequence": 3, "time_ms": 1751},
      {"sequence": 4, "time_ms": 1775},
      {"sequence": 5, "time_ms": 1578}
    ],
    "total_requests": 5,
    "successful_requests": 5,
    "failed_requests": 0,
    "rtt": {
      "min_ms": 1578.0,
      "avg_ms": 1683.0,
      "max_ms": 1775.0
    }
  },
  "summary": {
    "average_ping_ms": 1683.0,
    "destination_url": "https://www.gstatic.com/generate_204",
    "test_duration_seconds": 20,
    "packets_sent": 5,
    "packets_received": 5,
    "packet_loss_percent": 0.0
  },
  "raw_output": "vmessping output..."
}
```

### Response Fields

- **`success`**: Boolean indicating if the test was successful
- **`connection_info`**: Parsed VMess connection details
  - `network`: Connection type (ws, tcp, etc.)
  - `address`: Server address
  - `port`: Server port
  - `uuid`: Connection UUID
  - `type`: Connection type
  - `tls`: TLS configuration
  - `path`: Path/PS information
- **`ping_statistics`**: Detailed ping information
  - `pings`: Array of individual ping results
  - `total_requests`: Total packets sent
  - `successful_requests`: Successful responses
  - `failed_requests`: Failed responses
  - `rtt`: Round-trip time statistics (min/avg/max)
- **`summary`**: Test summary
  - `average_ping_ms`: Average ping time
  - `destination_url`: Test destination
  - `test_duration_seconds`: Test duration
  - `packets_sent`: Total packets sent
  - `packets_received`: Successful packets
  - `packet_loss_percent`: Packet loss percentage
- **`raw_output`**: Original vmessping output

## Error Responses

- `400 Bad Request` - Missing required fields
- `401 Unauthorized` - Invalid authentication
- `404 Not Found` - Invalid endpoint
- `500 Internal Server Error` - Server error

## Security Notes

- Change default credentials in `.env`
- Use HTTPS in production
- Keep API keys secure
- Consider rate limiting for production use 