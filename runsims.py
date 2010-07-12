
import dtn


#dtn.runSimulation("",[], []) 
#quit()

for i in range(0, 10):
    inh = i*0.0005+0.003
    name = "EXCRamp/EXCRamp-%.4f"%inh
    dtn.runSimulation(name, [["Exc", inh]], [])

