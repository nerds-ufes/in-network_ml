#!/bin/bash

#http://lists.p4.org/pipermail/p4-dev_lists.p4.org/2017-July/002874.html
#https://sandilands.info/sgordon/segmentation-offloading-with-wireshark-and-ethtool
main()
{
		
	INTERFACES="e1-eth1 e1-eth2 e1-eth3 s1-eth1 s1-eth2 e2-eth1 e2-eth2 e2-eth3 s2-eth1 s2-eth2 s2-eth3"

	for INTERFACE in $INTERFACES
	do
		TOE_OPTIONS="rx tx sg tso ufo gso gro lro rxvlan txvlan rxhash"
		for TOE_OPTION in $TOE_OPTIONS; do
			ethtool --offload "$INTERFACE" "$TOE_OPTION" off &> /dev/null
		done
		ifconfig "$INTERFACE" down
		ifconfig "$INTERFACE" up
	done
	
	
}

main "$@"
