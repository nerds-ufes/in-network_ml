#!/bin/bash

SAMPLES=3
DELAY=10

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
			echo "Starting: Iperf $i: h1 to $ip"
			iperf -c $ip -M 1200 -n 100000000 -yc 2> /dev/null >>fct.log
			sleep $DELAY
			#echo "Ending: Iperf $i"
			#killall iperf 2>/dev/null			
		done
		cat fct.log | cut -d ',' -f 7 | cut -d '-' -f 2 >> a1_${it};
		cd ..
		it=it+1
	done
	
	
}

main "$@"
