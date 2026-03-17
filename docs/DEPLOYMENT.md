# Production Deployment Guide

## Overview

This guide covers deploying Endee RAG System to production environments.

## Pre-Deployment Checklist

- [ ] Environment variables configured securely
- [ ] CORS settings restricted to allowed domains
- [ ] SSL/TLS certificates obtained
- [ ] Database backups configured
- [ ] Monitoring and logging setup
- [ ] Rate limiting enabled
- [ ] API authentication implemented
- [ ] Security audit completed

## Environment Setup

### Secure Configuration

```bash
# .env.production
OPENAI_API_KEY=sk-...  # Use secrets manager in production
ENDEE_URL=https://endee.yourdomain.com
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=WARNING

# Security
CORS_ORIGINS=["https://yourdomain.com"]
ALLOWED_HOSTS=["yourdomain.com"]
SESSION_TIMEOUT=3600
```

### Secrets Management

Using environment variables (recommended):
```bash
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id openai-api-key \
  --query SecretString --output text)
```

Or use HashiCorp Vault:
```bash
vault kv get secret/endee/openai-key
```

## Deployment Methods

### Docker Deployment

#### Single Server

```bash
# 1. Setup server
ssh user@your-server.com
git clone https://github.com/abhishek-p-r/endee.git
cd endee

# 2. Create .env with production values
cp .env.example .env.production
# Edit with production settings

# 3. Build and run
docker-compose -f docker-compose.yml up -d

# 4. Verify
curl https://your-domain.com/health
```

#### Multiple Servers (Load Balanced)

```yaml
# docker-compose-production.yml
version: '3.8'

services:
  backend-1:
    image: endee-backend:latest
    environment:
      - INSTANCE_ID=1
    labels:
      - "traefik.http.services.backend.loadbalancer.server.port=8000"
      - "traefik.http.routers.backend.rule=Host(`api.yourdomain.com`)"

  backend-2:
    image: endee-backend:latest
    environment:
      - INSTANCE_ID=2
    labels:
      - "traefik.http.services.backend.loadbalancer.server.port=8000"

  traefik:
    image: traefik:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./traefik.yml:/traefik.yml
      - /var/run/docker.sock:/var/run/docker.sock
```

### Kubernetes Deployment

#### Setup

```bash
# 1. Create namespace
kubectl create namespace endee

# 2. Create secrets
kubectl create secret generic openai-secret \
  --from-literal=api-key=$OPENAI_API_KEY \
  -n endee

# 3. Apply deployments
kubectl apply -f k8s/deployment.yml -n endee
```

#### Deployment YAML

```yaml
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: endee-backend
  namespace: endee
spec:
  replicas: 3
  selector:
    matchLabels:
      app: endee-backend
  template:
    metadata:
      labels:
        app: endee-backend
    spec:
      containers:
      - name: backend
        image: endee-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: ENDEE_URL
          value: "http://endee-db:8001"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Cloud Platforms

#### AWS Deployment

Using ECS:
```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name endee-backend

# 2. Build and push image
docker build -t endee-backend .
docker tag endee-backend:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/endee-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/endee-backend:latest

# 3. Create ECS task definition
# 4. Create ECS service
# 5. Setup ALB and autoscaling
```

#### Google Cloud Deployment

Using Cloud Run:
```bash
# 1. Build image
gcloud builds submit --tag gcr.io/PROJECT/endee-backend

# 2. Deploy
gcloud run deploy endee-backend \
  --image gcr.io/PROJECT/endee-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
```

#### Azure Deployment

Using Container Instances:
```bash
# 1. Create container group
az container create \
  --resource-group myResourceGroup \
  --name endee-backend \
  --image endee-backend:latest \
  --environment-variables OPENAI_API_KEY=$OPENAI_API_KEY
