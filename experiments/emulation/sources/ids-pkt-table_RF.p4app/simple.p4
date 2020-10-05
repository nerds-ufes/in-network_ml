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
header arr_t{
    bit<16> p;
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
    bit<9> rf1;
    bit<9> rf2;
    bit<9> rf3;
    bit<9> rf4;
    bit<9> rf5;

    bit<9> rf1_port;
    bit<9> rf2_port;
    bit<9> rf3_port;
    bit<9> rf4_port;
    bit<9> rf5_port;
    arr_t[9] rf_port;
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
    
    action sum_class(bit<9> clazz) {
        if (clazz == 2) meta.rf_port[2].p = meta.rf_port[2].p + 1;
        else if (clazz == 3) meta.rf_port[3].p = meta.rf_port[3].p + 1;
        else if (clazz == 4) meta.rf_port[4].p = meta.rf_port[4].p + 1;
        else if (clazz == 5) meta.rf_port[5].p = meta.rf_port[5].p + 1;
        else if (clazz == 6) meta.rf_port[6].p = meta.rf_port[6].p + 1;
        else if (clazz == 7) meta.rf_port[7].p = meta.rf_port[7].p + 1;
        else if (clazz == 8) meta.rf_port[8].p = meta.rf_port[8].p + 1;
    }    

    action ipv4_forward(egressSpec_t port) {
        standard_metadata.egress_spec = port;
    }
    action rf1(bit<9> clazz) {
        meta.rf1_port = clazz;
        sum_class(clazz);
    }
    action rf2(bit<9> clazz) {
        meta.rf2_port = clazz;
        sum_class(clazz);
    }
    action rf3(bit<9> clazz) {
        meta.rf3_port = clazz;
        sum_class(clazz);
    }
    action rf4(bit<9> clazz) {
        meta.rf4_port = clazz;
        sum_class(clazz);
    }
    action rf5(bit<9> clazz) {
        meta.rf5_port = clazz;
        sum_class(clazz);
    }
    
    table tbl_rf1 {
        key = {
            hdr.ethernet.etherType: range;
            hdr.ipv4.protocol: range;
            hdr.ipv4.flags: range;
            hdr.ipv4.totalLen: range;
            hdr.tcp.dstPort: range;
            hdr.tcp.ctrl: range;
            hdr.tcp.ecn: range;
            hdr.udp.dstPort: range;
        }
        actions = {
            rf1;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }
    table tbl_rf2 {
        key = {
            hdr.ethernet.etherType: range;
            hdr.ipv4.protocol: range;
            hdr.ipv4.flags: range;
            hdr.ipv4.totalLen: range;
            hdr.tcp.dstPort: range;
            hdr.tcp.ctrl: range;
            hdr.tcp.ecn: range;
            hdr.udp.dstPort: range;
        }
        actions = {
            rf2;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }    
    table tbl_rf3 {
        key = {
            hdr.ethernet.etherType: range;
            hdr.ipv4.protocol: range;
            hdr.ipv4.flags: range;
            hdr.ipv4.totalLen: range;
            hdr.tcp.dstPort: range;
            hdr.tcp.ctrl: range;
            hdr.tcp.ecn: range;
            hdr.udp.dstPort: range;
        }
        actions = {
            rf3;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }    
    table tbl_rf4 {
        key = {
            hdr.ethernet.etherType: range;
            hdr.ipv4.protocol: range;
            hdr.ipv4.flags: range;
            hdr.ipv4.totalLen: range;
            hdr.tcp.dstPort: range;
            hdr.tcp.ctrl: range;
            hdr.tcp.ecn: range;
            hdr.udp.dstPort: range;
        }
        actions = {
            rf4;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }    
    table tbl_rf5 {
        key = {
            hdr.ethernet.etherType: range;
            hdr.ipv4.protocol: range;
            hdr.ipv4.flags: range;
            hdr.ipv4.totalLen: range;
            hdr.tcp.dstPort: range;
            hdr.tcp.ctrl: range;
            hdr.tcp.ecn: range;
            hdr.udp.dstPort: range;
        }
        actions = {
            rf5;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }    
        
    table tbl_rf {
        key = {
            meta.rf1: exact;
            meta.rf2: exact;
            meta.rf3: exact;
            meta.rf4: exact;
            meta.rf5: exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }    

    apply {
        tbl_rf1.apply();
        tbl_rf2.apply();
        tbl_rf3.apply();
        tbl_rf4.apply();
        tbl_rf5.apply();

        if      (meta.rf_port[2].p > meta.rf_port[3].p && meta.rf_port[2].p > meta.rf_port[4].p && meta.rf_port[2].p > meta.rf_port[5].p && meta.rf_port[2].p > meta.rf_port[6].p && meta.rf_port[2].p > meta.rf_port[7].p && meta.rf_port[2].p > meta.rf_port[8].p) {standard_metadata.egress_spec = 2;}
        else if (meta.rf_port[3].p > meta.rf_port[2].p && meta.rf_port[3].p > meta.rf_port[4].p && meta.rf_port[3].p > meta.rf_port[5].p && meta.rf_port[3].p > meta.rf_port[6].p && meta.rf_port[3].p > meta.rf_port[7].p && meta.rf_port[3].p > meta.rf_port[8].p) {standard_metadata.egress_spec = 3;}
        else if (meta.rf_port[4].p > meta.rf_port[3].p && meta.rf_port[4].p > meta.rf_port[2].p && meta.rf_port[4].p > meta.rf_port[5].p && meta.rf_port[4].p > meta.rf_port[6].p && meta.rf_port[4].p > meta.rf_port[7].p && meta.rf_port[4].p > meta.rf_port[8].p) {standard_metadata.egress_spec = 4;}
        else if (meta.rf_port[5].p > meta.rf_port[3].p && meta.rf_port[5].p > meta.rf_port[4].p && meta.rf_port[5].p > meta.rf_port[2].p && meta.rf_port[5].p > meta.rf_port[6].p && meta.rf_port[5].p > meta.rf_port[7].p && meta.rf_port[5].p > meta.rf_port[8].p) {standard_metadata.egress_spec = 5;}
        else if (meta.rf_port[6].p > meta.rf_port[3].p && meta.rf_port[6].p > meta.rf_port[4].p && meta.rf_port[6].p > meta.rf_port[5].p && meta.rf_port[6].p > meta.rf_port[2].p && meta.rf_port[6].p > meta.rf_port[7].p && meta.rf_port[6].p > meta.rf_port[8].p) {standard_metadata.egress_spec = 6;}
        else if (meta.rf_port[7].p > meta.rf_port[3].p && meta.rf_port[7].p > meta.rf_port[4].p && meta.rf_port[7].p > meta.rf_port[5].p && meta.rf_port[7].p > meta.rf_port[6].p && meta.rf_port[7].p > meta.rf_port[2].p && meta.rf_port[7].p > meta.rf_port[8].p) {standard_metadata.egress_spec = 7;}
        else if (meta.rf_port[8].p > meta.rf_port[3].p && meta.rf_port[8].p > meta.rf_port[4].p && meta.rf_port[8].p > meta.rf_port[5].p && meta.rf_port[8].p > meta.rf_port[6].p && meta.rf_port[8].p > meta.rf_port[7].p && meta.rf_port[8].p > meta.rf_port[2].p) {standard_metadata.egress_spec = 8;}
        //else if (meta.rf1 == 1 && meta.rf_port[3].p == 1 && meta.rf_port[4].p == 1 && meta.rf_port[5].p == 1 && meta.rf_port[6].p == 1) {standard_metadata.egress_spec = meta.rf2_port;}

        standard_metadata.egress_spec = meta.rf1_port;
        //tbl_rf.apply();
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

        //parsed headers have to be added again into the packet.
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