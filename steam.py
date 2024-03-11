import numpy as np
from scipy.interpolate import griddata, interpolate

class steam():
    """
    thermodynamic properties of steam along an isobar.
    """
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        '''
        development  for steam
        '''
        #these are the properties
        self.p = pressure
        self.T = T
        self.x = x
        self.v = v
        self.h = h
        self.s = s
        self.name = name
        self.region = None
        if T==None and x==None and v==None and h==None and s==None: return
        else: self.calc()

    def calc(self):
        '''
        determing weather  saturated or superheated
        '''
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs= np.loadtxt("sat_water_table.txt", skiprows=1, unpack=True) #$JES MISSING CODE HERE$# #use np.loadtxt to read the saturated properties
        tcol, hcol, scol, pcol = np.loadtxt("superheated_water_table.txt", skiprows=1, unpack=True) #$JES MISSING CODE HERE$# #use np.loadtxt to read the superheated properties

        R=8.314/(18/1000) #gas constant for water
        Pbar=self.p/100 #pressure

        #saturated properties
        Tsat = float(griddata((ps), ts, (Pbar)))
        hf=float(griddata((ps),hfs,(Pbar)))
        hg=float(griddata((ps),hgs,(Pbar)))
        sf=float(griddata((ps),sfs,(Pbar)))
        sg=float(griddata((ps),sgs,(Pbar)))
        vf=float(griddata((ps),vfs,(Pbar)))
        vg=float(griddata((ps),vgs,(Pbar)))

        self.hf=hf # member variable


        if self.T is not None:
            if self.T>Tsat: #interpolate with griddata
                self.region='Superheated'
                self.h = float(griddata((tcol, pcol), hcol, (self.T, self.p)))
                self.s = float(griddata((tcol, pcol), scol, (self.T, self.p)))
                self.x=1.0
                TK = self.T + 273.14  # temperature to kelvin
                self.v=R*TK/(self.p*1000)  #volume ideal gas
        elif self.x!=None: # interpolation
            self.region='Saturated'
            self.T=Tsat
            self.h=hf+self.x*(hg-hf)
            self.s=sf+self.x*(sg-sf)
            self.v=vf+self.x*(vg-vf)
        elif self.h!=None:
            self.x=(self.h-hf)/(hg-hf)
            if self.x<=1.0: # interpolation
                self.region='Saturated'
                self.T=Tsat
                self.s=sf+self.x*(sg-sf)
                self.v=vf+self.x*(vg-vf)
            else: #interpolate with griddata
                self.region='Superheated'
                self.T = float(griddata((hcol, pcol), tcol, (self.h, self.p)))
                self.s = float(griddata((hcol, pcol), scol, (self.h, self.p)))
        elif self.s!=None:
            self.x=(self.s-sf)/(sg-sf)
            if self.x<=1.0: # interpolation
                self.region='Saturated'
                self.T=Tsat
                self.h=hf+self.x*(hg-hf)
                self.v=vf+self.x*(vg-vf)
            else: #interpolate with griddata
                self.region = 'Superheated'
                self.T = float(griddata((scol, pcol), tcol, (self.s, self.p)))
                self.h = float(griddata((scol, pcol), hcol, (self.s, self.p)))


    def print(self):
        """
        steam properties being printed
        """
        print('Name: ', self.name)
        if self.x<0.0: print('Region: compressed liquid')
        else: print('Region: ', self.region)
        print('p = {:0.2f} kPa'.format(self.p))
        if self.x >= 0.0: print('T = {:0.1f} degrees C'.format(self.T))
        print('h = {:0.2f} kJ/kg'.format(self.h))
        if self.x >= 0.0:
            print('s = {:0.4f} kJ/(kg K)'.format(self.s))
            if self.region == 'Saturated': print('v = {:0.6f} m^3/kg'.format(self.v))
            if self.region == 'Saturated': print('x = {:0.4f}'.format(self.x))
        print()

def main():
    inlet=steam(7350,name='Turbine Inlet')
    inlet.x=0.9 #90 percent
    inlet.calc()
    inlet.print()

    h1=inlet.h
    s1=inlet.s
    print(h1,s1,'\n')

    outlet=steam(100, s=inlet.s, name='Turbine Exit')
    outlet.print()

    another=steam(8575, h=2050, name='State 3')
    another.print()

    yetanother = steam(8575, h=3125, name='State 4')
    yetanother.print()


if __name__=="__main__":
    main()