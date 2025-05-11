# -*- coding: utf-8 -*-         DO NOT REMOVE THIS LINE

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class NetworkTopology(Topo):
    def build(self):

        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        attacker = self.addHost('attacker', ip='10.0.0.3/24', mac='02:00:00:00:00:03')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch("s2")

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(attacker, s1)

if __name__ == '__main__':
    setLogLevel('info')

    net = Mininet(topo=NetworkTopology(), switch=OVSSwitch, controller=RemoteController)
    net.start()

    # Launch http server (port 80) on h1
    h1 = net.get('h1')
    h1.cmd('python3 -m http.server 80 &')

    # Generate ssl certificates for https server
    h1.cmd('openssl req -x509 -nodes -newkey rsa:2048 -keyout /tmp/h1.key -out /tmp/h1.crt '
           '-days 365 -subj "/CN=h1"')

    # Launch https server (port 443) on h1
    h1.cmd('python3 -c "import http.server, ssl; '
           'httpd = http.server.HTTPServer((\'0.0.0.0\', 443), http.server.SimpleHTTPRequestHandler); '
           'httpd.socket = ssl.wrap_socket(httpd.socket, certfile=\'/tmp/h1.crt\', keyfile=\'/tmp/h1.key\', server_side=True); '
           'httpd.serve_forever()" &')

    # Test for pingall
    print("Server HTTP/HTTPS launched on h1 (ports 80 and 443).")

    # Launch CLI
    CLI(net)
    net.stop()
