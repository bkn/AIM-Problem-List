#!/bin/sh -e
module=$1
if [ -z "$module" ]; then
  echo "Usage: $0 modulename"
  exit 1
fi
# kills the dummy backend
kill `ps ax | grep "$module/run.py" | head -1 | awk '{print $1}'`
