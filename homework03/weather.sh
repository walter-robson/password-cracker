#!/bin/sh

# Globals

URL="https://forecast.weather.gov/zipcity.php?inputstring"
ZIPCODE=46556
FORECAST=0
CELSIUS=0

# Functions

usage() {
    cat 1>&2 <<EOF
Usage: $(basename $0) [zipcode]

-c    Use Celsius degrees instead of Fahrenheit for temperature
-f    Display forecast text

If zipcode is not provided, then it defaults to $ZIPCODE.
EOF
    exit $1
}

weather_information() {
    # Fetch weather information from URL based on ZIPCODE
    curl -sL $URL=$ZIPCODE
}

temperature() {
    # Extract temperature information from weather source
    if [ $CELSIUS -eq 1 ]; then
    weather_information | grep -Eo 'sm">[0-9|-].*&deg;C' | sed 's/sm">//' | sed 's/&deg;C//'
    else
    weather_information | grep -Eo 'lrg">[0-9|-].*&deg;F' | sed 's/lrg">//' | sed 's/&deg;F//'
    fi
}

forecast() {
    # Extract forecast information from weather source
    if [ $FORECAST -eq 1 ]; then
    weather_information | grep -Eo '"myforecast-current">.*' | sed 's/"myforecast-current">//' | sed 's/<\/p>//' | sed 's/\s//'
  fi
}

# Parse Command Line Options

while [ $# -gt 0 ]; do
    case $1 in
        -h) usage 0;;
        -c) CELSIUS=1;;
        -f) FORECAST=1;;
        -*) usage 1;;
        *) ZIPCODE=$1;;
    esac
    shift
done

# Display Information
if [ $FORECAST -eq 1 ]; then
echo "Forecast:    $(forecast)"
fi
echo "Temperature: $(temperature) degrees"
