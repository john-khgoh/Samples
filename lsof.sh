#!/bin/sh

DATE=`date +%Y%m%d`
TIME=`date +%H:%M`
FILE=chk_lsof_$DATE.txt
CMD_WLI=`ps -efx | grep java | grep NWLI | awk '{print $2}'`
CMD_WLS=`ps -efx | grep java | grep NWLS | awk '{print $2}'`
OUTPUT_WLI=`/usr/local/bin/lsof -p $CMD_WLI | wc -l`
OUTPUT_WLS=`/usr/local/bin/lsof -p $CMD_WLS | wc -l`

SUM=$OUTPUT_WLI+$OUTPUT_WLS
#SUM1=$(echo "$OUTPUT_WLI+$OUTPUT_WLS"|bc)
#echo "SUM: $SUM1\n"

#echo "$TIME\t\c" >> /tmp/$FILE
#echo "WLI:$OUTPUT_WLI\t\c" >> /tmp/$FILE
#echo "WLS:$OUTPUT_WLS\t" >> /tmp/$FILE

