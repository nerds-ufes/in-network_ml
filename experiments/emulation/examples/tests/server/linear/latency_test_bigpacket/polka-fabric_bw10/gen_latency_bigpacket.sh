#!/bin/bash

SAMPLES=1
DELAY=80

main()
{
	declare -a arr=("10.0.1.11" "10.0.2.2" "10.0.3.3" "10.0.4.4" "10.0.5.5" "10.0.6.6" "10.0.7.7" "10.0.8.8" "10.0.9.9" "10.0.10.10")
	declare -i it=0
	for ip in "${arr[@]}"
	do
		echo "IP $ip"
		mkdir "$it"
		cd "$it"
		rm -rf *
		for i in `seq $SAMPLES`
		do
			echo "Starting: Ping $i"
			ping -c 65 -s 1200 $ip > ping.log &
			sleep $DELAY
			echo "Ending: Ping $i"
			killall ping 2>/dev/null
			cat ping.log | head -n -4 | tail -n +2 | cut -d ' ' -f 7 | sed 's/time=//g' > a${i}_${it};
			#rm ping.log
		done
		cd ..
		it=it+1
	done
	
	
}

main "$@"
