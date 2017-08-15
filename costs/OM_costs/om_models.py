from costs.currency import Cost1
from farm_description import OandM_costs, availability

def oandm(aep, aeroloads, hydroloads, layout):
    costs_om = 16.0 * aep / 1000000.0
    avail = 0.98
    return costs_om, avail


def oandm_given_costs(aep, aeroloads, hydroloads, layout):
    return OandM_costs, availability


def oandm2(aep):
    return Cost1(0.0283, "USD", 2013) * aep

if __name__ == '__main__':
    print oandm2(672000000)
