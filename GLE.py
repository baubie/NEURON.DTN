from subprocess import call
from scipy import special
from os import remove
from os import access
from os import F_OK
from os import mkdir
from os import rename

class Stimulus:
    def __init__(self):
        self.dur = []
        self.delay = []

class Spikes:
    def __init__(self):
        self.stim = 0
        self.spikes = []

def GammaDist(alpha, beta, x):
    if x <= 0:
        return -100000
    else:
        return pow(x,alpha-1) * special.exp(-1.0*x / beta) / (pow(beta,alpha)*special.gamma(alpha))

class GLE:

    def __init__(self):
        self.w = 5.4
        self.h = 4.3
        self.scale = 1
        self.markers = ['fsquare', 'fcircle', 'ftriangle', 'square', 'circle', 'triangle']
        self.format = 'eps'
        self.rasterOffset = 0
        self.rasterStart = -0.5
        self.rasterEnd = 50
        self.binWindow = 20
        self.binCriteria = 0.001
        self.VariableType = 0 # 0=Duration 1=Delay
        self.Channel = 1 # Channel to use on dependent variable
        self.stimuli = []
        self.spikes = []
        self.stimFilterA = 1
        self.stimFilterB = 1
        self.filename = ''

    def launchQGLE(self):
        call(['qgle',self.filename+'.gle'])

    def save(self,folder,name):
        if access(folder, F_OK):
            fullpath = folder+'/'+name+'/'
            mkdir(fullpath)
            rename(self.filename+'.gle', fullpath+name+'.gle')
            for x in ['.png','_means_0','_means_1','_means_2','_means_3','_means_4','_spikes_0','_spikes_1','_spikes_2','_spikes_3','_spikes_4']:
                if access(self.filename+x, F_OK):
                    rename(self.filename+x,fullpath+self.filename.rsplit('/')[-1]+x)
        else:
            return False

    def __del__(self):
        self.cleantmp()

    def cleantmp(self):
        if self.filename != '':
            for x in ['','.gle','.png','_means_0','_means_1','_means_2','_means_3','_means_4','_spikes_0','_spikes_1','_spikes_2','_spikes_3','_spikes_4']:
                if access(self.filename+x, F_OK):
                    remove(self.filename+x)

    def binspikes(self):
        count = 0
        s1tmp = []
        s2tmp = []
        s3tmp = []
        numChannels = 1
        if len(self.stimuli) > 0:
            numChannels = len(self.stimuli[0].dur)

        dy = 0
        if len(self.spikes) > 0:
            dy = float(len(self.stimuli)) / float(len(self.spikes))
        dy = dy * 0.6
        y_offset = dy

        # First, crudely bin spikes based on a time window
        for run in self.spikes:
            count = count + 1
            for spike in run.spikes:
                if numChannels == 1 or (spike - self.stimuli[run.stim-1].delay[0] < self.binWindow and spike-self.stimuli[run.stim-1].delay[0] > 0):
                    s1tmp.append([run.stim,spike-self.rasterOffset,run.stim+y_offset])
                else:
                    if spike - self.stimuli[run.stim-1].delay[1] < self.binWindow and spike-self.stimuli[run.stim-1].delay[1] > 0:
                        s2tmp.append([run.stim,spike-self.rasterOffset,run.stim+y_offset])
                    else:
                        s3tmp.append([run.stim,spike-self.rasterOffset,run.stim+y_offset])

            if count == len(self.stimuli):
                y_offset = y_offset + dy
                count = 0

        # Second, use method of moments on stim=1 to get two distributions
        alpha = [0,0]
        beta = [0,0]
        m1 = [0,0]
        m2 = [0,0]
        offset = [1000,1000]
        count = [0,0]
        for spike in s1tmp:
            if spike[0] == 1:
                offset[0] = min(offset[0], spike[1]-self.stimuli[0].delay[0])
        for spike in s2tmp:
            if spike[0] == 1:
                offset[1] = min(offset[1], spike[1]-self.stimuli[0].delay[1])


        # For safety, shift offset by 2 ms
        offset[0] = max(0, offset[0] - 4)
        offset[1] = max(0, offset[1] - 4)

        stim_to_use = [1]

        for spike in s1tmp:
            for stim_use in stim_to_use:
                if spike[0] == stim_use: # Look at the first stimulus
                    m1[0] = m1[0] + spike[1]-self.stimuli[0].delay[0] - offset[0]+self.rasterOffset
                    m2[0] = m2[0] + pow(spike[1]-self.stimuli[0].delay[0] - offset[0]+self.rasterOffset,2)
                    count[0] = count[0] + 1
        if numChannels > 1:
            for spike in s2tmp:
                for stim_use in stim_to_use:
                    if spike[0] == stim_use: # Look at the first stimulus
                        m1[1] = m1[1] + spike[1]-self.stimuli[0].delay[1]-offset[1]+self.rasterOffset
                        m2[1] = m2[1] + pow(spike[1]-self.stimuli[0].delay[1]-offset[1]+self.rasterOffset,2)
                        count[1] = count[1] + 1

            if count[0] == 0:
                m1[0] = 0
                m2[0] = 0
            else:
                m1[0] = m1[0] / count[0]
                m2[0] = m2[0] / count[0]
            if count[1] == 0:
                m1[1] = 0
                m2[1] = 0
            else:
                m1[1] = m1[1] / count[1]
                m2[1] = m2[1] / count[1]

            if m2[0] == pow(m1[0],2):
                alpha[0] = 0
            else:
                alpha[0] = pow(m1[0],2) / (m2[0]-pow(m1[0],2))

            if m2[1] == pow(m1[1],2):
                alpha[1] = 0
            else:
                alpha[1] = pow(m1[1],2) / (m2[1]-pow(m1[1],2))

            if m1[0] == 0:
                beta[0] = 0
            else:
                beta[0] = (m2[0] - pow(m1[0],2)) / m1[0]

            if m1[1] == 0:
                beta[1] = 0
            else:
                beta[1] = (m2[1] - pow(m1[1],2)) / m1[1]

        # Bin all the spikes based on the statistical model
        s1 = []
        s2 = []
        s3 = []
        for s in s1tmp+s2tmp:
            if len(self.stimuli[s[0]-1].delay) > 1:
                GDC1 = GammaDist(alpha[0],beta[0],s[1]-self.stimuli[s[0]-1].delay[0]-offset[0]+self.rasterOffset)
                GDC2 = GammaDist(alpha[1],beta[1],s[1]-self.stimuli[s[0]-1].delay[1]-offset[1]+self.rasterOffset)
                if GDC1 < self.binCriteria and GDC2 < self.binCriteria:
                    s3.append(s)
                else:
                    if numChannels == 1 or (GDC1 > GDC2):
                        s1.append(s)
                    else:
                        if GDC1 < GDC2:
                            s2.append(s)
                        else:
                            s3.append(s)
            else:
                s1.append(s)

        # Assume spont spikes are still spontaneous
        for s in s3tmp:
            s3.append(s)

        return [s1,s2,s3]

    def meanspikespertrial(self, filename, mode='spike', notes=''):

        self.cleantmp()

        # Create the data file
        s = []
        means = []
        max_mean = 0
        min_mean = 0
        sd = []
        exp_total = [0 for i in self.stimuli] # Default 0
        count = [0 for i in self.stimuli] # Trials with spikes

        # Filter spikes
        tmpSpikes = []
        for s in self.spikes:
            newS = Spikes()
            newS.stim = s.stim
            for spike in s.spikes:
                if spike >= self.rasterStart+self.rasterOffset and spike <= self.rasterEnd+self.rasterOffset:
                    newS.spikes.append(spike)
            tmpSpikes.append(newS)
        self.spikes = tmpSpikes


        # Calculate the means
        for trial in self.spikes:
            if mode == 'spike':
                exp_total[trial.stim-1] = exp_total[trial.stim-1] + len(trial.spikes)
                count[trial.stim-1] = count[trial.stim-1] + 1
            if mode == 'fsl':
                if len(trial.spikes) > 0:
                    exp_total[trial.stim-1] = exp_total[trial.stim-1] + min(trial.spikes) - self.stimuli[trial.stim-1].delay[self.Channel]
                    count[trial.stim-1] = count[trial.stim-1] + 1
            if mode == 'lsl':
                if len(trial.spikes) > 0:
                    exp_total[trial.stim-1] = exp_total[trial.stim-1] + max(trial.spikes) - self.stimuli[trial.stim-1].delay[self.Channel]
                    count[trial.stim-1] = count[trial.stim-1] + 1
        means = [(float(exp_total[i]) / float(count[i]) if count[i] != 0 else 0) for i in range(len(self.stimuli))]
        if mode == 'ratio':
            binned = self.binspikes()
            exp_total1 = [0 for i in self.stimuli] # Default 0
            exp_total2 = [0 for i in self.stimuli] # Default 0
            for s in binned[0]:
                exp_total1[s[0]-1] = exp_total1[s[0]-1] + 1
            for s in binned[1]:
                exp_total2[s[0]-1] = exp_total2[s[0]-1] + 1
            means = [float(exp_total2[i]) / float(exp_total1[i]) if exp_total1[i] > 0 else 0 for i in range(len(self.stimuli))]

        # Calculate the standard deviation
        if mode == 'spike':
            sd = [0 for i in self.stimuli]
            for trial in self.spikes:
                    sd[trial.stim-1] = sd[trial.stim-1] + pow(len(trial.spikes)-means[trial.stim-1],2)
            sd = [pow(sd[i],0.5)/count[i] if count[i] > 0 else 0 for i in range(0,len(self.stimuli))]

        if mode == 'fsl':
            sd = [0 for i in self.stimuli]
            for trial in self.spikes:
                if len(trial.spikes) > 0:
                    sd[trial.stim-1] = sd[trial.stim-1] + pow(min(trial.spikes)-means[trial.stim-1],2)
            sd = [pow(sd[i],0.5)/count[i] if count[i] > 0 else 0 for i in range(0,len(self.stimuli))]

        if mode == 'lsl':
            sd = [0 for i in self.stimuli]
            for trial in self.spikes:
                if len(trial.spikes) > 0:
                        sd[trial.stim-1] = sd[trial.stim-1] + pow(max(trial.spikes)-means[trial.stim-1],2)
            sd = [pow(sd[i],0.5)/count[i] if count[i] > 0 else 0 for i in range(0,len(self.stimuli))]


        FILE = open(filename+'_means_'+str(0), "w")
        for i in range(len(self.stimuli)):
            max_mean = max(max_mean,means[i]) # For use in setting the y axis limit
            min_mean = min(min_mean,means[i]) # For use in setting the y axis limit
            line = str(i+1)+','+str(means[i])
            if len(sd) == len(means):
                line = line+','+str(sd[i])
            print >>FILE, line
        FILE.close()

        s = ['size '+str(self.w*self.scale)+' '+str(self.h*self.scale)]
        s.append('set font psh')
        s.append('set hei '+str(0.3 * self.scale))
        s.append('begin graph')
        s.append('nobox')
        s.append('x2axis off')
        s.append('y2axis off')
        s.append('scale auto')

        if self.VariableType == 0:
            s.append('xtitle "Stimulus Duration (ms)" hei '+str(0.2*self.scale))
        if self.VariableType == 1:
            s.append('xtitle "Stimulus Delay (ms)" hei '+str(0.2*self.scale))

        if mode == 'spike':
            s.append('ytitle "Mean Spikes per Trial" hei '+str(0.2*self.scale))
        if mode == 'fsl':
            s.append('ytitle "Mean First Spike Latency (ms)" hei '+str(0.2*self.scale))
        if mode == 'lsl':
            s.append('ytitle "Mean Last Spike Latency (ms)" hei '+str(0.2*self.scale))


        s.append('xticks length '+str(-0.1*self.scale))
        s.append('yticks length '+str(-0.1*self.scale))
        s.append('title ""')
        s.append('xaxis min 0 max '+str(len(self.stimuli)))
        s.append('yaxis min '+str(round(min_mean))+' max '+str(round(2*max_mean+0.5)/2))
        s.append('xaxis dsubticks '+str(1.0*self.scale))
        s.append('yaxis dsubticks '+str(0.25*self.scale))
        s.append('yaxis dticks '+str(0.5*self.scale))
        s.append('xaxis nofirst')

        xnames = ''
        # Display the appropriate x-axis
        if self.VariableType == 0:
            for d in self.stimuli:
                xnames = xnames + ' ' + str(int(d.dur[self.Channel]))
        if self.VariableType == 1:
            for d in self.stimuli:
                xnames = xnames + ' ' + str(int(d.delay[self.Channel]-self.rasterOffset))

        xplaces = ''
        for xp in range(len(self.stimuli)):
            xplaces = xplaces + ' ' + str(xp+1)

        long_scale = 1.0
        if len(self.stimuli) > 15:
            long_scale = 0.6

        s.append('xnames '+xnames)
        s.append('xplaces '+xplaces)
        s.append('xlabels hei '+str(0.25*self.scale*long_scale))
        s.append('ylabels hei '+str(0.20*self.scale))
        s.append('xlabels dist '+str(0.15*self.scale))

        s.append('data "'+filename.rsplit('/')[-1]+'_means_0"')
        if len(means) != len(sd):
            s.append('d1 line msize '+str(0.11*self.scale)+' marker '+self.markers[0])
        else:
            s.append('d1 line msize '+str(0.11*self.scale)+' marker '+self.markers[0]+' errup d2 errdown d2')

        s.append('end graph')

        if notes != '':
            s.append('amove xg(30) yg(6)')
            s.append('set hei 0.15')
            s.append('begin text')
            s.append(notes)
            s.append('end text')

        FILE = open(filename+'.gle', "w")
        FILE.writelines('\n'.join(s))
        FILE.close()

        call(['gle', '-device',self.format,'-output',filename+'.'+self.format, filename+'.gle'])
        self.filename = filename

    def spikeraster(self, filename, notes=''):

        self.cleantmp()

        # spikes: 3D list of spikes [trial][duration index][spikes]
        # Create the data file
        binned = self.binspikes()
        s1tmp = binned[0]
        s2tmp = binned[1]
        s3tmp = binned[2]
        ynames = ''

        s1 = []
        s2 = []
        s3 = []
        for s in s1tmp:
            s1.append(str(s[1])+' '+str(s[2]))
        for s in s2tmp:
            s2.append(str(s[1])+' '+str(s[2]))
        for s in s3tmp:
            s3.append(str(s[1])+' '+str(s[2]))

        # What we guess are channel 1 spikes
        FILE = open(filename+'_spikes_1', "w")
        FILE.writelines('\n'.join(s1))
        FILE.close()

        # What we guess are channel 2 spikes
        if len(s2) > 0:
            FILE = open(filename+'_spikes_2', "w")
            FILE.writelines('\n'.join(s2))
            FILE.close()

        # What we guess are spontaneous spikes
        if len(s3) > 0:
            FILE = open(filename+'_spikes_3', "w")
            FILE.writelines('\n'.join(s3))
            FILE.close()

        s = ['size '+str(self.w*self.scale)+' '+str(self.h*self.scale)]
        s.append('set font psh')
        s.append('set hei '+str(0.3 * self.scale))
        s.append('begin graph')
        s.append('nobox')
        s.append('x2axis off')
        s.append('y2axis off')
        s.append('scale auto')
        s.append('xtitle "Time (ms)" hei '+str(0.2*self.scale))

        if self.VariableType == 0:
            s.append('ytitle "Stimulus Duration (ms)" hei '+str(0.2*self.scale))
        if self.VariableType == 1:
            s.append('ytitle "Stimulus Delay (ms)" hei '+str(0.2*self.scale))

        s.append('xticks length '+str(-0.1*self.scale))
        s.append('yticks length '+str(-0.1*self.scale))
        s.append('title ""')
        if self.rasterEnd <= self.rasterStart:
            self.rasterEnd = self.rasterStart + 1
        s.append('xaxis min '+str(self.rasterStart)+' max '+str(self.rasterEnd))
        s.append('yaxis min 0 max '+str(len(self.stimuli)+0.9))
        s.append('yaxis nticks 0')
        s.append('yaxis nsubticks 0')
        s.append('ysubticks off')

        # Display the appropriate y-axis
        if self.VariableType == 0:
            for d in self.stimuli:
                ynames = ynames + ' ' + str(d.dur[self.Channel])
        if self.VariableType == 1:
            for d in self.stimuli:
                ynames = ynames + ' ' + str(d.delay[self.Channel]-self.rasterOffset)

        yplaces = ''
        for yp in range(len(self.stimuli)):
            yplaces = yplaces + ' ' + str(yp+1)

        long_scale = 1.0
        if len(self.stimuli) > 25:
            long_scale = 0.6

        s.append('ynames '+ynames)
        s.append('yplaces '+yplaces)
        s.append('xlabels hei '+str(0.25*self.scale))
        s.append('ylabels hei '+str(0.20*self.scale*long_scale))
        s.append('xlabels dist '+str(0.15*self.scale))
        s.append('data "'+filename.rsplit('/')[-1]+'_spikes_1"')
        s.append('d1 marker dot msize '+str(0.10*self.scale)+' color blue')
        if len(s2) > 0:
            s.append('data "'+filename.rsplit('/')[-1]+'_spikes_2"')
            s.append('d2 marker dot msize '+str(0.10*self.scale)+' color red')
        if len(s3) > 0:
            s.append('data "'+filename.rsplit('/')[-1]+'_spikes_3"')
            s.append('d3 marker dot msize '+str(0.10*self.scale)+' color black')

        s.append('end graph')

        # Plot the stimuli
        count = 0
        line_height = 0.02*self.scale
        s.append('set lwidth '+str(line_height))
        for stim in self.stimuli:
            count = count + 1
            for i in range(0,len(stim.dur)):
                if i == 0:
                    s.append('set color blue')
                if i == 1:
                    s.append('set color red')
                s.append('amove xg('+str(stim.delay[i]-self.rasterOffset)+') yg('+str(count+i*2*line_height)+')')
                s.append('aline xg('+str(stim.delay[i]+stim.dur[i]-self.rasterOffset)+') yg('+str(count+i*2*line_height)+')')

        if notes != '':
            s.append('amove xg(30) yg(6)')
            s.append('set hei 0.12')
            s.append('begin text')
            s.append(notes)
            s.append('end text')

        FILE = open(filename+'.gle', "w")
        FILE.writelines('\n'.join(s))
        FILE.close()

        call(['gle', '-device',self.format, '-output',filename+'.'+self.format, filename+'.gle'])
        self.filename = filename
