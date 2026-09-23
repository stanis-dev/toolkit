#!/bin/sh
# Start the issues page server if it is not already running. Idempotent. Its output, POSTs, errors and whatever a
# runner prints, goes to serve.log next to it.
cd "$(dirname "$0")" || exit 1
if curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8489/index.html | grep -q 200; then
  echo "serving http://127.0.0.1:8489/"; exit 0
fi
nohup python3 ./serve.py 8489 >>serve.log 2>&1 &
sleep 0.5
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8489/index.html | grep -q 200 && echo "serving http://127.0.0.1:8489/" || { echo "failed to start on 8489"; exit 1; }
