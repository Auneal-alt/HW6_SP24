
from steam import steam

class rankine():
    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        '''
        Rankine power cycle formating
        '''
        self.p_low=p_low
        self.p_high=p_high
        self.t_high=t_high
        self.name=name
        self.efficiency=None
        self.turbine_work=0
        self.pump_work=0
        self.heat_added=0
        self.state1=None
        self.state2=None
        self.state3=None
        self.state4=None

    def calc_efficiency(self):
        # 4 states
        #state 1: inlet of turbine
        if(self.t_high==None):
            self.state1 = steam(self.p_high, x = 1, name = 'Turbine Inlet')

        else:
            self.state1= steam(self.p_high, T=self.t_high, name='Turbine Inlet')

        #state 2: exit of turbine
        self.state2= steam(self.p_low, s=self.state1.s, name='Turbine Exit')
        #state 3: inlet of pump
        self.state3= steam(self.p_low, x=0, name='Pump Inlet')
        #state 4: exit of pump
        self.state4=steam(self.p_high,s=self.state3.s, name='Pump Exit')
        self.state4.h=self.state3.h+self.state3.v*(self.p_high-self.p_low)

        self.turbine_work= self.state1.h - self.state2.h
        self.pump_work= self.state4.h - self.state3.h
        self.heat_added= self.state1.h - self.state4.h
        self.efficiency=100.0*(self.turbine_work - self.pump_work)/self.heat_added
        return self.efficiency

    def print_summary(self):

        if self.efficiency==None:
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
    rankine1= rankine(8, 8000, t_high=500, name='Rankine Cycle - Superheated at Turbine Inlet')
    eff=rankine1.calc_efficiency()
    print(eff)
    rankine1.print_summary()

if __name__=="__main__":
    main()
