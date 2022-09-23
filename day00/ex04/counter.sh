#/bin/sh
INPUT_FILE="../ex03/hh_positions.csv"

echo '"name","count"' > $"hh_uniq_positions.csv"

cat $INPUT_FILE | awk 'BEGIN{FS=OFS=",";} NR>1 {print $3;}' \
                | sort | uniq -c | awk 'BEGIN{OFS=","} {print $2, $1;}' \
                >> $"hh_uniq_positions.csv"