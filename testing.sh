#!/bin/bash

# Play agent against specified program 100 times
# Example:
# ./playpy.sh lookt 12345

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <player> <port>" >&2
  exit 1
fi

# p is the port number
p=11300
i=0
while ((i < 100))
do
  ./servt -p $p & sleep 0.1
  ./agent.py -p $p & sleep 0.1
  ./$1    -p $p
  ((p++))
  ((i++))
done 
