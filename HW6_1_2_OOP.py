# region imports
import numpy as np
from scipy.optimize import fsolve

from HW6_1_OOP import ResistorNetwork, VoltageSource, Resistor, Loop


# endregion


class ResistorNetwork2(ResistorNetwork, Loop, Resistor, VoltageSource):

    # region class definitions

    def AnalyzeCircuit(self):
        """
        Use fsolve to find currents in the resistor network.
        1. KCL:  The total current flowing into any node in the network is zero.
        2. KVL:  When traversing a closed loop in the circuit, the net voltage drop must be zero.
        :return: a list of the currents in the resistor network
        """
        # need to set the currents to that Kirchoff's laws are satisfied
        i0 = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # JES MISSING CODE  #define an initial guess for the currents
        i = fsolve(self.GetKirchoffVals, i0)  # I imported numpy because I0 wanted an ndarray
        # print output to the screen
        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        print("I4 = {:0.1f}".format(i[3]))
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
        self.GetResistorByName('ed').Current = i[3]  #
        # calculate net current into node c
        Node_c_Current = sum([i[0], i[1], -i[2]])

        KVL = self.GetLoopVoltageDrops()  # two equations here
        KVL.append(Node_c_Current)  # one equation here
        return KVL

# region Function Definitions
def main():
    """
    This program solves for the unknown currents in the circuit of the homework assignment.
    :return: nothing
    """
    Net = ResistorNetwork2()  # JES MISSING CODE  #Instantiate a resistor network object
    Net.BuildNetworkFromFile("ResistorNetwork_2.txt")  # JES MISSING CODE #call the function from Net
    # that builds the resistor network from a text file
    IVals = Net.AnalyzeCircuit()


# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
