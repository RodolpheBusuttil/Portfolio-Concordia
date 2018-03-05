from pyo import*

s = Server().boot()

sample = 'Pad-a#0.wav' 

class AutoWah: 
    def __init__(self, sample, mini=450, maxi=2500, freq=30, q=10):
        self.source = sample
        self.minimum = mini
        self.maximum = maxi
        self.frequence = freq
        self.quality = q
        self.player = SfPlayer(self.source, speed=1, loop=True)
        self.follo = Follower(self.player, freq=self.frequence)
        self.bandpassfreq = self.follo * (self.maximum - self.minimum) + self.minimum
        self.bandpass = Biquad(self.player, freq=self.bandpassfreq, q=self.quality, type=2)
        

    def SetMinimum(self, x):
        self.minimum.value = x
    def SetMaximum(self, x):
        self.minimum.value = x
    def SetFrequence(self, x):
        self.frequence.value = x
    def SetQuality(self, x):   
        self.quality.value = x        
        
    def sig(self):
        return self.bandpass

    def out ( self, chnl):
        self.bandpass.out(chnl+chnl)
        return self
            
    
effet = AutoWah(sample).out(0)
 
s.gui(locals())
