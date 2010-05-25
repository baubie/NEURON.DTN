from neuron import *
from math import sqrt
from models import Onset

# Convert from nanosiemens to mho/cm2
def nstomho(ns,somaarea):
    return ((1E-9)*ns)/somaarea

# Parameters
speccm = 0.9
pi = 3.14159
totcap = 12 # Total capacity in pF for cell
somaarea = totcap * (1E-6) # pF -> uF, assume 1 uF/cm2; result is in cm2
lstd = 1E4*sqrt(somaarea/pi)

# Build the soma
soma = Onset()

soma.L = lstd
soma.diam = lstd
soma.nseg = 1
soma.Ra = 150
soma.cm = speccm

soma.insert('klt')
soma.insert('kht')
soma.insert('na')
soma.insert('ka')
soma.insert('ih')
soma.insert('leak')

soma(0.5).leak.g = 1/10000 
soma(0.5).leak.erev = -65
soma(0.5).ek = -70
soma(0.5).ena = 50

# Setup onset cell
soma(0.5).na.gnabar = nstomho(1000, somaarea)
soma(0.5).kht.gkhtbar = nstomho(150, somaarea)
soma(0.5).klt.gkltbar = nstomho(200, somaarea)
soma(0.5).ka.gkabar = nstomho(0, somaarea)
soma(0.5).ih.ghbar = nstomho(20, somaarea)
soma(0.5).leak.g = nstomho(2, somaarea)
h.celsius = 22


# Create the stimulus
stim = h.IClamp(0.5, sec=soma)
stim.delay = 5.0
stim.dur = 100.0
stim.amp = 0.3


# Create a synapse
#synA = h.ExpSyn(0.5, sec=soma2)
#synB = h.ExpSyn(0.5, sec=soma3)

# Connect the neurons together
#ncA = h.NetCon(axon(1)._ref_v, synA)
#ncB = h.NetCon(axon(1)._ref_v, synB)
#ncA.weight[0] = 2.0
#ncB.weight[0] = 5.0

# Record the shizzle
vec = {}
for var in 'v_soma', 'v_soma2', 'v_soma3', 't', 'i':
    vec[var] = h.Vector()
    
vec['v_soma'].record(soma(0.5)._ref_v)
#vec['v_soma2'].record(soma2(0.5)._ref_v)
#vec['v_soma3'].record(soma3(0.5)._ref_v)
vec['t'].record(h._ref_t)
vec['i'].record(stim._ref_i)

# run the stimulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 150.0
h.run()


# plot the results baby
import pylab

pylab.subplot(2,1,1)
pylab.plot(vec['t'], vec['i'])

pylab.subplot(2,1,2)
pylab.plot(vec['t'], vec['v_soma'])

#pylab.subplot(4,1,3)
#pylab.plot(vec['t'], vec['v_soma2'])

#pylab.subplot(4,1,4)
#pylab.plot(vec['t'], vec['v_soma3'])

pylab.show()
