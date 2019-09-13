packet_loss=`ping $1 -w 4 | grep -e "packet loss" | awk '{ print $6; exit}'`
if [ "$packet_loss" == "100%" ]
then
    echo "FAILED Server 1 can't connect to server 2"
else
    echo "PASSED with $packet_loss packet loss"
fi
