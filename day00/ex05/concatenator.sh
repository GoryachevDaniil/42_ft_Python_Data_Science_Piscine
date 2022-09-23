#/bin/sh

FILE_LIST=($(ls "splitted"/"created_at_"*".csv"))

cat ${FILE_LIST[0]} | head -n 1 > "./hh_positions.csv"

for file in ${FILE_LIST[@]}
do
  cat $file | tail -n +2 >> "./hh_positions.csv"
done