# Each Problem was collaborated with Marlesha Ellis and I(Austin Neal). Primary form of communication was Discord
# However when we remembered to we would send our files to the github so it may look inconsistent on the timeline.

from rankine import rankine

def main():
    """Testing the Rankine cycle"""
    R1=rankine(p_high=8000, p_low=8, name='Rankine cycle - saturated steam inlet')
    R1.calc_efficiency()

    Tsat=R1.state1.T
    R2=rankine(p_high=8000, p_low=8, t_high=1.7*Tsat, name='Rankine cycle - superheated steam inlet')
    R2.calc_efficiency()

    R1.print_summary()
    R2.print_summary()

if __name__=="__main__":
    main()
