
import dtn


#dtn.runSimulation("", [["Inh", 0.006],["Inh2", 0.006]], [])

for i in range(0, 12):
    inh = i*0.0005+0.004
    name = "PLT-%.4f"%inh
    dtn.runSimulation(name, [["Inh", inh],["Inh2", inh]], [])

