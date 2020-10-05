/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_SRCROUTING = 0x1234;

#define MAX_HOPS 3


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
    bit<1>    bos;
    bit<15>  port;
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
    bit<1> apply_sr;
}

struct headers {
    ethernet_t              ethernet;
    srcRoute_t[MAX_HOPS]    srcRoutes;
    ipv4_t                  ipv4;
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
            TYPE_SRCROUTING: accept;
            default: accept;
        }
    }
    

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        meta.apply_sr = 1;
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

    action add_header_0hop (   egressSpec_t port, bit<1> sr, macAddr_t dmac){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

    }


    action add_header_1hop (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoutes[0].setValid();
        hdr.srcRoutes[0].bos = bos0;
        hdr.srcRoutes[0].port = port0;
    }

    action add_header_3hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoutes[0].setValid();
        hdr.srcRoutes[0].bos = bos0;
        hdr.srcRoutes[0].port = port0;

        hdr.srcRoutes[1].setValid();
        hdr.srcRoutes[1].bos = bos1;
        hdr.srcRoutes[1].port = port1;

        hdr.srcRoutes[2].setValid();
        hdr.srcRoutes[2].bos = bos2;
        hdr.srcRoutes[2].port = port2;

    }

    table tunnel_encap_process_sr {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            add_header_0hop;
            add_header_1hop;
            add_header_3hops;
            tdrop;
        }
        size = 1024;
        default_action = tdrop();
    }    

    apply {
        tunnel_encap_process_sr.apply();
        if(meta.apply_sr!=1){
            hdr.srcRoutes[0].setInvalid();
            hdr.srcRoutes[1].setInvalid();
            hdr.srcRoutes[2].setInvalid();
        }else{
            hdr.ethernet.etherType = TYPE_SRCROUTING;
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
    
    action srcRoute_finish() {
        hdr.ethernet.etherType = TYPE_IPV4;
        hdr.srcRoutes[0].setInvalid();
        hdr.srcRoutes[1].setInvalid();
        hdr.srcRoutes[2].setInvalid();
    }

    apply {
        
    	if (hdr.ipv4.isValid() && hdr.ethernet.etherType != TYPE_SRCROUTING) {
            process_tunnel_encap.apply(hdr, meta, standard_metadata);
        } else if (hdr.ethernet.etherType == TYPE_SRCROUTING) {
            srcRoute_finish();
            // deliver to default VM port
            standard_metadata.egress_spec = 2;
		}
    
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
        packet.emit(hdr.srcRoutes);
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
