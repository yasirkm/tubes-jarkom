from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class Tubes(Topo):
    def build(self):
        host_param = {'cls':CPULimitedHost}
        router_param = {'cls':CPULimitedHost}

        hosts = ('A', 'B')
        routers = ('R1', 'R2', 'R3', 'R4')

        link_pairs = (
            ('A','R1'),
            ('A','R2'),
            ('B','R3'),
            ('B','R4'),
            ('R1','R4'),
            ('R2','R3'),
            ('R1','R3'),
            ('R2','R4')
        )
        link_params = {
            {
                # Parameters for ('A','R1')
                'params1':{
                    'ip':'192.168.0.10/24'
                },
                'params2':{
                    'ip':'192.168.0.1/24'
                },
                'cls':TCLink,
                'bw':1
            },
                # Parameters for ('A','R2')
            {
                'params1':{
                    'ip':'192.168.1.10/24'
                },
                'params2':{
                    'ip':'192.168.1.1/24'
                },
                'cls':TCLink,
                'bw':1
            },
                # Parameters for ('B','R3')
            {
                'params1':{
                    'ip':'192.168.2.20/24'
                },
                'params2':{
                    'ip':'192.168.2.1/24'
                },
                'cls':TCLink,
                'bw':1
            },
                # Parameters for ('B','R4')
            {
                'params1':{
                    'ip':'192.168.3.20/24'
                },
                'params2':{
                    'ip':'192.168.3.1/24'
                },
                'cls':TCLink,
                'bw':1
            },
                # Parameters for ('R1','R4')
            {
                'params1':{
                    'ip':'192.168.255.5/30'
                },
                'params2':{
                    'ip':'192.168.255.6/30'
                },
                'cls':TCLink,
                'bw':1
            },
                # Parameters for ('R2','R3'),
            {
                'params1':{
                    'ip':'192.168.255.9/30'
                },
                'params2':{
                    'ip':'192.168.255.10/30'
                },
                'cls':TCLink,
                'bw':1
            },
                # Parameters for ('R1','R3')
            {
                'params1':{
                    'ip':'192.168.255.1/30'
                },
                'params2':{
                    'ip':'192.168.255.2/30'
                },
                'cls':TCLink,
                'bw':0.5
            },
                # Parameters for ('R2','R4')
            {
                'params1':{
                    'ip':'192.168.255.13/30'
                },
                'params2':{
                    'ip':'192.168.255.14/30'
                },
                'cls':TCLink,
                'bw':0.5
            }
        }

        for host in hosts:
            self.addHost(host, **host_param)
        
        for router in routers:
            self.addNode(router, **router_param)

        for node1, node2, param in zip(link_pairs,link_params):
            self.addLink(node1, node2, **param)

def main():
    net = Mininet(Tubes)
    net.run()

