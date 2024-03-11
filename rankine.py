# Each Problem was collaborated with Marlesha Ellis and I(Austin Neal). Primary form of communication was Discord
# However when we remembered to we would send our files to the github so it may look inconsistent on the timeline.

from steam import steam


class rankine():
    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        '''
         Constructor for rankine power cycle.  If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param name: a convenient name
        '''
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.name = name
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.state4 = None

    def calc_efficiency(self):
        """Calcuates efficiency of te cycle"""
        # 4 states
        # state 1: inlet of turbine
        if (self.t_high == None):
            self.state1 = steam(self.p_high, x=1, name='Turbine Inlet')

        else:
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')

        # state 2: exit of turbine
        self.state2 = steam(self.p_low, s=self.state1.s, name='Turbine Exit')
        # state 3: inlet of pump
        self.state3 = steam(self.p_low, x=0, name='Pump Inlet')
        # state 4: exit of pump
        self.state4 = steam(self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low)

        self.turbine_work = self.state1.h - self.state2.h
        self.pump_work = self.state4.h - self.state3.h
        self.heat_added = self.state1.h - self.state4.h
        self.efficiency = 100.0 * (self.turbine_work - self.pump_work) / self.heat_added
        return self.efficiency

    def print_summary(self):
        """ prints the summary of calculations and values"""

        if self.efficiency == None:
            self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()


def main():
    """main problem statement"""
    rankine1 = rankine(8, 8000, t_high=500, name='Rankine Cycle - Superheated at Turbine Inlet')
    eff = rankine1.calc_efficiency()
    print(eff)
    rankine1.print_summary()


if __name__ == "__main__":
    main()
