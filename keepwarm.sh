#!/bin/bash
while true; do
  sleep 20
  U=$(cat /home/agentuser/shotform/CURRENT_URL 2>/dev/null)
  [ -n "$U" ] && { curl -s -o /dev/null --max-time 8 "$U" & }
done
