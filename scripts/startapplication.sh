
#!/bin/bash
set -e

cd /opt/ml-docker-aws

docker build -t ml-iris-app:latest .

docker rm -f ml-iris-app 2>/dev/null || true

docker run -d \
  --name ml-iris-app \
  --restart unless-stopped \
  -p 5000:5000 \
  ml-iris-app:latest

# Wait for the application to start
for i in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:5000/health; then
    echo "ML application started successfully"
    exit 0
  fi
  sleep 2
done

echo "ML application health check failed"
docker logs ml-iris-app
exit 1
