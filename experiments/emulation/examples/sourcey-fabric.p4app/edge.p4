/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_SRCROUTING = 0x1234;

#define MAX_HOPS 17


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
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoutes[0].setValid();
        hdr.srcRoutes[0].bos = bos0;
        hdr.srcRoutes[0].port = port0;

        hdr.srcRoutes[1].setValid();
        hdr.srcRoutes[1].bos = bos1;
        hdr.srcRoutes[1].port = port1;
    }

    action add_header_2hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
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

    action add_header_3hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

    }

    action add_header_4hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

    }

    action add_header_5hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

    }

    action add_header_6hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

    }

    action add_header_7hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

    }


    action add_header_8hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

    }

    action add_header_9hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

    }

    action add_header_10hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

    }

    action add_header_11hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10,
                                        bit<1> bos11, bit<15> port11){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

        hdr.srcRoutes[11].setValid();
        hdr.srcRoutes[11].bos = bos11;
        hdr.srcRoutes[11].port = port11;

    }

    action add_header_12hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10,
                                        bit<1> bos11, bit<15> port11,
                                        bit<1> bos12, bit<15> port12){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

        hdr.srcRoutes[11].setValid();
        hdr.srcRoutes[11].bos = bos11;
        hdr.srcRoutes[11].port = port11;

        hdr.srcRoutes[12].setValid();
        hdr.srcRoutes[12].bos = bos12;
        hdr.srcRoutes[12].port = port12;

    }

    action add_header_13hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10,
                                        bit<1> bos11, bit<15> port11,
                                        bit<1> bos12, bit<15> port12,
                                        bit<1> bos13, bit<15> port13){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

        hdr.srcRoutes[11].setValid();
        hdr.srcRoutes[11].bos = bos11;
        hdr.srcRoutes[11].port = port11;

        hdr.srcRoutes[12].setValid();
        hdr.srcRoutes[12].bos = bos12;
        hdr.srcRoutes[12].port = port12;

        hdr.srcRoutes[13].setValid();
        hdr.srcRoutes[13].bos = bos13;
        hdr.srcRoutes[13].port = port13;

    }

    action add_header_14hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10,
                                        bit<1> bos11, bit<15> port11,
                                        bit<1> bos12, bit<15> port12,
                                        bit<1> bos13, bit<15> port13,
                                        bit<1> bos14, bit<15> port14){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

        hdr.srcRoutes[11].setValid();
        hdr.srcRoutes[11].bos = bos11;
        hdr.srcRoutes[11].port = port11;

        hdr.srcRoutes[12].setValid();
        hdr.srcRoutes[12].bos = bos12;
        hdr.srcRoutes[12].port = port12;

        hdr.srcRoutes[13].setValid();
        hdr.srcRoutes[13].bos = bos13;
        hdr.srcRoutes[13].port = port13;

        hdr.srcRoutes[14].setValid();
        hdr.srcRoutes[14].bos = bos14;
        hdr.srcRoutes[14].port = port14;

    }

    action add_header_15hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10,
                                        bit<1> bos11, bit<15> port11,
                                        bit<1> bos12, bit<15> port12,
                                        bit<1> bos13, bit<15> port13,
                                        bit<1> bos14, bit<15> port14,
                                        bit<1> bos15, bit<15> port15){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

        hdr.srcRoutes[11].setValid();
        hdr.srcRoutes[11].bos = bos11;
        hdr.srcRoutes[11].port = port11;

        hdr.srcRoutes[12].setValid();
        hdr.srcRoutes[12].bos = bos12;
        hdr.srcRoutes[12].port = port12;

        hdr.srcRoutes[13].setValid();
        hdr.srcRoutes[13].bos = bos13;
        hdr.srcRoutes[13].port = port13;

        hdr.srcRoutes[14].setValid();
        hdr.srcRoutes[14].bos = bos14;
        hdr.srcRoutes[14].port = port14;

        hdr.srcRoutes[15].setValid();
        hdr.srcRoutes[15].bos = bos15;
        hdr.srcRoutes[15].port = port15;
    }
    
    action add_header_16hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<1> bos0, bit<15> port0,
                                        bit<1> bos1, bit<15> port1,
                                        bit<1> bos2, bit<15> port2,
                                        bit<1> bos3, bit<15> port3,
                                        bit<1> bos4, bit<15> port4,
                                        bit<1> bos5, bit<15> port5,
                                        bit<1> bos6, bit<15> port6,
                                        bit<1> bos7, bit<15> port7,
                                        bit<1> bos8, bit<15> port8,
                                        bit<1> bos9, bit<15> port9,
                                        bit<1> bos10, bit<15> port10,
                                        bit<1> bos11, bit<15> port11,
                                        bit<1> bos12, bit<15> port12,
                                        bit<1> bos13, bit<15> port13,
                                        bit<1> bos14, bit<15> port14,
                                        bit<1> bos15, bit<15> port15,
                                        bit<1> bos16, bit<15> port16){

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

        hdr.srcRoutes[3].setValid();
        hdr.srcRoutes[3].bos = bos3;
        hdr.srcRoutes[3].port = port3;

        hdr.srcRoutes[4].setValid();
        hdr.srcRoutes[4].bos = bos4;
        hdr.srcRoutes[4].port = port4;

        hdr.srcRoutes[5].setValid();
        hdr.srcRoutes[5].bos = bos5;
        hdr.srcRoutes[5].port = port5;

        hdr.srcRoutes[6].setValid();
        hdr.srcRoutes[6].bos = bos6;
        hdr.srcRoutes[6].port = port6;

        hdr.srcRoutes[7].setValid();
        hdr.srcRoutes[7].bos = bos7;
        hdr.srcRoutes[7].port = port7;

        hdr.srcRoutes[8].setValid();
        hdr.srcRoutes[8].bos = bos8;
        hdr.srcRoutes[8].port = port8;

        hdr.srcRoutes[9].setValid();
        hdr.srcRoutes[9].bos = bos9;
        hdr.srcRoutes[9].port = port9;

        hdr.srcRoutes[10].setValid();
        hdr.srcRoutes[10].bos = bos10;
        hdr.srcRoutes[10].port = port10;

        hdr.srcRoutes[11].setValid();
        hdr.srcRoutes[11].bos = bos11;
        hdr.srcRoutes[11].port = port11;

        hdr.srcRoutes[12].setValid();
        hdr.srcRoutes[12].bos = bos12;
        hdr.srcRoutes[12].port = port12;

        hdr.srcRoutes[13].setValid();
        hdr.srcRoutes[13].bos = bos13;
        hdr.srcRoutes[13].port = port13;

        hdr.srcRoutes[14].setValid();
        hdr.srcRoutes[14].bos = bos14;
        hdr.srcRoutes[14].port = port14;

        hdr.srcRoutes[15].setValid();
        hdr.srcRoutes[15].bos = bos15;
        hdr.srcRoutes[15].port = port15;
        
        hdr.srcRoutes[16].setValid();
        hdr.srcRoutes[16].bos = bos16;
        hdr.srcRoutes[16].port = port16;
    }

    table tunnel_encap_process_sr {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            add_header_0hop;
            add_header_1hop;
            add_header_2hops;
            add_header_3hops;
            add_header_4hops;
            add_header_5hops;
            add_header_6hops;
            add_header_7hops;
            add_header_8hops;
            add_header_9hops;
            add_header_10hops;
            add_header_11hops;
            add_header_12hops;
            add_header_13hops;
            add_header_14hops;
            add_header_15hops;
            add_header_16hops;
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
            hdr.srcRoutes[3].setInvalid();
            hdr.srcRoutes[4].setInvalid();
            hdr.srcRoutes[5].setInvalid();
            hdr.srcRoutes[6].setInvalid();
            hdr.srcRoutes[7].setInvalid();
            hdr.srcRoutes[8].setInvalid();
            hdr.srcRoutes[9].setInvalid();
            hdr.srcRoutes[10].setInvalid();
            hdr.srcRoutes[11].setInvalid();
            hdr.srcRoutes[12].setInvalid();
            hdr.srcRoutes[13].setInvalid();
            hdr.srcRoutes[14].setInvalid();
            hdr.srcRoutes[15].setInvalid();
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
        hdr.srcRoutes[3].setInvalid();
        hdr.srcRoutes[4].setInvalid();
        hdr.srcRoutes[5].setInvalid();
        hdr.srcRoutes[6].setInvalid();
        hdr.srcRoutes[7].setInvalid();
        hdr.srcRoutes[8].setInvalid();
        hdr.srcRoutes[9].setInvalid();
        hdr.srcRoutes[10].setInvalid();
        hdr.srcRoutes[11].setInvalid();
        hdr.srcRoutes[12].setInvalid();
        hdr.srcRoutes[13].setInvalid();
        hdr.srcRoutes[14].setInvalid();
        hdr.srcRoutes[15].setInvalid();

    }

    apply {
        
    	if (hdr.ipv4.isValid() && hdr.ethernet.etherType != TYPE_SRCROUTING) {
            process_tunnel_encap.apply(hdr, meta, standard_metadata);
        } else if (hdr.ethernet.etherType == TYPE_SRCROUTING) {
            srcRoute_finish();
            standard_metadata.egress_spec = 1;
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
