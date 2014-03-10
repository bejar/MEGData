# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:11:29 2013

@author: bejar
"""
import numpy as np
import scipy.io
import matplotlib
matplotlib.use('SVG')
from pylab import *
from numpy.fft import rfft, irfft 
import pywt

def plotSignalValues(signal1,name):
    fig = plt.figure()
    minaxis=min(signal1)
    maxaxis=max(signal1)
    num=len(signal1)  
    print num
    sp1=fig.add_subplot(111)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,signal1)
    plt.savefig(cres+name)
    plt.show()   
    
def plotSignalValues2(signal1,name):
    fig = plt.figure()
    minaxis=min(signal1[:,0])
    maxaxis=max(signal1[:,0])
    num=len(signal1)  
    print num
    sp1=fig.add_subplot(111)
#    sp1.axis([0,num,minaxis,maxaxis])
    sp1.plot(signal1[:,0],signal1[:,1])
    plt.savefig(cres+name)
    plt.show()   


cpath='/home/bejar/MEG/Data/control/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
#name='MMN-201205251030'
name='control1-MMN'
mats=scipy.io.loadmat( cpath+name+'.mat')
data= mats['data']
chann=mats['names']
plotSignalValues(data[30,300:700],'signal1.svg')
plotSignalValues(data[30,800:1200],'signal2.svg')
#orig=data[90,0:500]
#
#temp= rfft(data[90,0:500])
#
#plotSignalValues(temp,'fft.svg')
#
#
#tempwA,tempwD=pywt.dwt(data[90,0:500], 'sym2')
#plotSignalValues(tempwD,'wave.svg')
#
#
#tlag=np.zeros((498,2))
#
#for i in range(498):
#    tlag[i,0]=(orig[i]-orig[i+1])
#    tlag[i,1]=(orig[i+1]-orig[i+2])
#    print tlag[i,:]
#    
#plotSignalValues2(tlag,'tlag.svg')
    