```

## Web Server Configuration

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/endee
upstream endee_backend {
    server localhost:8000;
}

upstream endee_frontend {
    server localhost:8501;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://endee_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name app.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://endee_frontend;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Apache Configuration

```apache
# /etc/apache2/sites-available/endee.conf
<VirtualHost *:443>
    ServerName api.yourdomain.com
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    ProxyPreserveHost On
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
    
    Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-Content-Type-Options "nosniff"
</VirtualHost>
```

## Database Setup

### Endee Vector Database

#### Self-Hosted

```bash
# Production Dockerfile for Endee
FROM endeeio/endee:latest

# Run with persistent volume
docker run -d \
  --name endee-db \
  -p 8001:8001 \
  -v endee-data:/var/lib/endee \
  endeeio/endee:latest

# Backup
docker exec endee-db endee-backup > backup.tar.gz

# Restore
docker exec endee-db endee-restore < backup.tar.gz
```

#### Cloud Hosted

Visit https://www.endee.io/ for managed hosting options.

## Monitoring & Logging

### Prometheus Metrics

```python
# backend/app.py
from prometheus_client import Counter, Histogram, generate_latest

query_counter = Counter('endee_queries_total', 'Total queries')
response_time = Histogram('endee_response_time', 'Response time')

@app.post("/api/query/ask")
async def ask_question(request):
    query_counter.inc()
    # ... query logic ...
```

Access metrics at: `/metrics`

### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
# docker-compose-monitoring.yml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
  
  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
```

### Datadog Integration

```python
from datadog import initialize, api

options = {
    'api_key': 'YOUR_API_KEY',
    'app_key': 'YOUR_APP_KEY'
}

initialize(**options)

# Track events
api.Event.create(
    title="Query Processed",
    text="User query completed",
    tags=['endee', 'query']
)
```

## Security

### API Authentication

```python
# backend/app.py
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/api/query/ask")
async def ask_question(
    request: QuestionRequest,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Validate API key
    if credentials.credentials != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # ... process query ...
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/query/ask")
@limiter.limit("100/minute")
async def ask_question(request):
    pass
```

### SSL/TLS

```bash
# Get certificates from Let's Encrypt
sudo certbot certonly --standalone -d yourdomain.com

# Renew automatically
sudo certbot renew --quiet
```

## Performance Optimization

### Database Optimization

```bash
# Enable connection pooling
# In backend/config.py
DB_POOL_SIZE = 20
DB_POOL_TIMEOUT = 30

# Enable caching
REDIS_URL = "redis://localhost:6379"
CACHE_TTL = 3600
```

### CDN Configuration

Use CloudFlare or AWS CloudFront for:
- Static assets
- API response caching
- DDoS protection

## Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh - Daily backup script

BACKUP_DIR="/backups/endee"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup Endee data
docker exec endee-db endee-backup > \
  "$BACKUP_DIR/endee_$DATE.tar.gz"

# Upload to S3
aws s3 cp "$BACKUP_DIR/endee_$DATE.tar.gz" \
  s3://my-backups/endee/

# Keep only 30 days of backups
find $BACKUP_DIR -mtime +30 -delete
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh
```

## Maintenance

### Health Monitoring

```bash
# Check health regularly
while true; do
  curl https://api.yourdomain.com/health
  sleep 60
done
```

### Log Rotation

```bash
# /etc/logrotate.d/endee
/var/log/endee/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 nobody nobody
    sharedscripts
}
```

### Database Maintenance

```bash
# Regular optimization
docker exec endee-db endee-optimize

# Vacuum and reindex
docker exec endee-db endee-maintenance
```

## Troubleshooting Production Issues

### High CPU Usage
- Check for slow queries
- Implement query timeouts
- Use read replicas

### Memory Leaks
- Monitor container memory
- Restart services periodically
- Use memory profiler

### Database Issues
- Monitor connection pool
- Check disk space
- Verify backups running

## Support

For production support:
- Email: support@endeeai.com
- GitHub Issues: https://github.com/abhishek-p-r/endee/issues
- Documentation: https://github.com/abhishek-p-r/endee/wiki
