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
        self.plot_order = []


class Sandbox(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['Offset'] = m.Primary()
        self.syn['Offset'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'Offset','dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["Offset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["AMPA"].e = -10
        self.syn["Offset"]["AMPA"].tau1 = 0.4 
        self.syn["Offset"]["AMPA"].tau2 = 1.5

        self.syn["Offset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["GABA"].e = -95
        self.syn["Offset"]["GABA"].tau1 = 1.1 
        self.syn["Offset"]["GABA"].tau2 = 3.0 

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.0

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 0.8 

        self.syn["dtn"]["NMDA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["NMDA"].e = -10
        self.syn["dtn"]["NMDA"].tau1 = 1.00
        self.syn["dtn"]["NMDA"].tau2 = 8.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 20.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.005

        self.nc["Primary->Offset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_AMPA"].weight[0] = 0.005 
        self.nc["Primary->Offset_AMPA"].delay = 5

        self.nc["Primary->Offset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_GABA"].weight[0] = 0.002
        self.nc["Primary->Offset_GABA"].delay = 0

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.018
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Offset->DTN_AMPA"] = h.NetCon(self.cells['Offset'](0.5)._ref_v, self.syn["dtn"]["NMDA"], sec=self.cells['Offset'])
        self.nc["Offset->DTN_AMPA"].weight[0] = 0.001
        self.nc["Offset->DTN_AMPA"].delay = 5 

        self.nc["Onset->DTN_NMDA"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["NMDA"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_NMDA"].weight[0] = 0.003
        self.nc["Onset->DTN_NMDA"].delay = 12

        self.nc["Primary->DTN_Gly"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_Gly"].weight[0] = 0.0010
        self.nc["Primary->DTN_Gly"].delay = 5

######
# Used in poster
######

class MatchMU7_6_003(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 2.5 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.005

        self.nc["Primary->DTN_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_AMPA"].weight[0] = 0.008
        self.nc["Primary->DTN_AMPA"].delay = 6

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.005
        self.nc["Primary->DTN_GABA"].delay = 12

        self.nc["Primary->DTN_Glyc"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_Glyc"].weight[0] = 0.005
        self.nc["Primary->DTN_Glyc"].delay = 3


class MatchMU14_7_002(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['PrimaryW'] = m.Primary()
        self.syn['PrimaryW'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'PrimaryW', 'Onset', 'dtn']
        self.input = ['Input->Primary_AMPA','Input->PrimaryW_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["PrimaryW"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['PrimaryW'])
        self.syn["PrimaryW"]["AMPA"].e = -10
        self.syn["PrimaryW"]["AMPA"].tau1 = 0.04
        self.syn["PrimaryW"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.5

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 4.00
        self.syn["dtn"]["AMPA"].tau2 = 10.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Input->PrimaryW_AMPA"] = h.NetCon(None, self.syn["PrimaryW"]["AMPA"])
        self.nc["Input->PrimaryW_AMPA"].weight[0] = 0.00008

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.018
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Onset->DTN_AMPA"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_AMPA"].weight[0] = 0.0045
        self.nc["Onset->DTN_AMPA"].delay = 0 

        self.nc["PrimaryW->DTN_GABA"] = h.NetCon(self.cells['PrimaryW'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['PrimaryW'])
        self.nc["PrimaryW->DTN_GABA"].weight[0] = 0.003
        self.nc["PrimaryW->DTN_GABA"].delay = 0

class MatchUW231_4_008(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['Offset'] = m.Primary()
        self.syn['Offset'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'Offset','dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["Offset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["AMPA"].e = -10
        self.syn["Offset"]["AMPA"].tau1 = 0.4 
        self.syn["Offset"]["AMPA"].tau2 = 1.5

        self.syn["Offset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["GABA"].e = -95
        self.syn["Offset"]["GABA"].tau1 = 1.1 
        self.syn["Offset"]["GABA"].tau2 = 3.0 

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.0

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 1.5 

        self.syn["dtn"]["NMDA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["NMDA"].e = -10
        self.syn["dtn"]["NMDA"].tau1 = 1.00
        self.syn["dtn"]["NMDA"].tau2 = 8.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 20.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Primary->Offset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_AMPA"].weight[0] = 0.005
        self.nc["Primary->Offset_AMPA"].delay = 7

        self.nc["Primary->Offset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_GABA"].weight[0] = 0.002
        self.nc["Primary->Offset_GABA"].delay = 0

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.018
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Offset->DTN_AMPA"] = h.NetCon(self.cells['Offset'](0.5)._ref_v, self.syn["dtn"]["NMDA"], sec=self.cells['Offset'])
        self.nc["Offset->DTN_AMPA"].weight[0] = 0.0005
        self.nc["Offset->DTN_AMPA"].delay = 5 

        self.nc["Onset->DTN_NMDA"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["NMDA"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_NMDA"].weight[0] = 0.004
        self.nc["Onset->DTN_NMDA"].delay = 12

        self.nc["Primary->DTN_Gly"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_Gly"].weight[0] = 0.0010
        self.nc["Primary->DTN_Gly"].delay = 5

class MatchRAT39_164(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.PrimaryLarge()
        self.syn['Primary'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 1.00
        self.syn["Primary"]["AMPA"].tau2 = 5.0

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 6.0

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 1.5 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 3.0 
        self.syn["dtn"]["Gly"].tau2 = 10.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00004

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.012
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Onset->DTN_Glyc"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_Glyc"].weight[0] = 0.010
        self.nc["Onset->DTN_Glyc"].delay = 30

        self.nc["Primary->DTN_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_AMPA"].weight[0] = 0.006
        self.nc["Primary->DTN_AMPA"].delay = 35

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.005
        self.nc["Primary->DTN_GABA"].delay = 170

        self.nc["Primary->DTN_Glyc"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_Glyc"].weight[0] = 0.002
        self.nc["Primary->DTN_Glyc"].delay = 05

class MatchRAT9_39(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 2.5 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Primary->DTN_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_AMPA"].weight[0] = 0.003
        self.nc["Primary->DTN_AMPA"].delay = 18

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.003
        self.nc["Primary->DTN_GABA"].delay = 28

        self.nc["Primary->DTN_Glyc"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_Glyc"].weight[0] = 0.005
        self.nc["Primary->DTN_Glyc"].delay = 6
######
# Framework networks to build off of
######

class Onset_Shortpass_1ms_VerySharp(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['PrimaryW'] = m.Primary()
        self.syn['PrimaryW'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'PrimaryW', 'Onset', 'dtn']
        self.input = ['Input->Primary_AMPA','Input->PrimaryW_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["PrimaryW"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['PrimaryW'])
        self.syn["PrimaryW"]["AMPA"].e = -10
        self.syn["PrimaryW"]["AMPA"].tau1 = 0.04
        self.syn["PrimaryW"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["GABA"].e = -75
        self.syn["Onset"]["GABA"].tau1 = 1.5 
        self.syn["Onset"]["GABA"].tau2 = 5.0 

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 4.00
        self.syn["dtn"]["AMPA"].tau2 = 10.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Input->PrimaryW_AMPA"] = h.NetCon(None, self.syn["PrimaryW"]["AMPA"])
        self.nc["Input->PrimaryW_AMPA"].weight[0] = 0.00008

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.020
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Primary->Onset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_GABA"].weight[0] = 0.01
        self.nc["Primary->Onset_GABA"].delay = 2

        self.nc["Onset->DTN_AMPA"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_AMPA"].weight[0] = 0.0045
        self.nc["Onset->DTN_AMPA"].delay = 0

        self.nc["PrimaryW->DTN_GABA"] = h.NetCon(self.cells['PrimaryW'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['PrimaryW'])
        self.nc["PrimaryW->DTN_GABA"].weight[0] = 0.003
        self.nc["PrimaryW->DTN_GABA"].delay = 0

class Sustained_Bandpass_5ms_Sharp(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 2.5 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Primary->DTN_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_AMPA"].weight[0] = 0.008
        self.nc["Primary->DTN_AMPA"].delay = 5

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.005
        self.nc["Primary->DTN_GABA"].delay = 10

        self.nc["Primary->DTN_Glyc"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_Glyc"].weight[0] = 0.005
        self.nc["Primary->DTN_Glyc"].delay = 1.0 

class Onset_Shortpass_1ms_Sharp_Jitter(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["GABA"].e = -75
        self.syn["Onset"]["GABA"].tau1 = 1.5 
        self.syn["Onset"]["GABA"].tau2 = 5.0 

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 4.00
        self.syn["dtn"]["AMPA"].tau2 = 10.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.020
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Primary->Onset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_GABA"].weight[0] = 0.01
        self.nc["Primary->Onset_GABA"].delay = 2

        self.nc["Onset->DTN_Gly"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_Gly"].weight[0] = 0.010
        self.nc["Onset->DTN_Gly"].delay = 1.0

        self.nc["Onset->DTN_AMPA"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_AMPA"].weight[0] = 0.005
        self.nc["Onset->DTN_AMPA"].delay = 5

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.0005
        self.nc["Primary->DTN_GABA"].delay = 1.0

class Onset_Shortpass_1ms_Sharp(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['Onset'] = m.Onset()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.5

        self.syn["Onset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["GABA"].e = -75
        self.syn["Onset"]["GABA"].tau1 = 1.5 
        self.syn["Onset"]["GABA"].tau2 = 5.0 

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 4.00
        self.syn["dtn"]["AMPA"].tau2 = 10.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.020
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Primary->Onset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_GABA"].weight[0] = 0.01
        self.nc["Primary->Onset_GABA"].delay = 2

        self.nc["Onset->DTN_Gly"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_Gly"].weight[0] = 0.010
        self.nc["Onset->DTN_Gly"].delay = 0

        self.nc["Onset->DTN_AMPA"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_AMPA"].weight[0] = 0.005
        self.nc["Onset->DTN_AMPA"].delay = 5

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.0005
        self.nc["Primary->DTN_GABA"].delay = 0

class Offset_Bandpass_11ms_Wide(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['Offset'] = m.Primary()
        self.syn['Offset'] = {} 
        self.cells['Onset'] = m.Primary()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'Offset','dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 1.00
        self.syn["Primary"]["AMPA"].tau2 = 3.0

        self.syn["Offset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["AMPA"].e = -10
        self.syn["Offset"]["AMPA"].tau1 = 1.0 
        self.syn["Offset"]["AMPA"].tau2 = 3.0

        self.syn["Offset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["GABA"].e = -95
        self.syn["Offset"]["GABA"].tau1 = 1.1 
        self.syn["Offset"]["GABA"].tau2 = 3.0 

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.0

        self.syn["Onset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["GABA"].e = -75
        self.syn["Onset"]["GABA"].tau1 = 1.5 
        self.syn["Onset"]["GABA"].tau2 = 5.0 

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 1.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00005

        self.nc["Primary->Offset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_AMPA"].weight[0] = 0.002
        self.nc["Primary->Offset_AMPA"].delay = 7

        self.nc["Primary->Offset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_GABA"].weight[0] = 0.002
        self.nc["Primary->Offset_GABA"].delay = 0

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.012
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Primary->Onset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_GABA"].weight[0] = 0.01
        self.nc["Primary->Onset_GABA"].delay = 0

        self.nc["Offset->DTN_AMPA"] = h.NetCon(self.cells['Offset'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Offset'])
        self.nc["Offset->DTN_AMPA"].weight[0] = 0.007
        self.nc["Offset->DTN_AMPA"].delay = 0 

        self.nc["Onset->DTN_Gly"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_Gly"].weight[0] = 0.010
        self.nc["Onset->DTN_Gly"].delay = 0

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.0001 
        self.nc["Primary->DTN_GABA"].delay = 30

class Offset_Bandpass_11ms(BaseNetwork):
    def __init__(self):
        BaseNetwork.__init__(self)

        self.cells['Primary'] = m.Primary()
        self.syn['Primary'] = {} 
        self.cells['Offset'] = m.Primary()
        self.syn['Offset'] = {} 
        self.cells['Onset'] = m.Primary()
        self.syn['Onset'] = {} 
        self.cells['dtn'] = m.Primary()
        self.syn['dtn'] = {}

        self.plot_order = ['Primary', 'Onset', 'Offset','dtn']
        self.input = ['Input->Primary_AMPA']

        # Create synapses on cells
        # AMPA Receptors
        self.syn["Primary"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Primary'])
        self.syn["Primary"]["AMPA"].e = -10
        self.syn["Primary"]["AMPA"].tau1 = 0.04
        self.syn["Primary"]["AMPA"].tau2 = 1.0

        self.syn["Offset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["AMPA"].e = -10
        self.syn["Offset"]["AMPA"].tau1 = 1.0 
        self.syn["Offset"]["AMPA"].tau2 = 3.0

        self.syn["Offset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Offset'])
        self.syn["Offset"]["GABA"].e = -95
        self.syn["Offset"]["GABA"].tau1 = 1.1 
        self.syn["Offset"]["GABA"].tau2 = 3.0 

        self.syn["Onset"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["AMPA"].e = -10
        self.syn["Onset"]["AMPA"].tau1 = 0.04
        self.syn["Onset"]["AMPA"].tau2 = 1.0

        self.syn["Onset"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['Onset'])
        self.syn["Onset"]["GABA"].e = -75
        self.syn["Onset"]["GABA"].tau1 = 1.5 
        self.syn["Onset"]["GABA"].tau2 = 5.0 

        self.syn["dtn"]["AMPA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["AMPA"].e = -10
        self.syn["dtn"]["AMPA"].tau1 = 0.04
        self.syn["dtn"]["AMPA"].tau2 = 1.0 

        self.syn["dtn"]["GABA"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["GABA"].e = -75
        self.syn["dtn"]["GABA"].tau1 = 3.5 
        self.syn["dtn"]["GABA"].tau2 = 50.0 

        self.syn["dtn"]["Gly"] = h.Exp2Syn(0.5, sec=self.cells['dtn'])
        self.syn["dtn"]["Gly"].e = -95
        self.syn["dtn"]["Gly"].tau1 = 1.1 
        self.syn["dtn"]["Gly"].tau2 = 3.0 

        # Setup Network Connections
        self.nc["Input->Primary_AMPA"] = h.NetCon(None, self.syn["Primary"]["AMPA"])
        self.nc["Input->Primary_AMPA"].weight[0] = 0.00015

        self.nc["Primary->Offset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_AMPA"].weight[0] = 0.002
        self.nc["Primary->Offset_AMPA"].delay = 7

        self.nc["Primary->Offset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Offset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Offset_GABA"].weight[0] = 0.002
        self.nc["Primary->Offset_GABA"].delay = 0

        self.nc["Primary->Onset_AMPA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["AMPA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_AMPA"].weight[0] = 0.012
        self.nc["Primary->Onset_AMPA"].delay = 0

        self.nc["Primary->Onset_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["Onset"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->Onset_GABA"].weight[0] = 0.01
        self.nc["Primary->Onset_GABA"].delay = 0

        self.nc["Offset->DTN_AMPA"] = h.NetCon(self.cells['Offset'](0.5)._ref_v, self.syn["dtn"]["AMPA"], sec=self.cells['Offset'])
        self.nc["Offset->DTN_AMPA"].weight[0] = 0.007
        self.nc["Offset->DTN_AMPA"].delay = 0 

        self.nc["Onset->DTN_Gly"] = h.NetCon(self.cells['Onset'](0.5)._ref_v, self.syn["dtn"]["Gly"], sec=self.cells['Onset'])
        self.nc["Onset->DTN_Gly"].weight[0] = 0.010
        self.nc["Onset->DTN_Gly"].delay = 0

        self.nc["Primary->DTN_GABA"] = h.NetCon(self.cells['Primary'](0.5)._ref_v, self.syn["dtn"]["GABA"], sec=self.cells['Primary'])
        self.nc["Primary->DTN_GABA"].weight[0] = 0.0001
        self.nc["Primary->DTN_GABA"].delay = 30

