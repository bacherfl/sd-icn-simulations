
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

    # add nodes
    # switches first
    s1 = topology.addSwitch( 's1' )
    s2 = topology.addSwitch( 's2' )
    s3 = topology.addSwitch( 's3' )
    s4 = topology.addSwitch( 's4' )
    s5 = topology.addSwitch( 's5' )
    s6 = topology.addSwitch( 's6' )
    s7 = topology.addSwitch( 's7' )
    s8 = topology.addSwitch( 's8' )
    s9 = topology.addSwitch( 's9' )
    s10 = topology.addSwitch( 's10' )
    s11 = topology.addSwitch( 's11' )
    s12 = topology.addSwitch( 's12' )
    s13 = topology.addSwitch( 's13' )

    # and now hosts
    h1 = topology.addHost( 'h1', mac='00:00:00:00:00:01' )
    h2 = topology.addHost( 'h2', mac='00:00:00:00:00:02' )
    h3 = topology.addHost( 'h3', mac='00:00:00:00:00:03' )
    h4 = topology.addHost( 'h4', mac='00:00:00:00:00:04' )
    h5 = topology.addHost( 'h5', mac='00:00:00:00:00:05' )
    h6 = topology.addHost( 'h6', mac='00:00:00:00:00:06' )
    h7 = topology.addHost( 'h7', mac='00:00:00:00:00:07' )
    h8 = topology.addHost( 'h8', mac='00:00:00:00:00:08' )
    h9 = topology.addHost( 'h9', mac='00:00:00:00:00:09' )
    h10 = topology.addHost( 'h10', mac='00:00:00:00:00:0A' )
    h11 = topology.addHost( 'h11', mac='00:00:00:00:00:0B' )
    h12 = topology.addHost( 'h12', mac='00:00:00:00:00:0C' )
    h13 = topology.addHost( 'h13', mac='00:00:00:00:00:0D' )
    h14 = topology.addHost( 'h14', mac='00:00:00:00:00:0E' )
    h15 = topology.addHost( 'h15', mac='00:00:00:00:00:0F' )

    sv1 = topology.addHost( 'sv1', mac='00:00:00:00:00:10' )
    sv2 = topology.addHost( 'sv2', mac='00:00:00:00:00:11' )
    sv3 = topology.addHost( 'sv3', mac='00:00:00:00:00:12' )

    p1 = topology.addHost( 'p1', mac='00:00:00:00:00:13' ) 
    p2 = topology.addHost( 'p2', mac='00:00:00:00:00:14' )
    p3 = topology.addHost( 'p3', mac='00:00:00:00:00:15' )

    a1 = topology.addHost( 'a1', mac='00:00:00:00:00:16' )
 
    # add edges between switch and corresponding host
    topology.addLink( s1 , h1 )
    topology.addLink( s1 , h2 )
    topology.addLink( s1 , h3 )
    topology.addLink( s1 , s7 )
    topology.addLink( s7 , s2 )
    topology.addLink( s2 , h4 )
    topology.addLink( s2 , h5 )
    topology.addLink( s7 , s9 )
    topology.addLink( s7 , s9 )
    topology.addLink( s7 , p1 )
    topology.addLink( s9 , p2 )
    topology.addLink( s9 , s8 )
    topology.addLink( s9 , s11 )
    topology.addLink( s8 , s3 )
    topology.addLink( s3 , h6 )
    topology.addLink( s3 , h7 )
    topology.addLink( s3 , h8 )
    topology.addLink( s3 , h9 )
    topology.addLink( s8 , s4 )
    topology.addLink( s4 , h10 )
    topology.addLink( s4 , s5 )
    topology.addLink( s5 , h11 )
    topology.addLink( s5 , h12 )
    topology.addLink( s4 , s6 )
    topology.addLink( s6 , h13 )
    topology.addLink( s6 , h14 )
    topology.addLink( s6 , h15 )
    topology.addLink( s8 , s11 )
    topology.addLink( s8 , s10 )
    topology.addLink( s11 , sv1 )
    topology.addLink( s11 , a1 )
    topology.addLink( s11 , s13 )
    topology.addLink( s13 , sv2 )
    topology.addLink( s10 , s12 )
    topology.addLink( s10 , p3 )
    topology.addLink( s12 , sv3 )

    # Add links Mbps, ms delay, 10% loss
    linkopts = dict(bw=1000, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
    #linkopts = dict()


    
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

    p1 = net.get('p1')
    p1.cmd('java -jar proxy-0.0.1-SNAPSHOT.jar 10000 10.0.0.1 &') 

    a1 = net.get('a1')
    a1.cmd('java -jar sdicn-0.0.1-SNAPSHOT.jar &')

    sv1 = net.get('sv1')
    sv1.cmd('java -jar server-0.0.1-SNAPSHOT.jar --ip=10.0.0.20 --server.port=9004 --sdicnapp.location=10.0.0.1:6666 &')

    sv2 = net.get('sv2')
    sv2.cmd('java -jar server-0.0.1-SNAPSHOT.jar --ip=10.0.0.21 --server.port=9005 --sdicnapp.location=10.0.0.1:6666 &')
    
    net.pingAll()

    time.sleep(120)

    sv1.cmd("curl -i -F name=content1 -F file=@foo http://10.0.0.20:9004/upload")
    sv2.cmd("curl -i -F name=content2 -F file=@foo http://10.0.0.21:9005/upload")
    
    CLI(net)
    call("fuser -k 6633/tcp", shell=True)
         
    net.stop()    
    
