from neuron import hclass, h
import nrn
from math import sqrt

class IC_DTN(nrn.Section):
    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        

        self.insert('hhfast')        
        self.insert('pas')
        
        # Parameters
        lstd = 18
        
        self.L = lstd
        self.diam = lstd
        self.nseg = 1

        self(0.5).hhfast.gnabar = 0.12
        self(0.5).hhfast.gkbar = 0.036 
        self(0.5).ena = 50
        self(0.5).ek = -90
                  
    def nstomho(self, ns):
        return 1.0*((1E-9)*ns)/self.somaarea

class IC_DTNLarge(nrn.Section):
    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        

        self.insert('hhfast')
        self.insert('pas')
        
        # Parameters
        lstd = 24
        
        self.L = lstd
        self.diam = lstd
        self.nseg = 1

        self(0.5).hhfast.gnabar = 0.12
        self(0.5).hhfast.gkbar = 0.036 
        self(0.5).ena = 50
        self(0.5).ek = -90
                  
    def nstomho(self, ns):
        return 1.0*((1E-9)*ns)/self.somaarea

class Primary(nrn.Section):
    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        

        self.insert('hhfast')
        self.insert('pas')
        
        # Parameters
        lstd = 18
        self.L = lstd
        self.diam = lstd
        self.nseg = 1

        self(0.5).hhfast.gnabar = 0.15
        self(0.5).hhfast.gkbar = 0.036
        self(0.5).ena = 55
        self(0.5).ek = -90

class PrimaryLarge(nrn.Section):
    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        

        self.insert('hhfast')
        self.insert('pas')
        
        # Parameters
        lstd = 24
        self.L = lstd
        self.diam = lstd
        self.nseg = 1

        self(0.5).hhfast.gnabar = 0.150
        self(0.5).hhfast.gkbar = 0.036
        self(0.5).ena = 50
        self(0.5).ek = -90

class Onset(nrn.Section):
    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        

        self.insert('klt')
        self.insert('hhfast')
        self.insert('pas')
        lstd = 18
        self.L = lstd
        self.diam = lstd
        self.nseg = 1

        self(0.5).klt.gkltbar = 0.015
        self(0.5).hhfast.gnabar = 0.150
        self(0.5).hhfast.gkbar = 0.036
        self(0.5).ena = 50
        self(0.5).ek = -90
                  

















# Models from Rothman and Manis (2003)
class BaseModel(nrn.Section):
    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        
       
        # Insert membrane mechanisms
        self.insert('klt')
        self.insert('kht')
        self.insert('na')
        self.insert('ka')
        self.insert('leak')        

        # Parameters
        speccm = 0.9
        pi = 3.14159
        totcap = 12 # Total capacity in pF for cell
        self.somaarea = totcap * (1E-6) # pF -> uF, assume 1 uF/cm2; result is in cm2
        lstd = 1E4*sqrt(self.somaarea/pi)
        
        self.L = lstd
        self.diam = lstd
        self.nseg = 1
        self.Ra = 220
        self.cm = speccm
    
    def nstomho(self, ns):
        return 1.0*((1E-9)*ns)/self.somaarea

class Rebound(nrn.Section):

    def __init__(self):
        nrn.Section.__init__(self)

        # Provide recording variables
        self.rec_v = h.Vector()
        self.rec_v.record(self(0.5)._ref_v)        

        self.insert('ih2')
        self.insert('hhfast')
        self.insert('pas')
        
        # Parameters
        lstd = 14
        self.L = lstd
        self.diam = lstd
        self.nseg = 1

        self(0.5).ih2.ghbar = 0.0010
        self(0.5).ih2.eh = 10
        self(0.5).hhfast.gnabar = 0.120
        self(0.5).hhfast.gkbar = 0.036
        self(0.5).ena = 50
        self(0.5).ek = -90

# Based on type II

class FastRebound(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.insert('ih2')
        self(0.5).na.gnabar = self.nstomho(1000)
        self(0.5).kht.gkhtbar = self.nstomho(150)
        self(0.5).klt.gkltbar = self.nstomho(200)
        self(0.5).ka.gkabar = self.nstomho(0)
        self(0.5).ih2.ghbar = self.nstomho(25+205)
        self(0.5).ih2.eh = 10
        self(0.5).leak.g = self.nstomho(2)        
        self(0.5).leak.erev = -65
        self(0.5).ek = -90
        self(0.5).ena = 50    



# Based on type I-II
class OnsetB(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self(0.5).na.gnabar = self.nstomho(1000)
        self(0.5).kht.gkhtbar = self.nstomho(150)
        self(0.5).klt.gkltbar = self.nstomho(20)
        self(0.5).ka.gkabar = self.nstomho(0)
        self(0.5).leak.g = self.nstomho(2)        
        self(0.5).leak.erev = -65
        self(0.5).ek = -70
        self(0.5).ena = 50    

# Based on type II with I_LT = 0
class Normal(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self(0.5).na.gnabar = self.nstomho(1000)
        self(0.5).kht.gkhtbar = self.nstomho(150)
        self(0.5).klt.gkltbar = self.nstomho(20)
        self(0.5).ka.gkabar = self.nstomho(0)
        self(0.5).leak.g = self.nstomho(2)
        self(0.5).leak.erev = -65
        self(0.5).ek = -70
        self(0.5).ena = 50    
    
