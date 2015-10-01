#!/bin/sh
sed -i '/proto_run_command/i username=`echo -e "$username"`' /lib/netifd/proto/ppp.sh
sed -i '/proto_run_command/i password=`echo -e "$password"`' /lib/netifd/proto/ppp.sh
