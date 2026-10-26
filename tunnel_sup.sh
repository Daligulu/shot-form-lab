#!/bin/bash
URLFILE=/home/agentuser/shotform/CURRENT_URL
LOG=/home/agentuser/shotform/tunnel_live.log
while true; do
  rm -f "$LOG"
  ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o TCPKeepAlive=yes -R 80:127.0.0.1:8791 nokey@localhost.run > "$LOG" 2>&1 &
  SSHPID=$!
  NEW=""
  for i in $(seq 1 25); do
    sleep 1
    NEW=$(grep -o 'https://[a-z0-9]*\.lhr\.life' "$LOG" 2>/dev/null | head -1)
    [ -n "$NEW" ] && break
  done
  if [ -n "$NEW" ]; then
    echo "$NEW" > "$URLFILE"
    echo "$(date +%T) up: $NEW"
    wait $SSHPID
  else
    kill $SSHPID 2>/dev/null
    echo "$(date +%T) no url, retry"
    sleep 5
  fi
  echo "$(date +%T) down, reconnect"
  sleep 3
done
