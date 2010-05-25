import sys
from GLE import *
from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import askokcancel
from tkFileDialog import askdirectory
import tempfile
from PIL import Image, ImageTk


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createVariables()
        self.createWidgets()
        self.bind("<Destroy>", self.windowdestroy)

    def windowdestroy(self, event):
        self.quit()

    def quit(self):
        self.GLE.cleantmp()
        Frame.quit(self)

    def createVariables(self):
        self.filename = ''
        self.clean_filename = StringVar()
        self.clean_filename.set('No File Loaded')
        self.cellID = StringVar()
        self.frequency = StringVar()
        self.amplitude = StringVar()
        self.rasterOffset = StringVar()
        self.rasterOffset.set('0')
        self.rasterStart = StringVar()
        self.rasterStart.set('-0.5')
        self.rasterEnd = StringVar()
        self.rasterEnd.set('')
        self.rasterYAxisChannel = IntVar()
        self.rasterYAxisType = IntVar()
        self.stimFilterA = StringVar()
        self.stimFilterB = StringVar()

        self.binWindow = StringVar()
        self.binWindow.set('20')
        self.GLE = GLE()

    def stimuliFilter(self):
        s = []
        for stim in range(len(self.stimuli)):
            if stim+1 >= int(self.stimFilterA.get()) and stim+1 <= int(self.stimFilterB.get()):
                s.append(self.stimuli[stim])
        return s

    def spikesFilter(self):
        s = []
        for spike in self.spikes:
            if spike.stim >= int(self.stimFilterA.get()) and spike.stim <= int(self.stimFilterB.get()):
                newSpike = Spikes()
                newSpike.stim = spike.stim - int(self.stimFilterA.get())+1
                newSpike.spikes = spike.spikes
                s.append(newSpike)
        return s

    def setupPlot(self):
        G = self.GLE
        G.scale = 4
        G.rasterStart = float(self.rasterStart.get())
        G.rasterEnd = float(self.rasterEnd.get())
        G.rasterOffset = float(self.rasterOffset.get())
        G.format = 'png' # Used for previewing
        G.stimuli = self.stimuli
        G.spikes = self.spikes
        G.stimFilterA = int(self.stimFilterA.get())
        G.stimFilterB = int(self.stimFilterB.get())
        G.Channel = self.rasterYAxisChannel.get()
        G.VariableType = self.rasterYAxisType.get()
        G.binWindow = float(self.binWindow.get())

    def previewSpikeRaster(self):
        tmpname = tempfile.mkstemp()
        notes = ''
        self.setupPlot()
        self.GLE.spikeraster(tmpname[1], notes)
        image = Image.open(tmpname[1]+'.'+self.GLE.format)
        self.previewImage = ImageTk.PhotoImage(image)
        self.previewLabel.config(image=self.previewImage)

    def previewMeanSpikes(self):
        tmpname = tempfile.mkstemp()
        notes = ''
        self.setupPlot()
        self.GLE.meanspikespertrial(tmpname[1], 'spike', notes)
        image = Image.open(tmpname[1]+'.'+self.GLE.format)
        self.previewImage = ImageTk.PhotoImage(image)
        self.previewLabel.config(image=self.previewImage)

    def previewMeanFSL(self):
        tmpname = tempfile.mkstemp()
        notes = ''
        self.setupPlot()
        self.GLE.meanspikespertrial(tmpname[1], 'fsl', notes)
        image = Image.open(tmpname[1]+'.'+self.GLE.format)
        self.previewImage = ImageTk.PhotoImage(image)
        self.previewLabel.config(image=self.previewImage)

    def previewMeanLSL(self):
        tmpname = tempfile.mkstemp()
        notes = ''
        self.setupPlot()
        self.GLE.meanspikespertrial(tmpname[1], 'lsl', notes)
        image = Image.open(tmpname[1]+'.'+self.GLE.format)
        self.previewImage = ImageTk.PhotoImage(image)
        self.previewLabel.config(image=self.previewImage)

    def previewSpikeRatio(self):
        tmpname = tempfile.mkstemp()
        notes = ''
        self.setupPlot()
        self.GLE.meanspikespertrial(tmpname[1], 'ratio', notes)
        image = Image.open(tmpname[1]+'.'+self.GLE.format)
        self.previewImage = ImageTk.PhotoImage(image)
        self.previewLabel.config(image=self.previewImage)

    def createWidgets(self):
        # Setup the menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', underline=0, menu=fileMenu)

        # Setup the main frames
        self.settingsFrame = LabelFrame(self, text='General Settings')
        self.settingsFrame.grid(column=0, row=0, sticky=N+S+E+W)
        self.graphFrame = LabelFrame(self, text='Generated Graph')
        self.graphFrame.grid(column=1, row=0, sticky=N+S, rowspan=3)
        self.spikeSettingsFrame = LabelFrame(self, text='Data Filters')
        self.spikeSettingsFrame.grid(column = 0, row = 1, sticky=E+W)
        self.graphButtonFrame = LabelFrame(self, text='Generate Graphs')
        self.graphButtonFrame.grid(column=0, row=2, sticky=N+S+E+W)
        self.saveGraphButtonFrame = LabelFrame(self, text='Save Graphs')
        self.saveGraphButtonFrame.grid(column=0, row=3, sticky=N+S+E+W)


        # Settings frame widgets
        self.fileLabel = Label(self.settingsFrame, textvariable=self.clean_filename)
        self.fileLabel.grid(column=0, row=0)
        self.fileOpen = Button(self.settingsFrame, text='Open Spike File', command=self.openSpikeFile)
        self.fileOpen.grid(column=1, row=0)

        self.cellIDLabel = Label(self.settingsFrame, text='Cell ID')
        self.cellIDLabel.grid(column=0, row=1, sticky=E)
        self.cellIDEntry = Entry(self.settingsFrame, textvariable=self.cellID, width=12, state=DISABLED)
        self.cellIDEntry.grid(column=1, row=1, sticky=W)

        self.frequencyLabel = Label(self.settingsFrame, text='Frequency')
        self.frequencyLabel.grid(column=0, row=2, sticky=E)
        self.frequencyEntry = Entry(self.settingsFrame, textvariable=self.frequency, width=12, state=DISABLED)
        self.frequencyEntry.grid(column=1, row=2, sticky=W)

        self.amplitudeLabel = Label(self.settingsFrame, text='Amplitude')
        self.amplitudeLabel.grid(column=0, row=3, sticky=E)
        self.amplitudeEntry = Entry(self.settingsFrame, textvariable=self.amplitude, width=20, state=DISABLED)
        self.amplitudeEntry.grid(column=1, row=3, sticky=W)

        self.spikeOffsetLabel = Label(self.spikeSettingsFrame, text='Zero Time At')
        self.spikeOffsetLabel.grid(column=0, row=0, sticky=E)
        self.spikeOffsetEntry = Entry(self.spikeSettingsFrame, textvariable=self.rasterOffset, width=5, state=DISABLED)
        self.spikeOffsetEntry.grid(column=1, row=0, sticky=W)
        self.timeOffsetLabel = Label(self.spikeSettingsFrame, text='Time Start')
        self.timeOffsetLabel.grid(column=0, row=1, sticky=E)
        self.timeOffsetEntry = Entry(self.spikeSettingsFrame, textvariable=self.rasterStart, width=5, state=DISABLED)
        self.timeOffsetEntry.grid(column=1, row=1, sticky=W)
        self.maxTimeLabel = Label(self.spikeSettingsFrame, text='Time End')
        self.maxTimeLabel.grid(column=0, row=2, sticky=E)
        self.maxTimeEntry = Entry(self.spikeSettingsFrame, textvariable=self.rasterEnd, width=5, state=DISABLED)
        self.maxTimeEntry.grid(column=1, row=2, sticky=W)
        self.binWindowLabel = Label(self.spikeSettingsFrame, text='Classifier Window')
        self.binWindowLabel.grid(column=0,row=3,sticky=E)
        self.binWindowEntry = Entry(self.spikeSettingsFrame, textvariable=self.binWindow, width=5, state=DISABLED)
        self.binWindowEntry.grid(column=1,row=3,sticky=W)
        self.stimFilterLabel = Label(self.spikeSettingsFrame, text='Stimuli')
        self.stimFilterLabel.grid(column=0, row=4)
        self.stimFilterAEntry = Entry(self.spikeSettingsFrame, textvariable=self.stimFilterA, width=2, state=DISABLED)
        self.stimFilterAEntry.grid(column=1, row=4,stick=W)
        self.stimFilterBEntry = Entry(self.spikeSettingsFrame, textvariable=self.stimFilterB, width=2, state=DISABLED)
        self.stimFilterBEntry.grid(column=1, row=4, sticky=E)


        # Graph Generators
        self.genRasterButton = Button(self.graphButtonFrame, text='Spike Raster', command=self.previewSpikeRaster, state=DISABLED)
        self.genRasterButton.grid(column=0, row=0)
        self.genMeansButton = Button(self.graphButtonFrame, text='Spikes per Trial', command=self.previewMeanSpikes, state=DISABLED)
        self.genMeansButton.grid(column=1, row=0)
        self.genMeanFSL = Button(self.graphButtonFrame, text='Mean FSL', command=self.previewMeanFSL, state=DISABLED)
        self.genMeanFSL.grid(column=0, row=1)
        self.genMeanLSL = Button(self.graphButtonFrame, text='Mean LSL', command=self.previewMeanLSL, state=DISABLED)
        self.genMeanLSL.grid(column=1, row=1)
        self.genSpikeRatio = Button(self.graphButtonFrame, text='Spike Ratio', command=self.previewSpikeRatio, state=DISABLED)
        self.genSpikeRatio.grid(column=0, row=2)
        self.rasterYAxisChannelRadio1 = Radiobutton(self.graphButtonFrame, text="Channel 1", variable=self.rasterYAxisChannel, value=0, state=DISABLED)
        self.rasterYAxisChannelRadio1.grid(column=0, row=3)
        self.rasterYAxisChannelRadio2 = Radiobutton(self.graphButtonFrame, text="Channel 2", variable=self.rasterYAxisChannel, value=1, state=DISABLED)
        self.rasterYAxisChannelRadio2.grid(column=1, row=3)

        self.rasterYAxisDurationRadio = Radiobutton(self.graphButtonFrame, text="Duration", variable=self.rasterYAxisType, value=0, state=DISABLED)
        self.rasterYAxisDurationRadio.grid(column=0,row=4)
        self.rasterYAxisDelayRadio = Radiobutton(self.graphButtonFrame, text="Delay", variable=self.rasterYAxisType, value=1, state=DISABLED)
        self.rasterYAxisDelayRadio.grid(column=1,row=4)

        self.qgleButton = Button(self.saveGraphButtonFrame, text='Launch QGLE', command=self.launchQGLE, state=DISABLED)
        self.qgleButton.grid(column=0, row=0)
        self.saveButton = Button(self.saveGraphButtonFrame, text='Save GLE Script', command=self.saveGLE, state=DISABLED)
        self.saveButton.grid(column=1, row=0)

        # Graph frame widgets
        self.previewImage = PhotoImage()
        self.previewLabel = Label(self.graphFrame, image=self.previewImage)
        self.previewLabel.grid()

    def launchQGLE(self):
        self.GLE.launchQGLE()

    def saveGLE(self):
        folder = askdirectory(mustexist=True, title='Select Folder to Save To')
        if folder != ():
            self.GLE.save(folder,self.clean_filename.get().split('.')[0].replace('_','.'))

    def openSpikeFile(self):
        filename = askopenfilename(filetypes=[("Spike Text Files","*.txt")])
        if filename != []:
            self.filename = filename
            clean_filename = filename.rsplit('/',1)
            if len(clean_filename) == 1:
                clean_filename = clean_filename[0]
            else:
                clean_filename = clean_filename[1]
            self.clean_filename.set(clean_filename)
            # Guess that the filename is the cellID too
            self.cellID.set(clean_filename.split('.')[0].replace('_','.'))
            if self.parse():
                self.genRasterButton.config(state=NORMAL)
                self.genMeansButton.config(state=NORMAL)
                self.genMeanFSL.config(state=NORMAL)
                self.genMeanLSL.config(state=NORMAL)
                self.frequencyEntry.config(state=NORMAL)
                self.cellIDEntry.config(state=NORMAL)
                self.amplitudeEntry.config(state=NORMAL)
                self.spikeOffsetEntry.config(state=NORMAL)
                self.timeOffsetEntry.config(state=NORMAL)
                self.maxTimeEntry.config(state=NORMAL)
                self.rasterYAxisChannelRadio1.config(state=NORMAL)
                self.rasterYAxisDurationRadio.config(state=NORMAL)
                self.rasterYAxisDelayRadio.config(state=NORMAL)
                self.binWindowEntry.config(state=NORMAL)
                self.qgleButton.config(state=NORMAL)
                self.saveButton.config(state=NORMAL)
                self.stimFilterAEntry.config(state=NORMAL)
                self.stimFilterBEntry.config(state=NORMAL)
                self.stimFilterA.set('1')
                self.stimFilterB.set(str(len(self.stimuli)))
                if len(self.stimuli) > 0 and len(self.stimuli[0].dur) > 1:
                    self.rasterYAxisChannelRadio2.config(state=NORMAL)
                    self.genSpikeRatio.config(state=NORMAL)
                else:
                    self.rasterYAxisChannelRadio2.config(state=DISABLED)
                    self.genSpikeRatio.config(state=DISABLED)

                self.previewSpikeRaster()

    def parse(self):
        FILE = open(self.filename, "r")
        lines = FILE.readlines()
        FILE.close()

        found_stim = False
        found_data = False
        stimuli = []
        data = []
        curSweep = 0
        minStim = 0
        maxStim = 0
        for l in lines:
            if found_stim == True and l.strip() != 'n\tsweep\tX_value\tpass\tSpikeTimes':
                temp = l.strip().split('\t')
                if int(temp[0]) != curSweep:
                    if curSweep != 0:
                        stimuli.append(tmpStimulus)
                    tmpStimulus = Stimulus()
                    curSweep = int(temp[0])
                if temp[3] != 'OFF':
                    tmpStimulus.delay.append(float(temp[4]))
                    tmpStimulus.dur.append(float(temp[5]))
                    if float(temp[4]) < minStim:
                        minStim = float(temp[4])
                    if float(temp[4])+float(temp[5]) > maxStim:
                        maxStim = float(temp[4])+float(temp[5])

            if found_data == True:
                data.append(l.strip().split('\t'))

            if l.strip()[0:17] == 'Sweep\tTime_Offset':
                found_stim = True
            if l.strip() == 'n\tsweep\tX_value\tpass\tSpikeTimes':
                found_data = True
                found_stim = False
                stimuli.append(tmpStimulus) # Add our last stimulus


        # Record spike times
        spikes = []
        max_spike = -100
        for d in data:
            S = Spikes()
            S.stim = int(d[1])
            if len(d) > 4:
                S.spikes = [float(i) for i in d[4].split(',')]
                max_spike = max(max_spike, max(S.spikes))
            spikes.append(S)

        filename = self.filename
        self.spikes = spikes
        self.stimuli = stimuli
        self.rasterStart.set(float(minStim-0.5))
        self.rasterEnd.set(max([maxStim+minStim+1,int(round(max_spike/10+1)*10)]))
        self.rasterOffset.set(0)
        return found_data


app = Application()
app.master.title("Spike Data Parser")
app.mainloop()
