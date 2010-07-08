
import dtn

#for inhibition in [i * 0.0005 for i in range(0, 20)]:
#    filename = "PLT-%0.4f" % inhibition
#    dtn.runSimulation(filename,[["Inh",inhibition],["Inh2",inhibition]],[])

dtn.runSimulation("", [["Inh", 0.006],["Inh2", 0.006]], [])

