# -*- coding: utf-8 -*-

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet, ethernet, ipv4, icmp
import time
import json
from urllib import request

API_URL = "https://attakx-service-507224908244.europe-west9.run.app/predict"

class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    # - parameters ddos demo -
    ATTACKER_IP     = "10.0.0.3"   # attacker
    FLOOD_THRESHOLD = 5            # >5 ICMP/s -> suspect
    TIME_WINDOW     = 1            # seconds

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)
        self.icmp_stats  = {}      # src_ip -> (count, t0)
        self.blocked_ips = set()   # blocked ips

    # PACKETS IN TREATMENT
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg    = ev.msg
        dp     = msg.datapath
        ofp    = dp.ofproto
        parser = dp.ofproto_parser
        in_port = msg.in_port

        # DETECT ICMP flood
        pkt     = packet.Packet(msg.data)
        ip4_hdr = pkt.get_protocol(ipv4.ipv4)
        icmp_hdr = pkt.get_protocol(icmp.icmp)

        if ip4_hdr and icmp_hdr and icmp_hdr.type == 8:  # Echo-Request
            src_ip = ip4_hdr.src
            self.update_icmp_stats(src_ip)
            if self.is_flood(src_ip):
                self.handle_possible_ddos(dp, parser, src_ip)

        # switch L2 (flood)
        actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        data    = msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None

        out = parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        dp.send_msg(out)

    # COMPTEUR & SEUIL ICMP
    def update_icmp_stats(self, src_ip):
        now = time.time()
        count, t0 = self.icmp_stats.get(src_ip, (0, now))
        if now - t0 >= self.TIME_WINDOW:
            count, t0 = 0, now
        self.icmp_stats[src_ip] = (count + 1, t0)

    def is_flood(self, src_ip):
        if src_ip != self.ATTACKER_IP:
            return False
        count, _ = self.icmp_stats.get(src_ip, (0, 0))
        return count > self.FLOOD_THRESHOLD

    # API CALL AND FLOW DROP
    def handle_possible_ddos(self, dp, parser, src_ip):
        if src_ip in self.blocked_ips:
            return  # already blocked

        payload = self.build_ddos_payload()
        verdict = self.call_api(payload)
        self.logger.info("API verdict for %s → %s", src_ip, verdict)

        if verdict and verdict.lower() not in ("normal", "success"):
            self.install_drop_flow(dp, parser, src_ip)
            self.blocked_ips.add(src_ip)

    def build_ddos_payload(self):
        # Parameters
        return {
            "duration": 0, "protocol_type": "icmp", "flag": "SF",
            "src_bytes": 4096, "dst_bytes": 0, "land": 0,
            "wrong_fragment": 0, "urgent": 0, "hot": 0,
            "num_failed_logins": 0, "logged_in": 0,
            "num_compromised": 0, "root_shell": 1,
            "su_attempted": 0, "num_file_creations": 0,
            "num_shells": 0, "num_access_files": 0,
            "is_guest_login": 0, "count": 100, "srv_count": 100,
            "serror_rate": 1.0, "rerror_rate": 0.0,
            "same_srv_rate": 1.0, "diff_srv_rate": 0.0,
            "srv_diff_host_rate": 0.0, "dst_host_count": 255,
            "dst_host_srv_count": 255, "dst_host_same_srv_rate": 1.0,
            "dst_host_diff_srv_rate": 0.0,
            "dst_host_same_src_port_rate": 1.0,
            "dst_host_srv_diff_host_rate": 0.0,
            "time": int(time.time())
        }

    def call_api(self, payload):
        try:
            req = request.Request(API_URL,
                                  data=json.dumps(payload).encode(),
                                  headers={'Content-Type': 'application/json'})
            with request.urlopen(req, timeout=2) as resp:
                return json.load(resp).get("prediction", "unknown")
        except Exception as e:
            self.logger.warning("API call failed (%s) – continue", e)
            return "error"

    def install_drop_flow(self, dp, parser, src_ip):
        ofp = dp.ofproto
        match = parser.OFPMatch(dl_type=0x0800, nw_src=src_ip)
        mod = parser.OFPFlowMod(datapath=dp, priority=100, match=match,
                                cookie=0, command=ofp.OFPFC_ADD,
                                idle_timeout=0, hard_timeout=0,
                                actions=[]) 
        dp.send_msg(mod)
        self.logger.info("### DROP installed for %s ###", src_ip)