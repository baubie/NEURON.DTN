###################################
## Duration Tuned Neural Network ##
## Implemented with NEURON       ##
## Written By: Brandon Aubie     ##
###################################
from random import shuffle
from os import urandom
from random import uniform
from random import gauss


def runSimulation(data_filename, ncParams, synParams):
# Parameters
    delay = 50 # ms
    trial = 300 # ms
    PLOT_VOLTAGE = False
    PLOT_DTN_SPIKES = True
    PLOT_DTN_COUNT = True
    SHOW_PLOTS = True
    USE_GLE = False


    DATA_SAVE_NAME = data_filename

    plot_cutoff = 50
    repeats = 20

    print "Running Simulation: " + data_filename + "\n NC Params: " + str(ncParams) + "\n Syn Params: " + str(synParams) + "\n=========================================="

# Produce Stimuli
# [ 
#     [ [on, off], [on, off], ..., [on, off] ],   <-- Trial 1
#     [ [on, off], [on, off], ..., [on, off] ],   <-- Trial 2
#     [ [on, off], [on, off], ..., [on, off] ],   <-- Trial 3
# ]

# Duration Tuning Test
    stimuli = [ [ [0.0, d] ] for d in range(1, 26,1) ]
    #stimuli = [ [ [0.0, d] ] for d in [1, 5, 15] ]
    #stimuli = [ [ [0.0, d] ] for d in range(5, 201,5) ]
    

# Paired-Pulse Tuning Test
    PP_Length = 1.0
    PP_step = 0.1
    PP_max_sep = 3.0
    stimulipp = [ [ [0.0, PP_Length], [PP_Length+d*PP_step, PP_Length*2+d*PP_step] ] for d in range(0, PP_max_sep/PP_step) ]
    stimuli = stimuli+stimulipp

    BD_Length = 5.0
    BD_step = 1.0
    BD_max_sep = 100.0

    stimulipp = [ [ [0.0, BD_Length], [BD_Length+d*BD_step, BD_Length*2+d*BD_step] ] for d in range(0, BD_max_sep/BD_step) ]
    #stimuli = stimuli+stimulipp
    tstop = len(stimuli)*(trial)+delay



##################################
## SETUP AND RUN THE SIMULATION ##
##################################
    from neuron import h

    def mean(numberList):
        floatNums = [float(x) for x in numberList]
        return sum(floatNums) / len(numberList)

    dtn_spikes = []
    voltage = []
    for repeat in range(repeats):
        print "Running trial "+str(repeat+1)+" of "+str(repeats)
# Load the network
        from cells import BatCEC2000_BP as network

        net = network()
        cells = net.cells
        syn = net.syn
        nc = net.nc
        input = net.input
        input_type = net.input_type
        input_delay = net.input_delay
        input_size = net.input_size

        for mod in ncParams:
            nc[mod[0]].weight[0] = mod[1]


# Setting the temperature high is key.
        h.celsius = 37
        #h.dt = 0.025

        def generateSpikes():
            #global delay
            #global stimuli
            #global trial
            #global input
            #global input_type
            #global input_delay
            #global input_size
            
            rate = 1000 # Hz
            trial_num = 0
            ref = 1.0
            count = 0
            on_recovery = 20.0
            
            for trials in stimuli:
                count = count + 1
                spikes = []
                offset = delay+trial*trial_num
                dt = 1000.0 / rate # Gap between spikes
                last_spike = -999
                jitter = 0.1

                on_last_spike = -999
                for i in range(len(input)):
                    last_spike = -999
                    #print "\n"+input[i]+" - Trial: "+str(count)
                    if input_type[i] == 'SUS':
                        for pulse in trials:
                            for t in [tp * dt for tp in range( max(int((pulse[1]-pulse[0])/dt), input_size[i]))]:
                                spike_time = round(t+pulse[0]+offset+input_delay[i] + gauss(0,jitter),2)
                                if spike_time - last_spike >= ref:
                                    #print spike_time
                                    nc[input[i]].event(spike_time)
                                    last_spike = spike_time

                    if input_type[i] == 'ON':
                        for pulse in trials:
                            for x in range(input_size[i]):
                                spike_time = round(pulse[0]+offset+input_delay[i]+x+uniform(-jitter,jitter),2)
                                if spike_time - on_last_spike >= on_recovery:
                                    spike_time = spike_time + gauss(0,jitter)
                                    nc[input[i]].event(spike_time)
                                    last_spike = spike_time
                                    on_last_spike = last_spike

                    if input_type[i] == 'OFF':
                        for pulse in trials:
                            for x in range(input_size[i]):
                                spike_time = pulse[1]+offset+input_delay[i]+x*1.5
                                if spike_time - last_spike >= ref:
                                    spike_time = spike_time + uniform(-jitter,jitter)
                                    nc[input[i]].event(spike_time)
                                    last_spike = spike_time

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

        for trial_run in stimuli:
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
        import csv

        if PLOT_DTN_COUNT:
            # Calculate spike counts
            fig1 = pylab.figure(1, facecolor='white')
            count = []
            temp = [[] for s in stimuli]
            for run in dtn_spikes:
                c = 0
                for d in run:
                    temp[c].append(len(d))
                    c = c + 1
            for d in temp:
                count.append(mean(d))

            pylab.plot(range(1,len(stimuli)+1), count, 'ko-')
            pylab.axis(ymin=0, ymax=max(count)+1)

            if DATA_SAVE_NAME != False:
               w = csv.writer(open(DATA_SAVE_NAME+"_count.dat", 'w'), delimiter=",", quoting=csv.QUOTE_MINIMAL)
               for i in range(0, len(stimuli)):
                   w.writerow([i+1, count[i]])


        if PLOT_DTN_SPIKES:
            # Calculate spike counts
            fig2 = pylab.figure(2, facecolor='white')
            count = 0;
            dy = 1.0 / repeats
            y_offset = 0.0 

            if DATA_SAVE_NAME != False:
               w = csv.writer(open(DATA_SAVE_NAME+"_spikes.dat", 'w'), delimiter=",", quoting=csv.QUOTE_MINIMAL)

            # Plot the stimuli
            d = 1
            for s in stimuli:
                for pulse in s:
                    pylab.plot([pulse[0], pulse[1]], [d, d], 'k-')
                d = d + 1

            # Plot the spikes
            for run in dtn_spikes:
                count = 0

                d = 1
                for s in stimuli:
                    if len(run[count]) > 0:
                        pylab.plot(run[count], [d+y_offset for i in range(len(run[count]))], 'k,')
                        if DATA_SAVE_NAME != False:
                           for i in range(0, len(run[count])):
                               w.writerow([run[count][i], (d+y_offset)*5])

                    count = count + 1
                    d = d + 1
                y_offset = y_offset + dy

            pylab.axis(ymin=0.0, ymax=len(stimuli)+1, xmin=-5, xmax=plot_cutoff)



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

            num_plots = len(net.cells)+len(net.plots) #+1
            count = 0
            trial_num = 0
            psth = [0 for i in range(-delay, int(max(t)))]
            psth_t = [i for i in range(-delay, int(max(t)))]

#        count = count + 1
#        pylab.subplot(num_plots, 1, count, title='Input PSTH')
#        pylab.bar(psth_t, psth, fc='black')
#        pylab.axis([-delay, h.tstop-delay, 0, max(psth)+2])

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

        if SHOW_PLOTS:
            pylab.show()
