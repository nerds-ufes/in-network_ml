/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;

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
header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}
header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length_;
    bit<16> checksum;
}
struct metadata {
    bit<16> dstPort;
    bit<3> class;
}
struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    tcp_t        tcp;
    udp_t        udp;
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
            0x800: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            6: parse_tcp;
            17: parse_udp;
            default: accept;
        }
    }
    state parse_tcp {
        packet.extract(hdr.tcp);
        meta.dstPort = hdr.tcp.dstPort;
        transition accept;
    }
    state parse_udp {
        packet.extract(hdr.udp);
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
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }
    
    action ipv4_forward(egressSpec_t port) {
        standard_metadata.egress_spec = port;
    }
    
    table ipv4_class {
        key = {
            meta.class: exact;
        }
        actions = {
            ipv4_forward;
            drop;
        }
        size = 1024;
        default_action = drop();
    }
    
    apply {
        if (hdr.tcp.dstPort <= 86) 
            if (hdr.tcp.dstPort <= 23) 
                if (hdr.ipv4.totalLen <= 45) 
                    if (hdr.ipv4.flags <= 0) 
                        if (hdr.ipv4.protocol <= 11) 
                            meta.class = 6;
                        else 
                            if (hdr.ipv4.totalLen <= 43) 
                                meta.class = 6;
                            else 
                                meta.class = 0;
                    else 
                        meta.class = 0;
                else 
                    if (hdr.ipv4.totalLen <= 75) 
                        if (hdr.ipv4.flags <= 0) 
                            if (hdr.ipv4.protocol <= 11) 
                                meta.class = 0;
                            else 
                                meta.class = 0;
                        else 
                            meta.class = 0;
                    else 
                        if (hdr.tcp.dstPort <= 21) 
                            meta.class = 7;
                        else 
                            meta.class = 7;
            else 
                if (hdr.ipv4.totalLen <= 50) 
                    if (hdr.tcp.ctrl <= 10) 
                        if (hdr.ipv4.totalLen <= 42) 
                            meta.class = 1;
                        else 
                            meta.class = 6;
                    else 
                        meta.class = 0;
                else 
                    if (hdr.ipv4.totalLen <= 468) 
                        if (hdr.ipv4.totalLen <= 54) 
                            if (hdr.tcp.ctrl <= 9) 
                                meta.class = 0;
                            else 
                                if (hdr.tcp.ctrl <= 18) 
                                    if (hdr.tcp.ctrl <= 16) 
                                        meta.class = 1;
                                    else 
                                        meta.class = 1;
                                else 
                                    meta.class = 1;
                        else 
                            if (hdr.ipv4.totalLen <= 333) 
                                if (hdr.tcp.ctrl <= 9) 
                                    meta.class = 1;
                                else 
                                    if (hdr.tcp.ctrl <= 20) 
                                        meta.class = 0;
                                    else 
                                        if (hdr.ipv4.totalLen <= 302) 
                                            if (hdr.ipv4.totalLen <= 269) 
                                                if (hdr.ipv4.totalLen <= 60) 
                                                    if (hdr.ipv4.totalLen <= 59) 
                                                        if (hdr.ipv4.totalLen <= 57) 
                                                            meta.class = 3;
                                                        else 
                                                            if (hdr.ipv4.totalLen <= 58) 
                                                                meta.class = 6;
                                                            else 
                                                                meta.class = 3;
                                                    else 
                                                        meta.class = 5;
                                                else 
                                                    if (hdr.ipv4.totalLen <= 121) 
                                                        meta.class = 3;
                                                    else 
                                                        if (hdr.ipv4.totalLen <= 238) 
                                                            meta.class = 0;
                                                        else 
                                                            meta.class = 3;
                                            else 
                                                meta.class = 5;
                                        else 
                                            if (hdr.ipv4.totalLen <= 328) 
                                                if (hdr.ipv4.totalLen <= 322) 
                                                    meta.class = 0;
                                                else 
                                                    meta.class = 2;
                                            else 
                                                meta.class = 0;
                            else 
                                if (hdr.ipv4.totalLen <= 434) 
                                    if (hdr.tcp.ctrl <= 24) 
                                        if (hdr.ipv4.totalLen <= 402) 
                                            if (hdr.ipv4.totalLen <= 339) 
                                                if (hdr.ipv4.totalLen <= 338) 
                                                    meta.class = 1;
                                                else 
                                                    meta.class = 2;
                                            else 
                                                meta.class = 1;
                                        else 
                                            if (hdr.ipv4.totalLen <= 408) 
                                                if (hdr.ipv4.totalLen <= 407) 
                                                    if (hdr.ipv4.totalLen <= 403) 
                                                        meta.class = 1;
                                                    else 
                                                        if (hdr.ipv4.totalLen <= 404) 
                                                            meta.class = 1;
                                                        else 
                                                            meta.class = 1;
                                                else 
                                                    meta.class = 4;
                                            else 
                                                if (hdr.ipv4.totalLen <= 430) 
                                                    meta.class = 1;
                                                else 
                                                    if (hdr.ipv4.totalLen <= 432) 
                                                        meta.class = 1;
                                                    else 
                                                        meta.class = 1;
                                    else 
                                        meta.class = 3;
                                else 
                                    if (hdr.ipv4.totalLen <= 435) 
                                        meta.class = 4;
                                    else 
                                        if (hdr.ipv4.totalLen <= 453) 
                                            if (hdr.ipv4.totalLen <= 452) 
                                                if (hdr.ipv4.totalLen <= 438) 
                                                    if (hdr.ipv4.totalLen <= 437) 
                                                        meta.class = 1;
                                                    else 
                                                        meta.class = 0;
                                                else 
                                                    meta.class = 1;
                                            else 
                                                meta.class = 4;
                                        else 
                                            if (hdr.ipv4.totalLen <= 456) 
                                                meta.class = 1;
                                            else 
                                                if (hdr.ipv4.totalLen <= 457) 
                                                    meta.class = 0;
                                                else 
                                                    if (hdr.ipv4.totalLen <= 458) 
                                                        meta.class = 2;
                                                    else 
                                                        if (hdr.ipv4.totalLen <= 465) 
                                                            meta.class = 1;
                                                        else 
                                                            meta.class = 1;
                    else 
                        if (hdr.ipv4.totalLen <= 730) 
                            if (hdr.ipv4.totalLen <= 653) 
                                if (hdr.ipv4.totalLen <= 570) 
                                    if (hdr.ipv4.totalLen <= 500) 
                                        if (hdr.ipv4.totalLen <= 472) 
                                            if (hdr.ipv4.totalLen <= 471) 
                                                meta.class = 0;
                                            else 
                                                meta.class = 2;
                                        else 
                                            if (hdr.ipv4.totalLen <= 499) 
                                                meta.class = 0;
                                            else 
                                                meta.class = 3;
                                    else 
                                        if (hdr.ipv4.totalLen <= 566) 
                                            if (hdr.ipv4.totalLen <= 518) 
                                                if (hdr.ipv4.totalLen <= 511) 
                                                    meta.class = 0;
                                                else 
                                                    meta.class = 2;
                                            else 
                                                if (hdr.ipv4.totalLen <= 540) 
                                                    if (hdr.ipv4.totalLen <= 539) 
                                                        if (hdr.ipv4.totalLen <= 535) 
                                                            if (hdr.ipv4.totalLen <= 530) 
                                                                meta.class = 0;
                                                            else 
                                                                meta.class = 0;
                                                        else 
                                                            if (hdr.ipv4.totalLen <= 536) 
                                                                meta.class = 2;
                                                            else 
                                                                meta.class = 0;
                                                    else 
                                                        meta.class = 0;
                                                else 
                                                    if (hdr.ipv4.totalLen <= 563) 
                                                        meta.class = 2;
                                                    else 
                                                        meta.class = 0;
                                        else 
                                            meta.class = 2;
                                else 
                                    if (hdr.ipv4.totalLen <= 573) 
                                        meta.class = 3;
                                    else 
                                        if (hdr.ipv4.totalLen <= 627) 
                                            meta.class = 0;
                                        else 
                                            meta.class = 0;
                            else 
                                if (hdr.ipv4.totalLen <= 656) 
                                    meta.class = 4;
                                else 
                                    if (hdr.ipv4.totalLen <= 662) 
                                        meta.class = 2;
                                    else 
                                        if (hdr.ipv4.totalLen <= 686) 
                                            meta.class = 0;
                                        else 
                                            meta.class = 2;
                        else 
                            meta.class = 0;
        else 
            if (hdr.tcp.ctrl <= 3) 
                if (hdr.ipv4.flags <= 0) 
                    meta.class = 6;
                else 
                    if (hdr.tcp.ctrl <= 1) 
                        meta.class = 6;
                    else 
                        if (hdr.tcp.dstPort <= 444) 
                            if (hdr.tcp.dstPort <= 137) 
                                if (hdr.tcp.dstPort <= 111) 
                                    meta.class = 0;
                                else 
                                    meta.class = 6;
                            else 
                                meta.class = 0;
                        else 
                            if (hdr.ipv4.totalLen <= 56) 
                                if (hdr.tcp.dstPort <= 44858) 
                                    if (hdr.tcp.dstPort <= 753) 
                                        if (hdr.tcp.dstPort <= 455) 
                                            meta.class = 0;
                                        else 
                                            meta.class = 0;
                                    else 
                                        if (hdr.tcp.dstPort <= 19378) 
                                            meta.class = 6;
                                        else 
                                            if (hdr.tcp.dstPort <= 33884) 
                                                meta.class = 0;
                                            else 
                                                meta.class = 6;
                                else 
                                    meta.class = 0;
                            else 
                                meta.class = 0;
            else 
                if (hdr.tcp.dstPort <= 137) 
                    if (hdr.tcp.dstPort <= 111) 
                        meta.class = 0;
                    else 
                        if (hdr.ipv4.totalLen <= 50) 
                            meta.class = 0;
                        else 
                            if (hdr.ipv4.totalLen <= 136) 
                                meta.class = 6;
                            else 
                                meta.class = 0;
                else 
                    if (hdr.tcp.dstPort <= 2155) 
                        if (hdr.tcp.dstPort <= 751) 
                            if (hdr.ipv4.totalLen <= 43) 
                                if (hdr.ipv4.totalLen <= 40) 
                                    meta.class = 0;
                                else 
                                    meta.class = 0;
                            else 
                                meta.class = 0;
                        else 
                            meta.class = 6;
                    else 
                        meta.class = 0;


        ipv4_class.apply();
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
     apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	      hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
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