
from mininet.net import Mininet
from mininet.topo import *
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from subprocess import call
from functools import partial
import sys
import httplib,json, time

def add_topo_host(topo, id_host):
    topo.add_host('h%s' %str(id_host), mac='00:00:00:00:00:0%s' %str(id_host))

#build topology
def buildTopo():
    print 'init topology'
    topology=Topo()

    h1 = topology.addHost( 'h1', mac='00:00:00:00:00:01' )
    h2 = topology.addHost( 'h2', mac='00:00:00:00:00:02' )
    h3 = topology.addHost( 'h3', mac='00:00:00:00:00:03' )
    h4 = topology.addHost( 'h4', mac='00:00:00:00:00:04' )
    h5 = topology.addHost( 'h5', mac='00:00:00:00:00:05' )    
    
    s1 = topology.addSwitch( 's1' )
    s2 = topology.addSwitch( 's2' )


    # Add links Mbps, ms delay, 10% loss
    linkopts = dict(bw=1000, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
    #linkopts = dict()

    # alternately: linkopts = {'bw':10, 'delay':'5ms', 'loss':10,
    # max_queue_size=1000, 'use_htb':True}

    print 'init link'
    topology.addLink( h1, s1, **linkopts)
    topology.addLink( h2, s2, **linkopts)
    topology.addLink( s1, s2, **linkopts)
    topology.addLink( h3, s1, **linkopts)
    topology.addLink( h4, s2, **linkopts)
    topology.addLink( h5, s1, **linkopts)

    
    return topology

call("mn -c", shell=True)
 
net = Mininet(controller=partial( RemoteController, ip='127.0.0.1', port=6653 ), topo=buildTopo(), link=TCLink, switch=OVSKernelSwitch)

def start_proxy():
    h1 = net.get('h1')
    h1.cmd('java -jar proxy.jar &')

def start_server():
    h4 = net.get('h4')
    #h4.cmd('java -jar server.jar &')



def djb2(uuid):
    """ See for details: http://www.cse.yorku.ca/~oz/hash.html """

    _hash = 5381

    for i in xrange(0, len(uuid)):
        _hash = ((_hash << 5) + _hash) + ord(uuid[i])

    return _hash

if __name__ == '__main__':
    

    net.start()
    #test ping
#    net.pingAll()

    #start_proxy()
    #start server
    call("sh ./install-tools.sh", shell=True)

    h1 = net.get('h1')
    h1.cmd('java -jar proxy-0.0.1-SNAPSHOT.jar 10000 10.0.0.2 &') 

    h2 = net.get('h2')
    h2.cmd('java -jar sdicn-0.0.1-SNAPSHOT.jar &')

    h4 = net.get('h4')
    h4.cmd('java -jar server-0.0.1-SNAPSHOT.jar --ip=10.0.0.4 --server.port=9004 --sdicnapp.location=10.0.0.2:6666 &')

    h5 = net.get('h5')
    h5.cmd('java -jar server-0.0.1-SNAPSHOT.jar --ip=10.0.0.5 --server.port=9005 --sdicnapp.location=10.0.0.2:6666 &')
    
    net.pingAll()

    time.sleep(120)

    h4.cmd("curl -i -F name=content4 -F file=@foo http://10.0.0.4:9004/upload")
    h5.cmd("curl -i -F name=content5 -F file=@foo http://10.0.0.5:9005/upload")
    
    CLI(net)
    call("fuser -k 6633/tcp", shell=True)
         
    net.stop()    
    
