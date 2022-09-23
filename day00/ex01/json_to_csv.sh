#/bin/sh

if [ -z "$1" ]
  then
    cat ../ex00/hh.json | jq -r -f filter.jq > hh.csv
  else
    cat $1 | jq -r -f filter.jq > hh.csv
fi

