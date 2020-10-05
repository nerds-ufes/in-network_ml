/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

//My includes
#include "headers.p4"
#include "parsers.p4"


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

    table ipv4_lpm {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }

    apply {

        //only if IPV4 the rule is applied. Therefore other packets will not be forwarded.
        if (hdr.ipv4.isValid()){
            ipv4_lpm.apply();

        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {


    action add_int_header(switch_id_t swid){
        meta.switch_id = swid;

            hdr.int_count.num_switches = hdr.int_count.num_switches + 1;

            hdr.int_headers.push_front(1);
            hdr.int_headers[0].setValid();
            hdr.int_headers[0].switch_id = (bit<32>)meta.switch_id;
            hdr.int_headers[0].output_port = (bit<32>)standard_metadata.egress_port;

            hdr.int_headers[0].ini = (bit<64>) standard_metadata.egress_global_timestamp;
            hdr.int_headers[0].fim = (bit<64>) standard_metadata.egress_global_timestamp;

            hdr.ipv4.ihl = hdr.ipv4.ihl + 1;
            hdr.ipv4.totalLen = hdr.ipv4.totalLen + 24;
            hdr.ipv4_option.optionLength = hdr.ipv4_option.optionLength + 24;
    }

    table int_table {
        actions = {
            add_int_header;
            NoAction;
        }
        default_action = NoAction();
    }

    apply {
        if (hdr.int_count.isValid()){
            int_table.apply();
        }
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	      hdr.ipv4.ihl,
              hdr.ipv4.dscp,
              hdr.ipv4.ecn,
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
***********************  S W I T C H  *******************************
*************************************************************************/

//switch architecture
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;