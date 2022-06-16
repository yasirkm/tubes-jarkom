'''
    Script made to run tubes' topology
    - Yasir Khairul Malik (1301204395)
'''

from time import sleep

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

from topology import Tubes


class Iperf_Server():
    def __init__(self, net, server):
        self.server = net[server]

    def __enter__(self):
        self.server.cmd('iperf -s &')
        sleep(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.cmd('kill %iperf')



def ping_local_subnet(net, count=4): # CLO 1
    '''
        Ping all subnet in tubes' topology locally
    '''
    a, b, r1, r2, r3, r4 = net.get('A', 'B', 'R1', 'R2', 'R3', 'R4')
    a.cmdPrint(f'ping -c {count} 192.168.0.1')     # A to R!
    a.cmdPrint(f'ping -c {count} 192.168.1.1')     # A to R2
    b.cmdPrint(f'ping -c {count} 192.168.2.1')     # B to R3
    b.cmdPrint(f'ping -c {count} 192.168.3.1')     # B to R4
    r1.cmdPrint(f'ping -c {count} 192.168.255.2')  # R1 to R3
    r1.cmdPrint(f'ping -c {count} 192.168.255.6')  # R1 to R4
    r2.cmdPrint(f'ping -c {count} 192.168.255.10') # R2 to R3
    r2.cmdPrint(f'ping -c {count} 192.168.255.14') # R2 to R4

def enable_routing(net):    # CLO 2
    r1, r2, r3, r4 = net.get('R1', 'R2', 'R3', 'R4')

    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r1.cmd('ip route add 0.0.0.0/0 via 192.168.255.2')
    # r1.cmd('ip route add 192.168.1.0/24 via 192.168.255.6 dev R1-eth1')
    # r1.cmd('ip route add 192.168.255.8/30 via 192.168.255.6 dev R1-eth1')
    # r1.cmd('ip route add 192.168.255.12/30 via 192.168.255.6 dev R1-eth1')
    # r1.cmd('ip route add 192.168.2.0/24 via 192.168.255.6 dev R1-eth1')
    # r1.cmd('ip route add 192.168.3.0/24 via 192.168.255.6 dev R1-eth1')

    r2.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('ip route add 0.0.0.0/0 via 192.168.255.10')
    r2.cmd('ip route add 192.168.3.0/24 via 192.168.255.14')
    # r2.cmd('ip route add 192.168.0.0/24 via 192.168.255.10 dev R2-eth1')
    # r2.cmd('ip route add 192.168.255.0/30 via 192.168.255.10 dev R2-eth1')
    # r2.cmd('ip route add 192.168.255.4/30 via 192.168.255.10 dev R2-eth1')
    # r2.cmd('ip route add 192.168.2.0/24 via 192.168.255.10 dev R2-eth1')
    # r2.cmd('ip route add 192.168.3.0/24 via 192.168.255.10 dev R2-eth1')

    r3.cmd('sysctl net.ipv4.ip_forward=1')
    # r3.cmd('ip route add 0.0.0.0/0 via 192.168.255.1 dev R3-eth2')
    r3.cmd('ip route add 192.168.0.0/24 via 192.168.255.1')
    r3.cmd('ip route add 192.168.1.0/24 via 192.168.255.9')
    r3.cmd('ip route add 192.168.255.4/30 via 192.168.255.1')
    r3.cmd('ip route add 192.168.255.12/30 via 192.168.255.9')
    r3.cmd('ip route add 192.168.3.0/24 via 192.168.255.9')

    # r3.cmd('ip route add 192.168.0.0/24 via 192.168.255.1 dev R3-eth2')
    # r3.cmd('ip route add 192.168.1.0/24 via 192.168.255.1 dev R3-eth2')
    # r3.cmd('ip route add 192.168.255.4/30 via 192.168.255.1 dev R3-eth2')
    # r3.cmd('ip route add 192.168.255.12/30 via 192.168.255.1 dev R3-eth2')
    # r3.cmd('ip route add 192.168.3.0/24 via 192.168.255.1 dev R3-eth2')

    r4.cmd('sysctl net.ipv4.ip_forward=1')
    r4.cmd('ip route add 0.0.0.0/0 via 192.168.255.13')
    # r4.cmd('ip route add 192.168.0.0/24 via 192.168.255.13 dev R4-eth2')
    # r4.cmd('ip route add 192.168.1.0/24 via 192.168.255.13 dev R4-eth2')
    # r4.cmd('ip route add 192.168.255.0/30 via 192.168.255.13 dev R4-eth2')
    # r4.cmd('ip route add 192.168.255.8/30 via 192.168.255.13 dev R4-eth2')
    # r4.cmd('ip route add 192.168.2.0/24 via 192.168.255.13 dev R4-eth2')

    net.pingAll()

def generate_tcp_traffic(net, time=5, capture=False, cap_file='1301204395.pcap'):   # CLO 3
    a, b = net.get('A', 'B')

    # a.cmd('iperf -s &')
    if capture:
        a.cmd(f'tcpdump tcp -c 20 -w {cap_file} &')
    # sleep(1)

    b.cmdPrint(f'iperf -c 192.168.0.10 -t {time} -i 1')

    if capture:
        a.cmdPrint(f'tcpdump -r {cap_file}')
    # a.cmd('kill %iperf')
    # sleep(20)

def generate_buffer_traffic(net):   # CLO 4
    def change_buffer(router, size):
        for intf in router.intfNames():
            router.cmd(f'tc qdisc del dev {intf} root')
            router.cmd(f'tc qdisc add dev {intf} root handle 1: pfifo limit {size}')

    buffer_sizes = (20,40,60,100)
    routers = ('R1', 'R2', 'R3', 'R4')
    
    for size in buffer_sizes:
        for router in routers:
            change_buffer(net[router], size)
        generate_tcp_traffic(net, time=5, capture=True, cap_file=f'buffer_{size}.pcap')


def main():
    setLogLevel('info')
    net = Mininet(Tubes())
    net.start()
    # ping_local_subnet(net)
    enable_routing(net)
    with Iperf_Server(net, 'A'):
        generate_tcp_traffic(net, capture=True)
        generate_buffer_traffic(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()