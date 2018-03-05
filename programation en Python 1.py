from pyo import *
import random

s = Server().boot()


#atmos
a = Fader(fadein=0.1, fadeout=0.5, mul=0.20, add=0)
env1 = Adsr(attack=2, decay=3, sustain=2, release=0.5)
atmososc1 = RCOsc(freq=100, sharp=0.5, mul=0.2)
atmososc2 = FM(carrier=100, ratio=0.5, index=5, mul=0.3, add=0)
reverbatmos = Freeverb(atmososc1+atmososc2, size=1, damp=0.2, bal=0.7)
lowpass = Biquad(reverbatmos, freq=150, q=1, type=2)
p = Pan(lowpass, outs=2, pan=0.5).out()



count = 0
def atmos():
    global count
    count += 1
    if count == 2:
        count=0
    if count == 0:
        atmososc1.freq=250
        atmososc2.carrier=200
        p.pan=0.4
        a.play()
        env1.play()
    if count == 1:
        atmososc1.freq=350
        atmososc2.carrier=150
        p.pan=0.6
        a.play()
        env1.play()
    
atmosplay= Pattern(atmos, time=2).play(dur=115)



#lead
tab = HarmTable(list=[(150, 0.7), (400, 3), (550, .6), (1100, .8), (8191, 1.0)], size=8192)
bang = Metro(time=0.5, poly=8)
leadevent = TrigEnv(bang, table=tab, dur=bang*1, mul=.3)
midifreq = TrigXnoiseMidi(bang, dist=5, x1=1, x2=.5, scale=0, mrange=(64,72))
leadsnap = Snap(midifreq, choice=[1,2,5,7,9], scale=1)
leadosc1 = SineLoop(freq=leadsnap, feedback=0.1, mul=leadevent)
filterlead = Biquad(leadosc1, freq=3000, q=1, type=0, mul=0.3, add=0)
reverblead = Freeverb(filterlead, size=1, damp=0.2, bal=0.7).out()


def lead():
    bang.play()

leadplay= Pattern(lead, time=0.2).play(delay=40)


#bass
tab2 = CosTable([(0,0), (200,1), (600,0.3), (8191,0)])
beat = Beat(time=0.1, taps=16, w1=[90,80], w2=50, w3=35, poly=1)
bassevent2 = TrigEnv(beat, table=tab2, dur=beat*1, mul=3)
midifreq2 = TrigXnoiseMidi(beat, dist=1, x1=0.5, x2=0.5, scale=0, mrange=(10,13))
basssnap2 = Snap(midifreq2, choice=[2,4], scale=1)
bassosc2 = SuperSaw(freq=basssnap2, mul=bassevent2)
basslead = Biquad(bassosc2, freq=500, q=1, type=0 , mul=1, add=0).out()


def bass():
    beat.play()

bassplay= Pattern(bass, time=0.2).play(delay=20)




def bass_stop():
    bassplay.stop()
    beat.stop()
  
 
def lead_stop():
    leadplay.stop()
    bang.stop()


def atmos_stop():
    atmos.stop()
    a.stop()
    env.play()



atmosphereStop = CallAfter(atmos_stop, time=120).play()
leadstop = CallAfter(lead_stop, time=100).play()
bassstop = CallAfter(bass_stop, time=110).play()


s.gui(locals())
