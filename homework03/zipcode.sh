#!/bin/sh

# Globals

URL=https://www.zipcodestogo.com/
CITY=""
STATE=Indiana
CITYBOOL=0

# Functions

usage() {
    cat 1>&2 <<EOF
Usage: $(basename $0)

-c      CITY    Which city to search
-s      STATE   Which state to search (Indiana)

If no CITY is specified, then all the zip codes for the STATE are displayed.
EOF
  exit $1
}

state()
{
  curl -s $URL$STATE/ | grep -Eo '[0-9]{5}</a' | sed -e 's/<\/a//' | sort | uniq
}

city()
{
  curl -s $URL$STATE/ | grep -E "/$CITY/" | grep -Eo '/[0-9]{5}/' | sed 's/\///' | sed 's/\///' | sort | uniq
}
# Parse Command Line Options

while [ $# -gt 0 ]; do
    case $1 in
    -h) usage 0;;
    -c) CITY=$2;
        CITYBOOL=1;;
    -s) STATE=$(echo $2 | sed 's/\s/%20/');;
     *) usage 0;;
    esac
    shift
    shift
done

# Filter Pipeline(s)

if [ $CITYBOOL -eq 0 ]; then
  echo "$(state)"
else
  echo "$(city)"
fi
