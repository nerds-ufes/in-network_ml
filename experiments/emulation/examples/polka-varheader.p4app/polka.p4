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

header srcRoute_1hop_t {
    bit<8>   rlength;
    bit<16>    routeId;
}

header srcRoute_2hops_t {
    bit<8>   rlength;
    bit<32>    routeId;
}

header srcRoute_3hops_t {
    bit<8>   rlength;
    bit<48>    routeId;
}

header srcRoute_4hops_t {
    bit<8>   rlength;
    bit<64>    routeId;
}

header srcRoute_5hops_t {
    bit<8>   rlength;
    bit<80>    routeId;
}

header srcRoute_6hops_t {
    bit<8>   rlength;
    bit<96>    routeId;
}

header srcRoute_7hops_t {
    bit<8>   rlength;
    bit<112>    routeId;
}

header srcRoute_8hops_t {
    bit<8>   rlength;
    bit<128>    routeId;
}

header srcRoute_9hops_t {
    bit<8>   rlength;
    bit<144>    routeId;
}

header srcRoute_10hops_t {
    bit<8>    rlength;
    bit<160>    routeId;
}

header srcRoute_11hops_t {
    bit<8>   rlength;
    bit<176>    routeId;
}

header srcRoute_12hops_t {
    bit<8>   rlength;
    bit<192>    routeId;
}

header srcRoute_13hops_t {
    bit<8>   rlength;
    bit<208>    routeId;
}

header srcRoute_14hops_t {
    bit<8>   rlength;
    bit<224>    routeId;
}

header srcRoute_15hops_t {
    bit<8>   rlength;
    bit<240>    routeId;
}

header srcRoute_16hops_t {
    bit<8>   rlength;
    bit<256>    routeId;
}

struct metadata {
    bit<8>   rlength;
    bit<256>   routeId;
    bit<16>   etherType;
    bit<1> apply_sr;
    bit<1> apply_decap;
    bit<9> port;
}

struct polka_t_top {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
}

struct polka_t_top_1hop {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<16>    routeId;
}

struct polka_t_top_2hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<32>    routeId;
}

struct polka_t_top_3hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<48>    routeId;
}

struct polka_t_top_4hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<64>    routeId;
}

struct polka_t_top_5hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<80>    routeId;
}

struct polka_t_top_6hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<96>    routeId;
}

struct polka_t_top_7hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<112>    routeId;
}

struct polka_t_top_8hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<128>    routeId;
}

struct polka_t_top_9hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<144>    routeId;
}

struct polka_t_top_10hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<160>    routeId;
}

struct polka_t_top_11hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<176>    routeId;
}

struct polka_t_top_12hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<192>    routeId;
}

struct polka_t_top_13hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<208>    routeId;
}

struct polka_t_top_14hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<224>    routeId;
}

struct polka_t_top_15hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<240>    routeId;
}

struct polka_t_top_16hops {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<8>   rlength;
    bit<256>    routeId;
}

