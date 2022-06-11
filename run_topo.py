'''
    Script made to run tubes' topology
    - Yasir Khairul Malik (1301204395)
'''

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

from topology import Tubes


def ping_local_subnet(net): # CLO1
    '''
        Ping all subnet in tubes' topology locally
    '''
    A, B, R1, R2, R3, R4 = net.get('A', 'B', 'R1', 'R2', 'R3', 'R4')
    A.cmdPrint('ping -c 4 192.168.0.1')     # A to R!
    A.cmdPrint('ping -c 4 192.168.1.1')     # A to R2
    B.cmdPrint('ping -c 4 192.168.2.1')     # B to R3
    B.cmdPrint('ping -c 4 192.168.3.1')     # B to R4
    R1.cmdPrint('ping -c 4 192.168.255.2')  # R1 to R3
    R1.cmdPrint('ping -c 4 192.168.255.6')  # R1 to R4
    R2.cmdPrint('ping -c 4 192.168.255.10') # R2 to R3
    R2.cmdPrint('ping -c 4 192.168.255.14') # R2 to R4

def main():
    setLogLevel('info')
    net = Mininet(Tubes())
    net.start()
    ping_local_subnet(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()