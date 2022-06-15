'''
    Script made to run tubes' topology
    - Yasir Khairul Malik (1301204395)
'''

from time import sleep

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

from topology import Tubes


def ping_local_subnet(net): # CLO 1
    '''
        Ping all subnet in tubes' topology locally
    '''
    a, b, r1, r2, r3, r4 = net.get('A', 'B', 'R1', 'R2', 'R3', 'R4')
    a.cmdPrint('ping -c 4 192.168.0.1')     # A to R!
    a.cmdPrint('ping -c 4 192.168.1.1')     # A to R2
    b.cmdPrint('ping -c 4 192.168.2.1')     # B to R3
    b.cmdPrint('ping -c 4 192.168.3.1')     # B to R4
    r1.cmdPrint('ping -c 4 192.168.255.2')  # R1 to R3
    r1.cmdPrint('ping -c 4 192.168.255.6')  # R1 to R4
    r2.cmdPrint('ping -c 4 192.168.255.10') # R2 to R3
    r2.cmdPrint('ping -c 4 192.168.255.14') # R2 to R4

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

def tcp_traffic(net):   # CLO 3
    a, b = net.get('A', 'B')
    a.cmd('iperf -s &')
    a.cmd('tcpdump tcp -c 5 -w 1301204395.pcap &')
    sleep(1)
    b.cmdPrint('iperf -c 192.168.0.10 -t 5')
    a.cmdPrint('tcpdump -r 1301204395.pcap')


def main():
    setLogLevel('info')
    net = Mininet(Tubes())
    net.start()
    # ping_local_subnet(net)
    enable_routing(net)
    tcp_traffic(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()