struct headers {
    ethernet_t  ethernet;
    srcRoute_1hop_t  srcRoute_1hop;
    srcRoute_2hops_t  srcRoute_2hops;
    srcRoute_3hops_t  srcRoute_3hops;
    srcRoute_4hops_t  srcRoute_4hops;
    srcRoute_5hops_t  srcRoute_5hops;
    srcRoute_6hops_t  srcRoute_6hops;
    srcRoute_7hops_t  srcRoute_7hops;
    srcRoute_8hops_t  srcRoute_8hops;
    srcRoute_9hops_t  srcRoute_9hops;
    srcRoute_10hops_t  srcRoute_10hops;
    srcRoute_11hops_t  srcRoute_11hops;
    srcRoute_12hops_t  srcRoute_12hops;
    srcRoute_13hops_t  srcRoute_13hops;
    srcRoute_14hops_t  srcRoute_14hops;
    srcRoute_15hops_t  srcRoute_15hops;
    srcRoute_16hops_t  srcRoute_16hops;
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
        meta.routeId = 0;
        transition verify_decap;
    }

    state verify_decap{
        transition select(meta.apply_decap) {
            1: parse_srcRouting;
            default: verify_ethernet;
        }
    }

    state verify_ethernet {
        meta.etherType = packet.lookahead<polka_t_top>().etherType;
        transition select(meta.etherType) {
            TYPE_SRCROUTING: select_routeid_size;
            TYPE_IPV4: parse_ethernet;
            default: accept;
        }
    }

    state select_routeid_size {
        bit<8> n = packet.lookahead<polka_t_top>().rlength;
        transition select(n) {
            0 : get_routeId_1hop;
            1 : get_routeId_2hops;
            2 : get_routeId_3hops;
            3 : get_routeId_4hops;
            4 : get_routeId_5hops;
            5 : get_routeId_6hops;
            6 : get_routeId_7hops;
            7 : get_routeId_8hops;
            8 : get_routeId_9hops;
            9 : get_routeId_10hops;
            10 : get_routeId_11hops;
            11 : get_routeId_12hops;
            12 : get_routeId_13hops;
            13 : get_routeId_14hops;
            14 : get_routeId_15hops;
            15 : get_routeId_16hops;
        }
    }

    state get_routeId_1hop {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_1hop>().routeId);
        transition accept;
    }

    state get_routeId_2hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_2hops>().routeId);
        transition accept;
    }

    state get_routeId_3hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_3hops>().routeId);
        transition accept;
    }

    state get_routeId_4hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_4hops>().routeId);
        transition accept;
    }

    state get_routeId_5hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_5hops>().routeId);
        transition accept;
    }

    state get_routeId_6hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_6hops>().routeId);
        transition accept;
    }

    state get_routeId_7hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_7hops>().routeId);
        transition accept;
    }

    state get_routeId_8hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_8hops>().routeId);
        transition accept;
    }

    state get_routeId_9hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_9hops>().routeId);
        transition accept;
    }

    state get_routeId_10hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_10hops>().routeId);
        transition accept;
    }

    state get_routeId_11hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_11hops>().routeId);
        transition accept;
    }

    state get_routeId_12hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_12hops>().routeId);
        transition accept;
    }

    state get_routeId_13hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_13hops>().routeId);
        transition accept;
    }

    state get_routeId_14hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_14hops>().routeId);
        transition accept;
    }

    state get_routeId_15hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_15hops>().routeId);
        transition accept;
    }

    state get_routeId_16hops {
        meta.routeId = (bit<256>)(packet.lookahead<polka_t_top_16hops>().routeId);
        transition accept;
    }

    state parse_srcRouting {

        bit<8> n = packet.lookahead<polka_t_top>().rlength;
        packet.extract(hdr.ethernet);

        transition select(n) {
            0 : parse_srcRouting_1hop;
            1 : parse_srcRouting_2hops;
            2 : parse_srcRouting_3hops;
            3 : parse_srcRouting_4hops;
            4 : parse_srcRouting_5hops;
            5 : parse_srcRouting_6hops;
            6 : parse_srcRouting_7hops;
            7 : parse_srcRouting_8hops;
            8 : parse_srcRouting_9hops;
            9 : parse_srcRouting_10hops;
            10 : parse_srcRouting_11hops;
            11 : parse_srcRouting_12hops;
            12 : parse_srcRouting_13hops;
            13 : parse_srcRouting_14hops;
            14 : parse_srcRouting_15hops;
            15 : parse_srcRouting_16hops;
        }
    }

    state parse_srcRouting_1hop {
        packet.extract(hdr.srcRoute_1hop);
        transition accept;
    }

    state parse_srcRouting_2hops {
        packet.extract(hdr.srcRoute_2hops);
        transition accept;
    }

    state parse_srcRouting_3hops {
        packet.extract(hdr.srcRoute_3hops);
        transition accept;
    }

    state parse_srcRouting_4hops {
        packet.extract(hdr.srcRoute_4hops);
        transition accept;
    }

    state parse_srcRouting_5hops {
        packet.extract(hdr.srcRoute_5hops);
        transition accept;
    }

    state parse_srcRouting_6hops {
        packet.extract(hdr.srcRoute_6hops);
        transition accept;
    }

    state parse_srcRouting_7hops {
        packet.extract(hdr.srcRoute_7hops);
        transition accept;
    }

    state parse_srcRouting_8hops {
        packet.extract(hdr.srcRoute_8hops);
        transition accept;
    }

    state parse_srcRouting_9hops {
        packet.extract(hdr.srcRoute_9hops);
        transition accept;
    }

    state parse_srcRouting_10hops {
        packet.extract(hdr.srcRoute_10hops);
        transition accept;
    }

    state parse_srcRouting_11hops {
        packet.extract(hdr.srcRoute_11hops);
        transition accept;
    }

    state parse_srcRouting_12hops {
        packet.extract(hdr.srcRoute_12hops);
        transition accept;
    }

    state parse_srcRouting_13hops {
        packet.extract(hdr.srcRoute_13hops);
        transition accept;
    }

    state parse_srcRouting_14hops {
        packet.extract(hdr.srcRoute_14hops);
        transition accept;
    }

    state parse_srcRouting_15hops {
        packet.extract(hdr.srcRoute_15hops);
        transition accept;
    }

    state parse_srcRouting_16hops {
        packet.extract(hdr.srcRoute_16hops);
        transition accept;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition parse_ipv4;
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

    action add_header_0hop (   egressSpec_t port, bit<1> sr, macAddr_t dmac){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

    }

    action add_header_1hop (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<16>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_1hop.setValid();
        hdr.srcRoute_1hop.rlength = 0;
        hdr.srcRoute_1hop.routeId = routeIdPacket;
    }


    action add_header_2hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<32>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_2hops.setValid();
        hdr.srcRoute_2hops.rlength = 1;
        hdr.srcRoute_2hops.routeId = routeIdPacket;
    }

    action add_header_3hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<48>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_3hops.setValid();
        hdr.srcRoute_3hops.rlength = 2;
        hdr.srcRoute_3hops.routeId = routeIdPacket;
    }

    action add_header_4hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<64>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_4hops.setValid();
        hdr.srcRoute_4hops.rlength = 3;
        hdr.srcRoute_4hops.routeId = routeIdPacket;
    }

    action add_header_5hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<80>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_5hops.setValid();
        hdr.srcRoute_5hops.rlength = 4;
        hdr.srcRoute_5hops.routeId = routeIdPacket;
    }

    action add_header_6hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<96>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_6hops.setValid();
        hdr.srcRoute_6hops.rlength = 5;
        hdr.srcRoute_6hops.routeId = routeIdPacket;
    }

    action add_header_7hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<112>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_7hops.setValid();
        hdr.srcRoute_7hops.rlength = 6;
        hdr.srcRoute_7hops.routeId = routeIdPacket;
    }

    action add_header_8hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<128>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_8hops.setValid();
        hdr.srcRoute_8hops.rlength = 7;
        hdr.srcRoute_8hops.routeId = routeIdPacket;
    }

    action add_header_9hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<144>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_9hops.setValid();
        hdr.srcRoute_9hops.rlength = 8;
        hdr.srcRoute_9hops.routeId = routeIdPacket;
    }

    action add_header_10hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<160>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_10hops.setValid();
        hdr.srcRoute_10hops.rlength = 9;
        hdr.srcRoute_10hops.routeId = routeIdPacket;
    }

    action add_header_11hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<176>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_11hops.setValid();
        hdr.srcRoute_11hops.rlength = 10;
        hdr.srcRoute_11hops.routeId = routeIdPacket;
    }

    action add_header_12hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<192>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_12hops.setValid();
        hdr.srcRoute_12hops.rlength = 11;
        hdr.srcRoute_12hops.routeId = routeIdPacket;
    }

    action add_header_13hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<208>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_13hops.setValid();
        hdr.srcRoute_13hops.rlength = 12;
        hdr.srcRoute_13hops.routeId = routeIdPacket;
    }

    action add_header_14hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<224>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_14hops.setValid();
        hdr.srcRoute_14hops.rlength = 13;
        hdr.srcRoute_14hops.routeId = routeIdPacket;
    }

    action add_header_15hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<240>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_15hops.setValid();
        hdr.srcRoute_15hops.rlength = 14;
        hdr.srcRoute_15hops.routeId = routeIdPacket;
    }

    action add_header_16hops (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<256>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute_16hops.setValid();
        hdr.srcRoute_16hops.rlength = 15;
        hdr.srcRoute_16hops.routeId = routeIdPacket;
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
            //hdr.srcRoute.setInvalid();
            hdr.srcRoute_1hop.setInvalid();
            hdr.srcRoute_2hops.setInvalid();
            hdr.srcRoute_3hops.setInvalid();
            hdr.srcRoute_4hops.setInvalid();
            hdr.srcRoute_5hops.setInvalid();
            hdr.srcRoute_6hops.setInvalid();
            hdr.srcRoute_7hops.setInvalid();
            hdr.srcRoute_8hops.setInvalid();
            hdr.srcRoute_9hops.setInvalid();
            hdr.srcRoute_10hops.setInvalid();
            hdr.srcRoute_11hops.setInvalid();
            hdr.srcRoute_12hops.setInvalid();
            hdr.srcRoute_13hops.setInvalid();
            hdr.srcRoute_14hops.setInvalid();
            hdr.srcRoute_15hops.setInvalid();
            hdr.srcRoute_16hops.setInvalid();
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

    action srcRoute_nhop() {

        bit<16> nbase=0;
        bit<64> ncount=4294967296*2;
        bit<16> nresult;
        bit<16> nport;

        bit<256> routeid = meta.routeId;
        //routeid = 57851202663303480771156315372;

        bit<256> ndata = routeid >> 16;
        bit<16> dif = (bit<16>) (routeid ^ (ndata << 16));

        hash(nresult,
        HashAlgorithm.crc16_custom,
        nbase,
        {ndata},ncount);

        nport = nresult ^ dif;

        meta.port= (bit<9>) nport;

    }

    apply {

        if (meta.apply_decap==1){
            hdr.ethernet.etherType = TYPE_IPV4;
            hdr.srcRoute_1hop.setInvalid();
            hdr.srcRoute_2hops.setInvalid();
            hdr.srcRoute_3hops.setInvalid();
            hdr.srcRoute_4hops.setInvalid();
            hdr.srcRoute_5hops.setInvalid();
            hdr.srcRoute_6hops.setInvalid();
            hdr.srcRoute_7hops.setInvalid();
            hdr.srcRoute_8hops.setInvalid();
            hdr.srcRoute_9hops.setInvalid();
            hdr.srcRoute_10hops.setInvalid();
            hdr.srcRoute_11hops.setInvalid();
            hdr.srcRoute_12hops.setInvalid();
            hdr.srcRoute_13hops.setInvalid();
            hdr.srcRoute_14hops.setInvalid();
            hdr.srcRoute_15hops.setInvalid();
            hdr.srcRoute_16hops.setInvalid();

            standard_metadata.egress_spec = meta.port;
        }else{
            if (meta.routeId>0){
                srcRoute_nhop();

                if (meta.port==1){
                    meta.apply_decap = 1;
                    resubmit({meta, standard_metadata});
                }else{
                    standard_metadata.egress_spec = meta.port;
                }

            }else{
                if (hdr.ethernet.isValid() && hdr.ipv4.isValid()){
                    process_tunnel_encap.apply(hdr, meta, standard_metadata);
                }else{
                    drop();
                }
            }
        }
    }
}


/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {

    }
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
        packet.emit(hdr.srcRoute_1hop);
        packet.emit(hdr.srcRoute_2hops);
        packet.emit(hdr.srcRoute_3hops);
        packet.emit(hdr.srcRoute_4hops);
        packet.emit(hdr.srcRoute_5hops);
        packet.emit(hdr.srcRoute_6hops);
        packet.emit(hdr.srcRoute_7hops);
        packet.emit(hdr.srcRoute_8hops);
        packet.emit(hdr.srcRoute_9hops);
        packet.emit(hdr.srcRoute_10hops);
        packet.emit(hdr.srcRoute_11hops);
        packet.emit(hdr.srcRoute_12hops);
        packet.emit(hdr.srcRoute_13hops);
        packet.emit(hdr.srcRoute_14hops);
        packet.emit(hdr.srcRoute_15hops);
        packet.emit(hdr.srcRoute_16hops);
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
