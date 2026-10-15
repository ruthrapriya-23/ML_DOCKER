
#!/bin/bash

docker stop ml-iris-app 2>/dev/null || true
docker rm ml-iris-app 2>/dev/null || true
exit 0
