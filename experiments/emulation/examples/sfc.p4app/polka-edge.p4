/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_SRCROUTING = 0x1234;


//Ethernet frame payload padding and P4
//https://github.com/p4lang/p4-spec/issues/587

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header srcRoute_t {
    bit<160>    routeId;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

struct metadata {
    bit<160>   routeId;
    bit<16>   etherType;
    bit<1> apply_sr;
    bit<9> port;
}

struct polka_t_top {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<160>    routeId;
}

struct headers {
    ethernet_t  ethernet;
    srcRoute_t  srcRoute;
    ipv4_t      ipv4;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            TYPE_SRCROUTING: parse_srcRouting;
            default: accept;
        }
    }
    
    state parse_srcRouting {
        packet.extract(hdr.srcRoute);
        transition accept;
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }


}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**********************  T U N N E L   E N C A P   ************************
*************************************************************************/
control process_tunnel_encap(inout headers hdr,
                            inout metadata meta,
                            inout standard_metadata_t standard_metadata) {
    action tdrop() {
        mark_to_drop();
    }
    
    action srcRoute_finish() {
        hdr.ethernet.etherType = TYPE_IPV4;
        hdr.srcRoute.setInvalid();
    }
    
    action sf_process ( egressSpec_t port){
        standard_metadata.egress_spec = port;
        srcRoute_finish();
    }

    action add_sourcerouting_header (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<160>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute.setValid();
        hdr.srcRoute.routeId = routeIdPacket;
        hdr.ethernet.etherType = TYPE_SRCROUTING;

    }

    table tunnel_encap_process_sr {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            add_sourcerouting_header;
            tdrop;
        }
        size = 1024;
        default_action = tdrop();
    }


    table tunnel_encap_process_sfc {
        key = {            
            hdr.ethernet.dstAddr : exact;
            standard_metadata.ingress_port : exact;
        }
        actions = {
			add_sourcerouting_header;
            tdrop;
        }
        size = 1024;
        default_action = tdrop();
    }
    
    table to_vnf_process_sfc {
        key = {            
            hdr.ethernet.dstAddr : exact;
            standard_metadata.ingress_port : exact;
        }
        actions = {
			sf_process;
            tdrop;
        }
        size = 1024;
        default_action = tdrop();
    } 

    apply {
    
		// Case 1: Packet from VM to edge: match IP dest, add SR header and send to core: tunnel_encap_process_sr.apply()
		// Case 2: Packet from VNF to edge: match inport and MAC dest, add SR header and send to core: tunnel_encap_process_sfc.apply()
		// Case 3: Packet from core to edge with destination VNF: match inport and MAC dest, remove SR header and send to VNF: tunnel_encap_process_sfc.apply()
		// Case 4: Packet from core to edge with destination end host VM: remove SR header and send to VM
		if(hdr.ipv4.isValid() && hdr.ethernet.etherType != TYPE_SRCROUTING){
			// From VM (end host or VNF) to edge
			// Test Case 1
			if(!tunnel_encap_process_sr.apply().hit){
				// Case 2: from VNF
				tunnel_encap_process_sfc.apply();
			}						
		}else{			
			if(hdr.ethernet.etherType == TYPE_SRCROUTING){
				// From core to edge
				// Test Case 3
				if(!(to_vnf_process_sfc.apply().hit)){
					// Case 4: Deliver to end host
					srcRoute_finish();
					standard_metadata.egress_spec = 1;
				}				
			}			
		} 

    }

}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop();
    }

    apply {
        
        process_tunnel_encap.apply(hdr, meta, standard_metadata);
    
    }
}



/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply {  }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.srcRoute);
        packet.emit(hdr.ipv4);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
