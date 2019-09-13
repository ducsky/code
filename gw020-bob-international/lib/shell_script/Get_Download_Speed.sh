output=`tail -n 1 speed.txt`
 
if echo "$output" | grep 'Done' ; then
  DL2=`cat speed.txt | grep -e receiver | awk '{print $7; exit}'`
else
  if (echo "$output" | grep 'Connection refused') || [ "$output" == "" ] ; then
      echo "LOST CONNECTION: IPERF CLIENT CAN'T CONNECT TO SERVER CLIENT"
      DL2=0
  else
      DL2=`cat speed.txt | tail -n +4 | awk '{x+=$7; next} END{print x/NR}'`
  fi
fi
echo -e "$DL2"