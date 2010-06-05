###################################
## Duration Tuned Neural Network ##
## Implemented with NEURON       ##
## Written By: Brandon Aubie     ##
###################################
from random import shuffle

# Parameters
delay = 50 # ms

# Single Tone Mode
duration = range(1,26,1)
duration = [5,10,15,40]

# Paired Pulse Gap Mode
GAP_MODE = False
GAP_MODE_TONE_DURATION = 1
GAPS = [i*0.5 for i in range(1,20,1)] 

# Plotting Parameters
PLOT_VOLTAGE = True
PLOT_DTN_SPIKES = False
PLOT_DTN_COUNT = False

trial = 300 # ms
if GAP_MODE:
    tstop = len(GAPS)*(trial+2)
else:
    tstop = len(duration)*(trial+2)

plot_cutoff = 50
GEN_SPIKES = True

repeats = 1
USE_GLE = False


##################################
## SETUP AND RUN THE SIMULATION ##
##################################
from neuron import h
import pickle

def mean(numberList):
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

dtn_spikes = []
voltage = []
for repeat in range(repeats):
    print "Running trial "+str(repeat+1)+" of "+str(repeats)
    # Load the network
    from cells import Sandbox as network

    net = network()
    cells = net.cells
    syn = net.syn
    nc = net.nc
    input = net.input


    # Setting the temperature high is key.
    h.celsius = 30

    def generateSpikes():
        global ic
        global icN
        global delay
        global duration
        global trial
        global GAP_MODE
        global GAP_MODE_TONE_DURATION
        global GAPS
        
        rate = 1000 # Hz
        trial_num = 0
        
        if GAP_MODE:
            for g in GAPS:
                spikes = []
                offset = delay+trial*trial_num
                dt = 1000.0 / rate
                for t in [i * dt for i in range(int(GAP_MODE_TONE_DURATION /dt)+1)]:
                    spikes.append(t)
                for s in spikes:
                    for i in input:
                        nc[i].event(s+offset)
                        nc[i].event(s+offset+g+GAP_MODE_TONE_DURATION)
                trial_num = trial_num + 1

        else:
            for d in duration:
                spikes = []
                offset = delay+trial*trial_num
                dt = 1000.0 / rate # Gap between spikes
                for t in [i * dt for i in range(int(d / dt)+1)]:
                    spikes.append(t)
                for s in spikes:
                    for i in input:
                        nc[i].event(s+offset)
                trial_num = trial_num + 1

    # Record time vector
    t = h.Vector()
    t.record(h._ref_t)

    # Record spike times
    nc["DTN_spikes"] = h.NetCon(cells['dtn'](0.5)._ref_v, None, sec=cells['dtn'])
    spikes = h.Vector()
    nc["DTN_spikes"].record(spikes)

    # run the stimulation
    fih = h.FInitializeHandler(0,generateSpikes)
        
    h.load_file("stdrun.hoc")
    h.init()
    h.tstop = tstop
    h.run()

    # extract spike counts for each trial
    cur_t = delay
    run_dtn_spikes = []

    if GAP_MODE:
        for trial_run in GAPS:
            new_spikes = []
            for s in spikes:
                if s > cur_t and s < cur_t + trial:
                    new_spikes.append(s - cur_t)
            run_dtn_spikes.append(new_spikes)
            cur_t = cur_t + trial
        dtn_spikes.append(run_dtn_spikes)
    else:
        for trial_run in duration:
            new_spikes = []
            for s in spikes:
                if s > cur_t and s < cur_t + trial:
                    new_spikes.append(s - cur_t)
            run_dtn_spikes.append(new_spikes)
            cur_t = cur_t + trial
        dtn_spikes.append(run_dtn_spikes)

    trial_voltage = {}
    for c in cells.keys():
        trial_voltage[c] = []
        for v in cells[c].rec_v:
            trial_voltage[c].append(v)
    voltage.append(trial_voltage)


print 'Plotting Results' 

if USE_GLE == True:
    from GLE import GLE
    GLE = GLE()

    if PLOT_DTN_SPIKES:
        # Calculate spike counts
        GLE.spikeraster(plot_prefix+'_raster', duration, dtn_spikes)

    if PLOT_DTN_COUNT:
        GLE.meanspikespertrial(plot_prefix+'_means', duration, [dtn_spikes])



