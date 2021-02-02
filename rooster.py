#--------------------------------------------------------------------------------------------------
# TREE OF CLASSES:
#     Reactor
#         Solid
#             FuelElement
#             Structure
#         Fluid
#         Neutron
#             PointKinetics
#             SpatialKinetics
#         Control
#             Detector
#             Controller
#--------------------------------------------------------------------------------------------------
from control import Control
from dumka3 import dumka3
from fluid import Fluid
from neutron import Neutron
from solid import Solid

# SciPy requires installation : 
#     python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
from scipy.integrate import ode

#--------------------------------------------------------------------------------------------------
class Reactor:
    def __init__(self):
        # create objects
        self.control = Control(self)
        self.solid = Solid(self)
        self.fluid = Fluid(self)
        self.neutron = Neutron(self)
        # initialize state: a vector of variables
        self.state = self.control.state + self.solid.state + self.fluid.state + self.neutron.state
        solve(self)

#--------------------------------------------------------------------------------------------------
def solve(reactor):

    def construct_rhs(t, y):
        reactor.state = y
        reactor.control.evaluate(reactor, t)
        rhs = []
        rhs += reactor.solid.calculate_rhs(reactor, t)
        rhs += reactor.fluid.calculate_rhs(reactor, t)
        rhs += reactor.neutron.calculate_rhs(reactor, t)
        rhs += reactor.control.calculate_rhs(reactor, t)
        return rhs

#    solver = ode(construct_rhs, jac = None).set_integrator('lsoda', method = 'bdf')
#    t0 = reactor.control.input['t0']
#    solver.set_initial_value(reactor.state, t0)
#    solver.set_integrator
#    for t_dt in reactor.control.input['t_dt'] :
#       tend = t_dt[0]
#       dtout = t_dt[1]
#       while solver.successful() and solver.t < tend:
#           time = solver.t + dtout
#           reactor.state = solver.integrate(time)
#           print(time, reactor.state)

    inp = {}
    inp['tstart'] = 0
    inp['tend'] = 10
    inp['y'] = reactor.state
    inp['h0'] = 1e-6
    inp['rhs'] = construct_rhs
    
    with open('coef', mode = 'r') as f :
        string = f.read()
    arr = string.split('\n')
    inp['C_1'] = []
    inp['C_2'] = []
    inp['C_3'] = []
    inp['C_4'] = []
    inp['C_5'] = []
    inp['C_6'] = []
    for a in arr :
        aa = a.strip().split()
        inp['C_1'].append(float(aa[0]))
        inp['C_2'].append(float(aa[1]))
        inp['C_3'].append(float(aa[2]))
        inp['C_4'].append(float(aa[3]))
    inp['rtol'] = [1e-10] * len(reactor.state)
    inp['atol'] = [1e-3] * len(reactor.state)

    dumka3(inp)
#--------------------------------------------------------------------------------------------------
# create and solve
reactor = Reactor()
