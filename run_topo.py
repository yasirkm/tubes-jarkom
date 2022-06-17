'''
    Script made to run tubes' topology
    - Yasir Khairul Malik (1301204395)
'''

from time import sleep

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from topology import Tubes


class Iperf_Server():
    '''
        Context manager for running iperf server
    '''
    def __init__(self, net, server):
        'Initiate server node'
        self.server = net[server]

    def __enter__(self):
        'Run iperf server process on server node'
        self.server.cmd('iperf -s &')
        sleep(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        'Close iperf process'
        self.server.cmd('kill %iperf')



def ping_local_subnet(net, count=4): # CLO 1
    '''
        Ping all subnet in tubes' topology locally
    '''
    a, b, r1, r2 = net.get('A', 'B', 'R1', 'R2')
    a.cmdPrint(f'ping -c {count} 192.168.0.1')     # A to R!
    info('\n')
    a.cmdPrint(f'ping -c {count} 192.168.1.1')     # A to R2
    info('\n')
    b.cmdPrint(f'ping -c {count} 192.168.2.1')     # B to R3
    info('\n')
    b.cmdPrint(f'ping -c {count} 192.168.3.1')     # B to R4
    info('\n')
    r1.cmdPrint(f'ping -c {count} 192.168.255.2')  # R1 to R3
    info('\n')
    r1.cmdPrint(f'ping -c {count} 192.168.255.6')  # R1 to R4
    info('\n')
    r2.cmdPrint(f'ping -c {count} 192.168.255.10') # R2 to R3
    info('\n')
    r2.cmdPrint(f'ping -c {count} 192.168.255.14') # R2 to R4
    info('\n')

def enable_routing(net):    # CLO 2
    '''
        Enable ipv4 routing on all routers
        Uses tree topology
    '''
    a, r1, r2, r3, r4 = net.get('A', 'R1', 'R2', 'R3', 'R4')

    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r1.cmd('ip route add 0.0.0.0/0 via 192.168.255.2')

    r2.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('ip route add 0.0.0.0/0 via 192.168.255.10')
    r2.cmd('ip route add 192.168.3.0/24 via 192.168.255.14')

    r3.cmd('sysctl net.ipv4.ip_forward=1')
    r3.cmd('ip route add 192.168.0.0/24 via 192.168.255.1')
    r3.cmd('ip route add 192.168.1.0/24 via 192.168.255.9')
    r3.cmd('ip route add 192.168.255.4/30 via 192.168.255.1')
    r3.cmd('ip route add 192.168.255.12/30 via 192.168.255.9')
    r3.cmd('ip route add 192.168.3.0/24 via 192.168.255.9')

    r4.cmd('sysctl net.ipv4.ip_forward=1')
    r4.cmd('ip route add 0.0.0.0/0 via 192.168.255.13')

    net.pingAll()
    info('\n')
    a.cmdPrint('traceroute 192.168.2.20')  # Trace route from hostA to hostB
    info('\n')
    r4.cmdPrint('traceroute 192.168.0.10') # Trace route from R4 to hostA
    info('\n')

def generate_tcp_traffic(net, server='A', client='B', time=5, save_cap=False, cap_file='1301204395.pcap'):   # CLO 3
    '''
        Generate tcp traffic using iperf
    '''
    server, client = net.get(server, client)

    if save_cap:
        server.cmd(f'tcpdump tcp -c 20 -w {cap_file} &')
    else:
        server.cmd(f'tcpdump tcp -c 20 &')

    client.cmdPrint(f'iperf -c {server.IP()} -t {time} -i 1')
    info('\n')

    if save_cap:
        server.cmd('kill %tcpdump')
        server.cmdPrint(f'tcpdump -r {cap_file}')
    else:
        server.cmdPrint('fg %tcpdump')
    info('\n')

def generate_buffer_traffic(net, server='A', client='B', time=5, save_cap=False, buffer_sizes=(20,40,60,100)):   # CLO 4
    '''
        Generate tcp traffic(s) for each buffer size
    '''
    def change_buffer(router, size):
        'Change the queue buffer size for every interface on the router'
        for intf in router.intfNames():
            router.cmd(f'tc qdisc del dev {intf} root')
            router.cmd(f'tc qdisc add dev {intf} root handle 1: pfifo limit {size}')
    routers = ('R1', 'R2', 'R3', 'R4')
    
    for size in buffer_sizes:
        for router in routers:  # Change the queue buffer size on all routers
            change_buffer(net[router], size)
        info(f'\nTraffic for queue buffer {size} packets\n\n')
        net['R1'].cmdPrint('tc qdisc')
        info('\n')
        generate_tcp_traffic(net, server=server, client=client, time=time, save_cap=save_cap, cap_file=f'buffer_{size}.pcap')


def main():
    setLogLevel('info')

    #   Initializing network
    net = Mininet(Tubes())
    net.start()
    server='A'

    # info('\n\n')
    # info('CLO 1 : Pinging Local Subnet\n\n')
    # ping_local_subnet(net)
    # info('\n\n')

    info('CLO 2 : Enabling Routing\n\n')
    enable_routing(net)
    info('\n\n')

    with Iperf_Server(net, server):
        info('CLO 3 : Generating TCP Traffic\n\n')
        generate_tcp_traffic(net, server=server, save_cap=True)
        info('\n\n')

        info('CLO 4 : Generatic TCP Traffic with Modified Queue Buffer\n\n')
        generate_buffer_traffic(net, server=server, save_cap=True)
        info('\n\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()