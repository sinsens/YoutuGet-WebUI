p=`netstat -lnp|grep 8081|awk '{print $7}'`
pid=${p%/*}
echo "Stop process pid:" ${pid}
kill ${pid}
netstat -lnp|grep 8081

