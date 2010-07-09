
import dtn

#for inhibition in [i * 0.0005 for i in range(0, 20)]:
#    filename = "PLT-%0.4f" % inhibition
#    dtn.runSimulation(filename,[["Inh",inhibition],["Inh2",inhibition]],[])

for i in range(0, 8):
    inh = i*0.0005+0.004
    name = "PLT-%.4f"%inh
    dtn.runSimulation(name, [["Inh", inh],["Inh2", inh]], [])

