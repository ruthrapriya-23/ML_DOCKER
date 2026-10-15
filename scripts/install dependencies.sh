
#!/bin/bash
set -e

dnf install -y docker
systemctl enable --now docker

docker --version
