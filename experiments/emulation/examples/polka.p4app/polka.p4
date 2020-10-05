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
    bit<1> apply_decap;
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
            TYPE_SRCROUTING: get_routeId;
            TYPE_IPV4: parse_ethernet;
            default: accept;
        }
    }

    state get_routeId {
        meta.routeId = packet.lookahead<polka_t_top>().routeId;
        transition accept;
    }

    state parse_srcRouting {
        packet.extract(hdr.ethernet);
        packet.extract(hdr.srcRoute);
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

    action add_sourcerouting_header (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<160>  routeIdPacket){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;

        hdr.ethernet.dstAddr = dmac;

        hdr.srcRoute.setValid();
        hdr.srcRoute.routeId = routeIdPacket;

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

    apply {
        tunnel_encap_process_sr.apply();
        if(meta.apply_sr!=1){
            hdr.srcRoute.setInvalid();
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

        bit<160> routeid = meta.routeId;
        //routeid = 57851202663303480771156315372;

        bit<160> ndata = routeid >> 16;
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
            hdr.srcRoute.setInvalid();
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
    apply { }
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
