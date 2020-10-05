/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#define MAX_INT_HEADERS 9
const bit<32>  REGISTER_LENGTH  = 131072;
const bit<16> TYPE_IPV4 = 0x800;
const bit<5>  IPV4_OPTION_INT = 31;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

typedef bit<13> switch_id_t;
typedef bit<13> queue_depth_t;
typedef bit<6>  output_port_t;

header ipv4_option_t {
    bit<1> copyFlag;
    bit<2> optClass;
    bit<5> option;
    bit<8> optionLength;
}

header int_count_t {
    bit<16>   num_switches;
}

header int_header_t {
    bit<8> class;
    bit<16> df;
    bit<16> mf;
    bit<16> fin;
    bit<16> syn;
    bit<16> rst;
    bit<16> psh;
    bit<16> ack;
    bit<16> urg;
    bit<16> ece;
    bit<16> cwr;
    
    bit<32> totalLen;

    bit<48> flow_duration;
    bit<32> min_pkt_len;
    bit<32> max_pkt_len;
    bit<32> pkts;
}

struct parser_metadata_t {
    bit<16> num_headers_remaining;
}

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
    bit<1>    reserv;
    bit<1>    df;
    bit<1>    mf;
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
    bit<1>  ns;
    bit<1>  ece;
    bit<1>  cwr;
    bit<1> urg;
    bit<1> ack;
    bit<1> psh;
    bit<1> rst;
    bit<1> syn;
    bit<1> fin;
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
struct intrinsic_metadata_t {
    bit<48> ingress_global_timestamp;
}
/*
    bit<64> ingress_global_timestamp; 
    bit<64> current_global_tstamp; 

*/  



struct metadata {
    bit<3> class;
    bit<8> if_;
    bit<32> fw_index;

    bit <16> srcPort;
    bit <16> dstPort;
    bit <8> protocol;

    bit<16> df;
    bit<16> mf;
    bit<16> fin;
    bit<16> syn;
    bit<16> rst;
    bit<16> psh;
    bit<16> ack;
    bit<16> urg;
    bit<16> ece;
    bit<16> cwr;
    bit<32> totalLen;

    bit<48> flow_duration;
    bit<32> min_pkt_len;
    bit<32> max_pkt_len;
    bit<32> pkts;
    bit<32> avg_len;
    bit<32> len_variance;
    bit<48> first_pkt;
    bit<32> k;
    bit<32> ex;
    bit<32> ex2;

    bit<32> flags;
    
    intrinsic_metadata_t intrinsic_metadata;
    parser_metadata_t  parser_metadata;
}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    tcp_t        tcp;
    udp_t        udp;
    ipv4_option_t ipv4_option;
    int_count_t   int_count;
    int_header_t[MAX_INT_HEADERS] int_headers;    
}
error { IPHeaderWithoutOptions }

register<bit<16>>(REGISTER_LENGTH) df;
register<bit<16>>(REGISTER_LENGTH) mf;
register<bit<16>>(REGISTER_LENGTH) fin;
register<bit<16>>(REGISTER_LENGTH) syn;
register<bit<16>>(REGISTER_LENGTH) rst;
register<bit<16>>(REGISTER_LENGTH) psh;
register<bit<16>>(REGISTER_LENGTH) ack;
register<bit<16>>(REGISTER_LENGTH) urg;
register<bit<16>>(REGISTER_LENGTH) ece;
register<bit<16>>(REGISTER_LENGTH) cwr;
register<bit<32>>(REGISTER_LENGTH) totalLen;

register<bit<48>>(REGISTER_LENGTH) flow_duration;
register<bit<32>>(REGISTER_LENGTH) min_pkt_len;
register<bit<32>>(REGISTER_LENGTH) max_pkt_len;
register<bit<32>>(REGISTER_LENGTH) pkts;
register<bit<32>>(REGISTER_LENGTH) avg_len;
register<bit<32>>(REGISTER_LENGTH) len_variance;
register<bit<48>>(REGISTER_LENGTH) first_pkt;
register<bit<32>>(REGISTER_LENGTH) k;
register<bit<32>>(REGISTER_LENGTH) ex;
register<bit<32>>(REGISTER_LENGTH) ex2;
/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/


parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {

        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType){
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        //Check if ihl is bigger than 5. Packets without ip options set ihl to 5.
        //verify(hdr.ipv4.ihl >= 5, error.IPHeaderWithoutOptions);
        transition parse_ipv4_option;
    }
    state parse_ipv4_option {
        packet.extract(hdr.ipv4_option);
        transition select(hdr.ipv4_option.option){

            IPV4_OPTION_INT:  parse_int;
            default: accept;

        }
     }

    state parse_int {
        packet.extract(hdr.int_count);
        meta.parser_metadata.num_headers_remaining = hdr.int_count.num_switches;
        transition select(meta.parser_metadata.num_headers_remaining){
            0: parse_l3;
            default: parse_int_headers;
        }
    }

    state parse_int_headers {
        packet.extract(hdr.int_headers.next);
        meta.parser_metadata.num_headers_remaining = meta.parser_metadata.num_headers_remaining -1 ;
        transition select(meta.parser_metadata.num_headers_remaining){
            0: accept;
            default: parse_int_headers;
        }
    }  

    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }

    state parse_l3 {
        transition select(hdr.ipv4.protocol) {
            6: parse_tcp;
            17: parse_udp;
            default: accept;
        }
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
    action hash_() {
        hash<bit<32>, bit<16>, tuple<bit<32>,bit<32>,bit<16>,bit<16>,bit<8>>, bit<32>>
            (meta.fw_index,
            HashAlgorithm.crc32, 16w0,
            { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, meta.srcPort, meta.dstPort, hdr.ipv4.protocol},
            REGISTER_LENGTH);
    }    
    action read(bit<32> hash) {
        df.read(meta.df, hash);
        mf.read(meta.mf, hash);
        fin.read(meta.fin, hash);
        syn.read(meta.syn, hash);
        rst.read(meta.rst, hash);
        psh.read(meta.psh, hash);
        ack.read(meta.ack, hash);
        urg.read(meta.urg, hash);
        ece.read(meta.ece, hash);
        cwr.read(meta.cwr, hash);
        totalLen.read(meta.totalLen, hash);
        flow_duration.read(meta.flow_duration, hash);
        min_pkt_len.read(meta.min_pkt_len, hash);
        max_pkt_len.read(meta.max_pkt_len, hash);
        pkts.read(meta.pkts, hash);
        avg_len.read(meta.avg_len, hash);
        len_variance.read(meta.len_variance, hash);
        first_pkt.read(meta.first_pkt, hash);
        k.read(meta.k, hash);
        ex.read(meta.ex, hash);
        ex2.read(meta.ex2, hash);
    }

    action write(bit<32> hash) {
        df.write(hash, meta.df);
        mf.write(hash, meta.mf);
        fin.write(hash, meta.fin);
        syn.write(hash, meta.syn);
        rst.write(hash, meta.rst);
        psh.write(hash, meta.psh);
        ack.write(hash, meta.ack);
        urg.write(hash, meta.urg);
        ece.write(hash, meta.ece);
        cwr.write(hash, meta.cwr);
        totalLen.write(hash, meta.totalLen);
        flow_duration.write(hash, meta.flow_duration);
        min_pkt_len.write(hash, meta.min_pkt_len);
        max_pkt_len.write(hash, meta.max_pkt_len);
        pkts.write(hash, meta.pkts);
        avg_len.write(hash, meta.avg_len);
        len_variance.write(hash, meta.len_variance);
        first_pkt.write(hash, meta.first_pkt);
        k.write(hash, meta.k);
        ex.write(hash, meta.ex);
        ex2.write(hash, meta.ex2);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
    
    table ipv4_class {
        key = {
            meta.class: exact;
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
        if (hdr.ipv4.isValid()) {
            if (hdr.tcp.isValid()) {
                meta.srcPort = hdr.tcp.srcPort;
                meta.dstPort = hdr.tcp.dstPort;
            } else if (hdr.udp.isValid()) {
                meta.srcPort = hdr.udp.srcPort;
                meta.dstPort = hdr.udp.dstPort;
            } else{
                meta.srcPort = hdr.tcp.srcPort;
                meta.dstPort = hdr.tcp.dstPort;
            }
            hash_();
            read(meta.fw_index);

            if (meta.pkts == 0) {
                meta.first_pkt = standard_metadata.ingress_global_timestamp;
                meta.min_pkt_len = (bit<32>)hdr.ipv4.totalLen;
                meta.max_pkt_len = 0;
                meta.k = (bit<32>)hdr.ipv4.totalLen;
                meta.totalLen = 0;
            }
            meta.df = meta.df + (bit<16>)hdr.ipv4.df;
            meta.mf = meta.mf + (bit<16>)hdr.ipv4.mf;
            meta.fin = meta.fin + (bit<16>)hdr.tcp.fin;
            meta.syn = meta.syn + (bit<16>)hdr.tcp.syn;
            meta.rst = meta.rst + (bit<16>)hdr.tcp.rst;
            meta.psh = meta.psh + (bit<16>)hdr.tcp.psh;
            meta.ack = meta.ack + (bit<16>)hdr.tcp.ack;
            meta.urg = meta.urg + (bit<16>)hdr.tcp.urg;
            meta.ece = meta.ece + (bit<16>)hdr.tcp.ece;
            meta.cwr = meta.cwr + (bit<16>)hdr.tcp.cwr;
            meta.totalLen = meta.totalLen + (bit<32>)hdr.ipv4.totalLen;
            meta.flow_duration = standard_metadata.ingress_global_timestamp - meta.first_pkt;
            if (meta.min_pkt_len > (bit<32>)hdr.ipv4.totalLen)
                meta.min_pkt_len = (bit<32>)hdr.ipv4.totalLen;
            if (meta.max_pkt_len < (bit<32>)hdr.ipv4.totalLen)
                meta.max_pkt_len = (bit<32>)hdr.ipv4.totalLen;
            meta.pkts = meta.pkts + 1;
            
            //meta.ex =  meta.ex + (meta.totalLen - meta.k);
            //meta.ex2 = meta.ex2 + ((meta.totalLen - meta.k) * (meta.totalLen - meta.k));
            //meta.len_variance = (meta.ex2 - (meta.ex * meta.ex)/meta.pkts) / (meta.pkts - 1);
            write(meta.fw_index);

            if (meta.rst <= 1) 
                if (meta.max_pkt_len <= 46) 
                    if (meta.ack <= 0) 
                        meta.class = 6;
                    else 
                        meta.class = 0;
                else 
                    if (meta.max_pkt_len <= 60) 
                        if (meta.max_pkt_len <= 59) 
                            meta.class = 0;
                        else 
                            if (meta.syn <= 1) 
                                if (meta.dstPort <= 291) 
                                    if (hdr.ipv4.protocol <= 11) 
                                        if (meta.flow_duration <= 0) 
                                            if (meta.min_pkt_len <= 56) 
                                                if (meta.flow_duration <= 0) 
                                                    meta.class = 2;
                                                else 
                                                    meta.class = 4;
                                            else 
                                                meta.class = 4;
                                        else 
                                            if (meta.totalLen <= 152) 
                                                meta.class = 0;
                                            else 
                                                if (meta.flow_duration <= 6) 
                                                    if (meta.min_pkt_len <= 46) 
                                                        meta.class = 0;
                                                    else 
                                                        meta.class = 4;
                                                else 
                                                    meta.class = 0;
                                    else 
                                        meta.class = 0;
                                else 
                                    meta.class = 0;
                            else 
                                if (meta.dstPort <= 84) 
                                    if (meta.syn <= 3) 
                                        if (meta.flow_duration <= 1) 
                                            meta.class = 3;
                                        else 
                                            meta.class = 5;
                                    else 
                                        meta.class = 3;
                                else 
                                    meta.class = 0;
                    else 
                        if (meta.max_pkt_len <= 281) 
                            meta.class = 0;
                        else 
                            if (meta.dstPort <= 84) 
                                if (meta.max_pkt_len <= 283) 
                                    if (hdr.ipv4.protocol <= 11) 
                                        meta.class = 5;
                                    else 
                                        meta.class = 0;
                                else 
                                    if (meta.min_pkt_len <= 46) 
                                        if (meta.rst <= 0) 
                                            meta.class = 0;
                                        else 
                                            if (meta.flow_duration <= 107) 
                                                meta.class = 0;
                                            else 
                                                meta.class = 3;
                                    else 
                                        if (meta.dstPort <= 51) 
                                            meta.class = 0;
                                        else 
                                            if (meta.ack <= 10) 
                                                if (meta.flow_duration <= 3) 
                                                    if (meta.flow_duration <= 0) 
                                                        meta.class = 2;
                                                    else 
                                                        if (meta.flow_duration <= 0) 
                                                            meta.class = 0;
                                                        else 
                                                            meta.class = 0;
                                                else 
                                                    if (meta.flow_duration <= 18) 
                                                        if (meta.fin <= 0) 
                                                            meta.class = 2;
                                                        else 
                                                            meta.class = 0;
                                                    else 
                                                        if (meta.rst <= 0) 
                                                            if (meta.flow_duration <= 62) 
                                                                meta.class = 0;
                                                            else 
                                                                meta.class = 3;
                                                        else 
                                                            meta.class = 2;
                                            else 
                                                if (meta.psh <= 19) 
                                                    if (meta.syn <= 1) 
                                                        meta.class = 0;
                                                    else 
                                                        if (meta.rst <= 0) 
                                                            meta.class = 3;
                                                        else 
                                                            meta.class = 1;
                                                else 
                                                    meta.class = 4;
                            else 
                                meta.class = 0;
            else 
                if (meta.dstPort <= 234) 
                    meta.class = 1;
                else 
                    meta.class = 0;

        }
  

        ipv4_class.apply();
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    
    apply{
        hdr.int_count.num_switches = hdr.int_count.num_switches + 1;
        hdr.int_headers.push_front(1);
        hdr.int_headers[0].setValid();
        hdr.int_headers[0].class = (bit<8>)meta.class;   
        hdr.int_headers[0].df = meta.df;
        hdr.int_headers[0].mf = meta.mf;
        hdr.int_headers[0].fin = meta.fin;
        hdr.int_headers[0].syn = meta.syn;
        hdr.int_headers[0].rst = meta.rst;
        hdr.int_headers[0].psh = meta.psh;
        hdr.int_headers[0].ack = meta.ack;
        hdr.int_headers[0].urg = meta.urg;
        hdr.int_headers[0].ece = meta.ece;
        hdr.int_headers[0].cwr = meta.cwr;
        hdr.int_headers[0].totalLen = meta.totalLen;
        hdr.int_headers[0].flow_duration = meta.flow_duration;
        hdr.int_headers[0].min_pkt_len = meta.min_pkt_len;
        hdr.int_headers[0].max_pkt_len = meta.max_pkt_len;
        hdr.int_headers[0].pkts = meta.pkts; 
    }

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
              hdr.ipv4.reserv,
              hdr.ipv4.df,
              hdr.ipv4.mf,
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
        packet.emit(hdr.ipv4_option);
        packet.emit(hdr.int_count);
        packet.emit(hdr.int_headers);
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