# plot results
if USE_GLE == False:
    import pylab

    if PLOT_DTN_COUNT:
        # Calculate spike counts
        fig1 = pylab.figure(1, facecolor='white')
        count = []
        if GAP_MODE:
            temp = [[] for d in GAPS]
        else:
            temp = [[] for d in duration]
        for run in dtn_spikes:
            c = 0
            for d in run:
                temp[c].append(len(d))
                c = c + 1
        for d in temp:
            count.append(mean(d))

        if GAP_MODE:
            pylab.plot(GAPS, count, 'ko-')
        else:
            pylab.plot(duration, count, 'ko-')
        pylab.axis(ymin=0, ymax=max(count)+1)

    if PLOT_DTN_SPIKES:
        # Calculate spike counts
        fig2 = pylab.figure(2, facecolor='white')
        count = 0;
        dy = 1.0 / repeats
        y_offset = 0.0 

        # Plot the stimuli first
        if GAP_MODE:
            for d in GAPS:
                pylab.plot([0, GAP_MODE_TONE_DURATION], [d, d], 'k-')
                pylab.plot([GAP_MODE_TONE_DURATION+d,GAP_MODE_TONE_DURATION*2+d], [d, d], 'k-')
        else:
            for d in duration:
                pylab.plot([0, d], [d, d], 'k-')

        for run in dtn_spikes:
            count = 0

            if GAP_MODE:
                for d in GAPS:
                    if len(run[count]) > 0:
                        pylab.plot(run[count], [d+y_offset for i in range(len(run[count]))], 'k.', markersize=10.0)
                    count = count + 1
                y_offset = y_offset + dy

            else:
                for d in duration:
                    if len(run[count]) > 0:
                        pylab.plot(run[count], [d+y_offset for i in range(len(run[count]))], 'k,')
                    count = count + 1
                y_offset = y_offset + dy

        if GAP_MODE:
            pylab.axis(ymin=min(GAPS)-0.2, ymax=max(GAPS)+1, xmin=-5, xmax=plot_cutoff)
        else:
            pylab.axis(ymin=min(duration)-0.2, ymax=max(duration)+1, xmin=-5, xmax=plot_cutoff)

    if PLOT_VOLTAGE:

        # Average the voltages
        avg_voltage = {}
        avg_weight = 1.0 / len(voltage)
        for c in cells.keys():
            avg_voltage[c] = [0 for i in t]
        for v in voltage:
            for c in cells.keys():
                for i in range(0, len(t)):
                    avg_voltage[c][i] = avg_voltage[c][i] + v[c][i]*avg_weight

        fig3 = pylab.figure(3, facecolor='white')
        y_min = -100
        y_max = 50

        t = [i-delay for i in t]

        num_plots = len(net.cells)+len(net.plots)+1
        count = 0
        trial_num = 0
        psth = [0 for i in range(-delay, int(max(t)))]
        psth_t = [i for i in range(-delay, int(max(t)))]

        count = count + 1
        pylab.subplot(num_plots, 1, count, title='Input PSTH')
        pylab.bar(psth_t, psth, fc='black')
        pylab.axis([-delay, h.tstop-delay, 0, max(psth)+2])

        for c in net.plot_order:
            count = count + 1
            pylab.subplot(num_plots, 1, count, title=c)
            pylab.plot(t, avg_voltage[c], color='black')
            pylab.axis([-delay, h.tstop-delay, y_min, y_max])
            ax = pylab.gca()
            ax.xaxis.set_major_locator(pylab.AutoLocator())
            x_major = ax.xaxis.get_majorticklocs()
            dx_minor = (x_major[-1]-x_major[0])/(len(x_major)-1) / 25;
            ax.xaxis.set_minor_locator(pylab.MultipleLocator(dx_minor))

        for c in net.plots:
            count = count + 1
            pylab.subplot(num_plots, 1, count, title=c)
            for p in net.plots[c]:
                pylab.plot(t, net.plots[c][p],label=p)
            pylab.axis(xmin=-delay, xmax=h.tstop-delay)
            ax = pylab.gca()
            ax.xaxis.set_major_locator(pylab.AutoLocator())
            x_major = ax.xaxis.get_majorticklocs()
            dx_minor = (x_major[-1]-x_major[0])/(len(x_major)-1) / 25;
            ax.xaxis.set_minor_locator(pylab.MultipleLocator(dx_minor))
            pylab.legend()

        pylab.subplots_adjust(hspace=0.9)

    pylab.show()
