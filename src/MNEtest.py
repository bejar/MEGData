# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:23:03 2013

Testing MNE library

@author: bejar
"""

from mne.fiff.bti import read_raw_bti
from mne.viz import circular_layout, plot_connectivity_circle
import numpy as np
import matplotlib.pyplot as plt

        
def plotOneSignal(signal):
    fig = plt.figure()
    minaxis=min(signal)
    maxaxis=max(signal)
    num=len(signal)    
    sp1=fig.add_subplot(111)
#    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,signal)
    plt.show() 
         

a=read_raw_bti('/home/bejar/MEG/ESQ21com10/ESQ21com10/MEG@-EKG/05@-25@-12@_10:00/1/c,rfhp1.0Hz')
cnames= a.info['ch_names'][0:148]

con=np.array([0.2,0.3,0.4,0.8,0.9])
lind=(np.array([12,79,123,104,97,61]),np.array([88,36,74,27,32,54]))

plot_connectivity_circle(con, cnames, indices=lind,title='Connections',n_lines=6,
                         linewidth=3,colormap='hot',vmin=0,vmax=1)
plt.savefig('circle.png', facecolor='black')
plt.show()