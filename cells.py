import models as m
from neuron import h
from os import urandom
from random import uniform

class BaseNetwork:
    def __init__(self):
        self.cells = {}
        self.syn = {}
        self.nc = {}
        self.plots = {}
        self.input = [] 
        self.input_type = []
        self.input_delay = []
        self.input_size = []
        self.plot_order = []


class Bat(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['dtn']
        self.input = ['Onset','Offset','Sustain','OnsetInh']
        self.input_type = ['ON', 'OFF', 'SUS', 'ON']

        n = 1.0

        self.input_delay = [12.0+uniform(-n,n), 7.0+uniform(-n,n), 3.0, 3.0+uniform(-n,n)]
        self.input_size = [1, 2, 3, 3]

        # Create synapses on cells
        # AMPA Receptors
        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.1
        self.syn["dtn"]["AMPA"].tau2 = 1.5

        self.syn["dtn"]["NMDA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["NMDA"].e = -10
        self.syn["dtn"]["NMDA"].tau1 = 3.00
        self.syn["dtn"]["NMDA"].tau2 = 13.0 

        # Rat
        #self.syn["dtn"]["NMDA"].tau1 = 22.8 #NMDA
        # self.syn["dtn"]["NMDA"].tau2 = 92.1 #NMDA

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 8.5 
        self.syn["dtn"]["GABA"].tau2 = 60.0 

        self.syn["dtn"]["Glyc"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Glyc"].e = -95
        self.syn["dtn"]["Glyc"].tau1 = 1.5 
        self.syn["dtn"]["Glyc"].tau2 = 20.0 

        # Setup Network Connections
        self.nc["Onset"] = h.NetCon(None, self.syn["dtn"]["AMPA"])
        self.nc["Onset"].weight[0] = 0.0052

        self.nc["Offset"] = h.NetCon(None, self.syn["dtn"]["AMPA"])
        self.nc["Offset"].weight[0] = 0.0055 + 0.001

        self.nc["Sustain"] = h.NetCon(None, self.syn["dtn"]["GABA"])
        self.nc["Sustain"].weight[0] = 0.00150

        self.nc["OnsetInh"] = h.NetCon(None, self.syn["dtn"]["Glyc"])
        self.nc["OnsetInh"].weight[0] = 0.0010






class Rat(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['dtn']
        self.input = ['Onset','Offset','Sustain','OnsetInh']
        self.input_type = ['ON', 'OFF', 'SUS', 'ON']

        n = 3.0

        self.input_delay = [19.0+50+uniform(-n,n), 14.0+uniform(-n,n), 3.0, 2.0+uniform(-n,n)]
        self.input_size = [1, 2, 3, 3]

        # Create synapses on cells
        # AMPA Receptors
        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.1
        self.syn["dtn"]["AMPA"].tau2 = 1.5

        # Rat
        self.syn["dtn"]["AMPA"].tau1 = 5.4 #AMPA
        self.syn["dtn"]["AMPA"].tau2 = 35.6 #AMPA

        self.syn["dtn"]["NMDA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["NMDA"].e = -10
        self.syn["dtn"]["NMDA"].tau1 = 3.00
        self.syn["dtn"]["NMDA"].tau2 = 13.0 

        # Rat
        #self.syn["dtn"]["NMDA"].tau1 = 22.8 #NMDA
        # self.syn["dtn"]["NMDA"].tau2 = 92.1 #NMDA

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 8.5 
        self.syn["dtn"]["GABA"].tau2 = 60.0 

        self.syn["dtn"]["Glyc"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Glyc"].e = -95
        self.syn["dtn"]["Glyc"].tau1 = 1.5 
        self.syn["dtn"]["Glyc"].tau2 = 20.0 

        # Setup Network Connections
        self.nc["Onset"] = h.NetCon(None, self.syn["dtn"]["AMPA"])
        self.nc["Onset"].weight[0] = 0.0060 - 0.0045

        self.nc["Offset"] = h.NetCon(None, self.syn["dtn"]["AMPA"])
        self.nc["Offset"].weight[0] = 0.0055 - 0.0045

        self.nc["Sustain"] = h.NetCon(None, self.syn["dtn"]["GABA"])
        self.nc["Sustain"].weight[0] = 0.00003

        self.nc["OnsetInh"] = h.NetCon(None, self.syn["dtn"]["Glyc"])
        self.nc["OnsetInh"].weight[0] = 0.0005


