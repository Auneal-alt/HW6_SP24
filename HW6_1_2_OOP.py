# Each Problem was collaborated with Marlesha Ellis and I(Austin Neal). Primary form of communication was Discord
# However when we remembered to we would send our files to the github so it may look inconsistent on the timeline.
# region imports
import numpy as np
from scipy.optimize import fsolve
from HW6_1_OOP import ResistorNetwork


class ResistorNetwork2(ResistorNetwork):  # Inherit from ResistorNetwork
    def __init__(self):
        """
        The resistor network consists of Loops, Resistors and Voltage Sources.
        This is the constructor for the network and it defines fields for Loops, Resistors and Voltage Sources."""
        # create some instance variables that are logical parts of a resistor network
        super().__init__()   # not sure, saw it on your bolt example so I added it.

    def GetLoopVoltageDrops(self):
        """
        This calculates the net voltage drop around a closed loop in a circuit based on the
        current flowing through resistors (cause a drop in voltage regardless of direction of traversal) or
        the value of the voltage source that have been set up as positive based on the direction of traversal.
        :return: net voltage drop for all loops in the network.
        """
        loopVoltages = []
        for L in self.Loops:
            # Traverse loops in order of nodes and add up voltage drops between nodes
            loopDeltaV = 0
            for n in range(len(L.Nodes)):
                if n == len(L.Nodes) - 1:
                    name = L.Nodes[0] + L.Nodes[n]
                else:
                    name = L.Nodes[n] + L.Nodes[n + 1]

                deltaV = self.GetElementDeltaV(name)

                if deltaV is not None:
                    loopDeltaV += deltaV  # when I requested help from chatgpt about a different problem on line 81
                    # it also recommended this change and as I was desperate for my code to run
                    # I went ahead and added it in, it just checks if the self.GeetEle... is none

            loopVoltages.append(loopDeltaV)
        return loopVoltages

    def AnalyzeCircuit(self):
        """
        Use fsolve to find currents in the resistor network for the modified circuit with 5 currents.
        :return: a list of the currents in the resistor network
        """
        # need to set the currents to that Kirchoff's laws are satisfied
        i0 = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # JES MISSING CODE  # Update the initial guess for 5 currents
        i = fsolve(self.GetKirchoffVals, i0)  # I imported numpy because I0 wanted an ndarray
        # print output to the screen
        print("For Circuit 2:")  # The modified or second circuit had 5 currents listed so each one was given a name
        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        print("I4 = {:0.1f}".format(i[3]))  # not sure why its giving me the yellow error here but not on the others?
        print("I5 = {:0.1f}".format(i[4]))
        return i

    def GetKirchoffVals(self, i):
        """
        This function uses Kirchoff Voltage and Current laws to analyze this specific circuit
        KVL:  The net voltage drop for a closed loop in a circuit should be zero
        KCL:  The net current flow into a node in a circuit should be zero
        :param i: a list of currents relevant to the circuit
        :return: a list of loop voltage drops and node currents
        """
        # set current in resistors in the top loop.
        self.GetResistorByName('ad').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('bc').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('cd').Current = i[2]  # I_3 in diagram
        # set current in resistor in middle Loop.
        self.GetResistorByName('ce').Current = i[4]  # I_5 in diagram
        # set current in new resistor in bottom Loop
        self.GetResistorByName('ed').Current = i[3]  # I_4 in diagram
        # set current for current through bottom voltage source
        self.GetResistorByName('df').Current = i[1]  # I_2 in diagram
        # calculate net currents into nodes c, d, and e
        Node_c_Current = sum([i[4], i[0], -i[2]])
        Node_d_Current = sum([i[2], i[3], -i[0], -i[1]])
        Node_e_Current = sum([i[1], -i[3], i[4]])

        KVL = self.GetLoopVoltageDrops()  # three equations here
        return np.array(KVL + [Node_c_Current, Node_d_Current, Node_e_Current])[:5]  # return only the first 5 equations
        # I couldnt get this code to finish for the life of me but chatgpt managed to get it to run by limiting it to
        # 5 equations and as I run out of time, I got to take what I can get and figure out why its wrong later.


# endregion

# region Function Definitions
def main():
    """
    This program solves for the unknown currents in the circuit of the homework assignment.
    :return: nothing
    """
    Net = ResistorNetwork()  # JES MISSING CODE  #Instantiate a resistor network object
    Net.BuildNetworkFromFile("ResistorNetwork_1.txt")  # JES MISSING CODE #call the function from Net
    # that builds the resistor network from a text file
    IVals = Net.AnalyzeCircuit()

    Net2 = ResistorNetwork2()  # Instantiate ResistorNetwork2 object
    Net2.BuildNetworkFromFile("ResistorNetwork_2.txt")  # Build the resistor network from a text file
    IVals2 = Net2.AnalyzeCircuit()  # Analyze the modified circuit with 5 currents


# endregion

# region function calls
if __name__ == "__main__":
    main()
