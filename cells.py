import models as m
from neuron import h
from os import urandom

class BaseNetwork:
    def __init__(self):
        self.cells = {}
        self.syn = {}
        self.nc = {}
        self.plots = {}
        self.input = [] 
        self.input_type = []
        self.input_delay = []
        self.plot_order = []


class Sandbox(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['dtn']
        self.input = ['Onset','Offset','Sustain']
        self.input_type = ['ON', 'OFF', 'SUS']
        self.input_delay = [15.0, 5.0, 0.0]

        # Create synapses on cells
        # AMPA Receptors
        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 1.2
        self.syn["dtn"]["AMPA"].tau1 = 1.0
        self.syn["dtn"]["AMPA"].tau2 = 4.0

        # Rat
        # self.syn["dtn"]["AMPA"].tau1 = 5.4 #AMPA
        # self.syn["dtn"]["AMPA"].tau2 = 35.6 #AMPA

        self.syn["dtn"]["NMDA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["NMDA"].e = -10
        self.syn["dtn"]["NMDA"].tau1 = 0.04
        self.syn["dtn"]["NMDA"].tau2 = 1.2 

        # Rat
        # self.syn["dtn"]["NMDA"].tau1 = 22.8 #NMDA
        # self.syn["dtn"]["NMDA"].tau2 = 92.1 #NMDA

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -80
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 20.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Onset"] = h.NetCon(None, self.syn["dtn"]["AMPA"])
        self.nc["Onset"].weight[0] = 0.005

        self.nc["Offset"] = h.NetCon(None, self.syn["dtn"]["NMDA"])
        self.nc["Offset"].weight[0] = 0#.005

        self.nc["Sustain"] = h.NetCon(None, self.syn["dtn"]["GABA"])
        self.nc["Sustain"].weight[0] = 0#.005


