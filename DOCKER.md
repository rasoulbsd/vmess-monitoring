# Docker Setup for VMess Monitoring

Simple Docker configuration for running the VMess monitoring server.

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run**:
   ```bash
   docker-compose up -d
   ```

2. **View logs**:
   ```bash
   docker-compose logs -f
   ```

3. **Stop the service**:
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t vmess-monitoring .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name vmess-monitoring \
     -p 8000:8000 \
     -e API_KEY=your-secret-api-key \
     -e USERNAME=admin \
     -e PASSWORD=your-password \
     vmess-monitoring
   ```

## Configuration

### Environment Variables

You can configure the server using environment variables:

```bash
# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False

# Authentication
API_KEY=your-secret-api-key-here
USERNAME=admin
PASSWORD=your-secure-password-here

# VMess testing
VMESSPING_BIN=./vmessping
MAX_PING=5
INTERVAL=2
DEFAULT_DEST_URL=https://www.gstatic.com/generate_204
```

### Using .env file

1. Copy the example:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your settings

3. Run with docker-compose (automatically loads .env)

## API Usage

Once running, test the API:

```bash
# Health check
curl http://localhost:8000/health

# Test VMess connection
curl -X POST http://localhost:8000/api/test-vmess \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{"vmess_link": "vmess://your-link-here"}'
```

## Troubleshooting

### Check container status
```bash
docker-compose ps
```

### View logs
```bash
docker-compose logs vmess-monitoring
```

### Access container shell
```bash
docker-compose exec vmess-monitoring bash
```

### Rebuild after changes
```bash
docker-compose up -d --build
``` 