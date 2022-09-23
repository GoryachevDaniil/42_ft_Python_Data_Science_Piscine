#/bin/sh

cat "../ex01/hh.csv" | head -n 1 \
                      > hh_sorted.csv

cat "../ex01/hh.csv" | tail -n +2 \
                      | sort --field-separator=',' -k 2,2 -k 1,1 \
                      >> hh_sorted.csv
