import numpy as np
import math
from scipy.optimize import fsolve
import random as rnd
class Fluid():
    def __init__(self, mu=0.00089, rho=1000):
        '''
        properties  for water
        '''
        self.mu= mu
        self.rho= rho
        self.nu= mu/rho
class Node():
    def __init__(self, Name='a', Pipes=[], ExtFlow=0):
        '''
        A node
        '''
        self.name=Name
        self.pipes=Pipes
        self.extFlow=ExtFlow

    def getNetFlowRate(self):
        '''
        Net flow rate into this node in L/s
        '''
        Qtot= self.extFlow #$JES MISSING CODE$  #count the external flow first
        for p in self.pipes:

            Qtot+=p.getFlowIntoNode(self.name)
        return Qtot
class Loop():
    def __init__(self, Name='A', Pipes=[]):
        '''
        Defines a loop in the pipe
        '''
        self.name=Name
        self.pipes=Pipes

    def getLoopHeadLoss(self):
        '''
        Calculates the net head loss as I traverse around the loop, in m of fluid.
        :return:
        '''
        deltaP=0 #initialize to zero
        startNode=self.pipes[0].startNode #begin at the start node of the first pipe
        for p in self.pipes:
            # calculates the head loss in the pipe considering loop traversal and flow directions
            phl=p.getFlowHeadLoss(startNode)
            deltaP+=phl
            startNode=p.endNode if startNode!=p.endNode else p.startNode #move to the next node
        return deltaP
class Pipe():
    def __init__(self, Start='A', End='B',L=100, D=200, r=0.00025, fluid=Fluid()):
        '''
        Defines the pipe
        '''

        self.startNode=min(Start,End) #lowest letter for startNode
        self.endNode=max(Start,End) # highest letter for endNode
        self.length=L
        self.r=r
        self.fluid=fluid

        self.d=D/1000.0 #diameter
        self.relrough = self.r/self.d # roughness
        self.A=math.pi/4.0*self.d**2 #pipe cross-sectional area
        self.Q=10
        self.vel=self.V()  #initial velocity
        self.reynolds=self.Re() #initial reynolds number

    def V(self):
        '''
        average velocity in the pipe
        '''
        self.vel= ((self.Q/1000) / self.A)

        return self.vel

    def Re(self):
        '''
        reynolds number
        '''
        self.reynolds= (self.V()*self.length)/0.00000089
        return self.reynolds

    def FrictionFactor(self):
        """
         friction factor
        """
        # Reynolds number
        Re=self.Re()
        rr=self.relrough

        def CB():

            cb = lambda f: 1 / (f ** 0.5) + 2.0 * np.log10(rr / 3.7 + 2.51 / (Re * f ** 0.5))
            result = fsolve(cb, (0.01))
            val = cb(result[0])
            return result[0]

        def lam():
            return 64 / Re

        if Re >= 4000:  #turb flow
            return CB()
        if Re <= 2000: #laminor
            return lam()


        CBff = CB()
        Lamff = lam()

        mean = Lamff+((Re-2000)/(4000-2000))*(CBff - Lamff)
        sig = 0.2 * mean
        # normalvariate for random choice
        return rnd.normalvariate(mean, sig)

    def frictionHeadLoss(self):  # calculate headloss through a section of pipe in m of fluid
        '''
       head loss.
        '''
        g = 9.81  # m/s^2
        ff = self.FrictionFactor()
        hl = ff*(self.length/self.d) * (self.vel**2/(2*g)) #$JES MISSING CODE$ # calculate the head loss in m of water
        return hl

    def getFlowHeadLoss(self, s):
        '''
        head loss for the pipe.
        '''

        nTraverse= 1 if s==self.startNode else -1
        #if flow is positive  scalar =1 else =-1
        nFlow=1 if self.Q >= 0 else -1
        return nTraverse*nFlow*self.frictionHeadLoss()

    def Name(self):
        '''
         pipe name.
        '''
        return self.startNode+'-'+self.endNode

    def oContainsNode(self, node):
        #pipe connection?
        return self.startNode==node or self.endNode==node

    def printPipeFlowRate(self):
        print('The flow in segment {} is {:0.2f} L/s'.format(self.Name(),self.Q))

    def getFlowIntoNode(self, n):
        '''
         flow rate into node n
        '''
        if n==self.startNode:
            return -self.Q
        return self.Q

