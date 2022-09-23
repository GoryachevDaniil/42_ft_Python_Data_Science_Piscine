#/bin/sh

UNIQUE_DATES=$(cat $"../ex03/hh_positions.csv" \
                | tail -n +2 \
                | awk 'BEGIN{FS=",\""} {split($2, result, "T"); print result[1];}' \
                | sort \
                | uniq \
              )

mkdir -p "splitted"

for date in $UNIQUE_DATES
do
  MY_FILE=""splitted"/"created_at_"$date.csv"
  touch $MY_FILE
  
  cat $"../ex03/hh_positions.csv" \
    | head -n 1 \
    > $MY_FILE

  cat $"../ex03/hh_positions.csv" \
    | tail -n +2 \
    | awk -v date=$date \
      'BEGIN{FS=OFS=","}
      {
        i = index($2, date);
        if (i > 0)
        {
          print $0;
        }
      }' \
    >> $MY_FILE
done