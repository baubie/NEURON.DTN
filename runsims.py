
import dtn


#dtn.runSimulation("",[], []) 
#quit()

for i in range(0, 3):
    inh = i*0.0010+0.003
    name = "EXCRamp2/EXCRamp-%.4f"%inh
    dtn.runSimulation(name, [["Exc", inh]], [])