class PipeNetwork():
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        '''
        The pipe network
        '''
        self.loops=Loops
        self.nodes=Nodes
        self.Fluid=fluid
        self.pipes=Pipes

    def findFlowRates(self):
        '''
         find the flow rates in each pipe
        '''
        #nodes and loops are present?
        N=len(self.nodes)+len(self.loops)

        Q0=np.full(N,10)
        def fn(q):
            """
         callback for fsolve.
            """

            for i in range(len(self.pipes)):
                self.pipes[i].Q= q[i]

            L= self.getNodeFlowRates()
            #calculate the net head loss for the loop objects
            # note: when the flow rates in pipes are correct, the net head loss for each loop should be zero.
            L+= self.getLoopHeadLosses() #$JES MISSING CODE$  # call the getLoopHeadLoss function of this class
            return L
        #finding the flow rates
        FR=fsolve(fn,Q0)
        return FR

    def getNodeFlowRates(self):

        qNet=[n.getNetFlowRate() for n in self.nodes]
        return qNet

    def getLoopHeadLosses(self):

        lhl=[l.getLoopHeadLoss() for l in self.loops]
        return lhl

    def getPipe(self, name):
        #returns a pipe object
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        #returns a list of pipe objects
        l=[]
        for p in self.pipes:
            if p.oContainsNode(node):
                l.append(p)
        return l

    def nodeBuilt(self, node):

        for n in self.nodes:
            if n.name==node:
                return True
        return False

    def getNode(self, name):

        for n in self.nodes:
            if n.name==name:
                return n

    def buildNodes(self):

        for p in self.pipes:
            if self.nodeBuilt(p.startNode)==False:

                self.nodes.append(Node(p.startNode,self.getNodePipes(p.startNode)))
            if self.nodeBuilt(p.endNode)==False:

                self.nodes.append(Node(p.endNode,self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        for n in self.nodes:
            print('net flow into node {} is {:0.2f}'.format(n.name, n.getNetFlowRate()))

    def printLoopHeadLoss(self):
        for l in self.loops:
            print('head loss for loop {} is {:0.2f}'.format(l.name, l.getLoopHeadLoss()))

def main(water=None):
    '''
    program analyzes flows
    '''
    water = Fluid()
    roughness = 0.00025


    Pipes=[]
    Loops=[]
    PN= PipeNetwork(Pipes, Loops)

    PN.pipes.append(Pipe('a','b',250, 300, roughness, water))
    PN.pipes.append(Pipe('a','c',100, 200, roughness, water))
    PN.pipes.append(Pipe('b','e',100, 200, roughness, water))
    PN.pipes.append(Pipe('c','d',125, 200, roughness, water))
    PN.pipes.append(Pipe('c','f',100, 150, roughness, water))
    PN.pipes.append(Pipe('d','e',125, 200, roughness, water))
    PN.pipes.append(Pipe('d','g',100, 150, roughness, water))
    PN.pipes.append(Pipe('e','h',100, 150, roughness, water))
    PN.pipes.append(Pipe('f','g',125, 250, roughness, water))
    PN.pipes.append(Pipe('g','h',125, 250, roughness, water))
    #add Node objects to the pipe network by calling buildNodes method of PN object
    PN.buildNodes()


    PN.getNode('d').extFlow=-30
    PN.getNode('f').extFlow=-15
    PN.getNode('h').extFlow=-15

    #add Loop objects
    PN.loops.append(Loop('A',[PN.getPipe('a-b'), PN.getPipe('b-e'),PN.getPipe('d-e'), PN.getPipe('c-d'), PN.getPipe('a-c')]))
    PN.loops.append(Loop('B',[PN.getPipe('c-d'), PN.getPipe('d-g'),PN.getPipe('f-g'), PN.getPipe('c-f')]))
    PN.loops.append(Loop('C',[PN.getPipe('d-e'), PN.getPipe('e-h'),PN.getPipe('g-h'), PN.getPipe('d-g')]))

    #call the findFlowRates method
    PN.findFlowRates()

    #get output
    PN.printPipeFlowRates()
    print()
    print('Check node flows:')
    PN.printNetNodeFlows()
    print()
    print('Check loop head loss:')
    PN.printLoopHeadLoss()
    #PN.printPipeHeadLosses()

main()
